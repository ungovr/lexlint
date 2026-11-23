# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Merge a LexLint run into lexlint.yml. Needs python3 with PyYAML."""
import argparse
import json
import os
import re
import string
import sys
import tempfile

try:
    import yaml
except ImportError:  # --help still works; a merge says what to do instead
    yaml = None

# Exit codes, one per way the merge stops; --help lists them for the agent.
EXIT_OK = 0
EXIT_USAGE = 2
EXIT_NO_RUNS = 3
EXIT_MANIFEST = 4
EXIT_RUN_SHAPE = 5

DESCRIPTION = """\
Merge one LexLint run into lexlint.yml, the way step 4 of the procedure says.

Each finding's triage (state, where, note, handled_by) is carried across by
id, or, where an id moved, by the second match (exactly one candidate on each
side with the same note code, or the same id once a collision suffix is set
aside); lint.work_items is kept as it was, save that an id matched that way is
rewritten to the new one; an acknowledged finding the run no longer returns
moves to lint.vanished; only the lint: block is rewritten, and everything
above and below it is kept byte for byte. stdout carries exactly
one JSON object of counts for the report; every diagnostic goes to stderr."""

EPILOG = """\
examples:
  one run_lint call, merged into the manifest in place:
    python3 %(prog)s lint.json --manifest lexlint.yml -o lexlint.yml \\
        --run-at 2026-10-22 --tool 'lexlint 1.86.0' \\
        --summary 'Six findings, five instruments, across three jurisdictions.'

  a split run of three calls, counted without writing anything:
    python3 %(prog)s lint-1.json lint-2.json lint-3.json \\
        --manifest lexlint.yml -o lexlint.yml \\
        --run-at 2026-10-22 --tool 'lexlint 1.86.0' --dry-run

  On a python3 without PyYAML, run it as `uv run %(prog)s ...` with the same
  arguments: the script's own header declares the dependency.

exit codes:
  0  merged, or under --dry-run, counted
  2  usage: a flag missing or malformed, or no PyYAML for this python3
  3  no run: a run file is not there, or the run has no findings
     (--allow-empty if that is really the run)
  4  manifest: lexlint.yml or --previous cannot be read, is not YAML, has no
     profile block, or cannot be written
  5  run shape: a run file is not JSON, carries no findings list, holds a
     finding with no id, or comes from a different corpus build than the rest
"""

CARRY = ("state", "where", "note", "handled_by")
# A jurisdiction is ASCII, and only its ASCII case folds: str.lower() would read
# U+212A KELVIN SIGN as "k" and name a place the profile does not.
ASCII_LOWER = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)
KEYS = {
    "lint": ("run_at", "tool", "summary", "findings", "work_items", "vanished"),
    "findings": (
        "id", "severity", "kind", "jurisdiction", "jurisdiction_name",
        "jurisdiction_flag", "summary", "name", "detail", "why", "matched_by", "posture", "basis",
        "citation", "url", "note_url", "catalog", "status", "requires", "applies_to",
        "owed", "requires_elsewhere", "role", "flows", "reading", "customer_duty_id", "instrument_id",
        "capability", "stated_by", "inferred_from", "derived_from", "moments",
        "effective_date", "lifecycle", "in_force", "certainty", "settledness",
        "court_action", "as_of_date",
        "stale", "confidence", "resolved_from") + CARRY,
    "work_items": ("id", "lane", "title", "findings", "jurisdictions"),
    "vanished": ("id", "last_seen") + CARRY + ("note_url", "citation", "name"),
}

# A note link is LexLint's page on one law, `/l/<short code>`. The code is set
# when the law is researched, so a citation edit or a collision suffix leaves
# it alone. The old host still appears in manifests written before the move.
# Exact host and https only: a link anywhere else names no law of ours.
NOTE_PREFIXES = ("https://lexlint.io/l/", "https://lexlint.org/l/")  # suppress: lexlint-legacy-domain -- older manifests carry note links on the old host

def note_code(url):
    """The short code in a LexLint note link, or None."""
    if not isinstance(url, str):
        return None
    for prefix in NOTE_PREFIXES:
        if url.startswith(prefix):
            return url[len(prefix):].strip("/") or None
    return None

# The suffix the server adds when two findings would share an id: FNV-1a over
# 32 bits, in base 36, padded to seven. 2**32 - 1 is `1z141z3`, so a real
# suffix starts with 0 or 1, which keeps a seven-letter word from reading as one.
SUFFIX = re.compile(r"-[01][0-9a-z]{6}\Z")
# One per jurisdiction or per run by construction, so never suffixed: these ids are
# used whole (`activity:deploys-chatbot` ends in seven letters, not a hash).
STRUCTURAL = ("activity", "derived", "topic")

def plain(fid):
    """An id about one jurisdiction that is not structural: the only kind the
    second match reads."""
    return ":" in fid and fid.split(":", 1)[0] not in STRUCTURAL

def base_id(fid):
    """`fid` with its collision suffix set aside, or None when it has none. A
    customer duty is its instrument's final id plus `:customer`, so its suffix
    sits before that tail, and the tail is kept."""
    if not isinstance(fid, str) or not plain(fid):
        return None
    tail = ":customer" if fid.endswith(":customer") else ""
    m = SUFFIX.search(fid[:len(fid) - len(tail)])
    base = fid[:m.start()] if m else ""
    if ":" not in base or base.endswith(":"):
        return None
    return base + tail

def slug_of(text):
    """The server's citation slug for an instrument id, character for
    character: lowercase, every run of anything but a-z and 0-9 one `-`, no
    `-` at either end, cut at 60 characters."""
    s = re.sub(r"[^a-z0-9]+", "-", str(text or "").lower()).strip("-")
    return s[:60].rstrip("-") or "unnamed"

def worker_id(e):
    """The unsuffixed id the server derives for this entry's law, from its
    citation, or its name when it has none, as the server does; None when the
    entry carries neither (a vanished entry written before it kept one)."""
    src = next((v for v in (e.get("citation"), e.get("name")) if isinstance(v, str) and v),
               None)
    if src is None:
        return None
    tail = ":customer" if e["id"].endswith(":customer") else ""
    return e["id"].split(":", 1)[0] + ":" + slug_of(src) + tail

def kin(a, b):
    """The same kind where both say one. A customer duty (its id ends
    `:customer`) is never its instrument, whatever either side records."""
    ka, kb = a.get("kind"), b.get("kind")
    if isinstance(ka, str) and ka and isinstance(kb, str) and kb and ka != kb:
        return False
    return a["id"].endswith(":customer") == b["id"].endswith(":customer")

def cite(e):
    c = e.get("citation")
    c = c.strip() if isinstance(c, str) else c
    return None if c in (None, "", []) else c

def by_code(e):
    code = note_code(e.get("note_url"))
    return [(e["id"].split(":", 1)[0], code)] if code else []

def by_base(e):
    return [k for k in (e["id"], base_id(e["id"])) if k]

def same_base(n, o):
    """The shared unsuffixed id must be proven the server's own id for the
    law, by each side whose tail is set aside: that side's own citation (or
    name) slugs to exactly it, so a seven-character token that belongs to a
    name is never set aside as a suffix, and a side with nothing to prove it
    matches nothing. A side that carries a citation or name must slug to it
    too. Equal citations where both carry one, and never two different note
    codes: the code names the law, so two codes are two laws. A code missing
    on either side is allowed, since a law can gain a note page later."""
    bn, bo = base_id(n["id"]), base_id(o["id"])
    shared = n["id"] if n["id"] == bo else o["id"] if o["id"] == bn else bn if bn == bo else None
    if shared is None:
        return False
    stripped = [e for e in (n, o) if e["id"] != shared]
    if any(worker_id(e) != shared for e in stripped):
        return False
    if any(worker_id(e) not in (None, shared) for e in (n, o)):
        return False
    cn, co = note_code(n.get("note_url")), note_code(o.get("note_url"))
    if cn and co and cn != co:
        return False
    return (cite(n) is None or cite(o) is None or cite(n) == cite(o)) and kin(n, o)

def pair(news, olds, keys, fits):
    """{new id: previous id} for each pair that is the only candidate the other
    side has. More than one either way is no match."""
    bucket = {}
    for o in olds:
        for k in keys(o):
            bucket.setdefault(k, []).append(o)
    cand, back = {}, {}
    for n in news:
        found = {}
        for k in keys(n):
            for o in bucket.get(k, ()):
                if fits(n, o):
                    found[o["id"]] = o
        cand[n["id"]] = list(found)
        for oid in found:
            back.setdefault(oid, []).append(n["id"])
    return {nid: found[0] for nid, found in cand.items()
            if len(found) == 1 and back[found[0]] == [nid]}

def second_match(findings, prev, prev_f, prev_v):
    """{new id: previous id} for every finding whose id moved.

    Only what the exact-id pass left on both sides is read. The same kind, the
    same declared slug and the same note code first; then the same id once a
    collision suffix is set aside on either side, where a citation or name
    proves the shared id is the server's own (same_base). When in doubt
    nothing is matched and the entry is left as it was: an id held twice in
    the previous manifest is never a candidate.
    """
    held = {}
    for block in ("findings", "vanished"):
        entries = prev.get(block)
        for e in entries if isinstance(entries, list) else []:
            if isinstance(e, dict) and isinstance(e.get("id"), str):
                held[e["id"]] = held.get(e["id"], 0) + 1
    live = {f["id"] for f in findings}
    news = [f for f in findings if f["id"] not in held and plain(f["id"])]
    olds = [e for pid, e in list(prev_f.items()) + list(prev_v.items())
            if held.get(pid) == 1 and pid not in live and plain(pid)]
    moved = pair(news, olds, by_code, kin)
    taken = set(moved.values())
    moved.update(pair([n for n in news if n["id"] not in moved],
                      [o for o in olds if o["id"] not in taken], by_base, same_base))
    return moved

def follow(items, renamed):
    """Work items with each id the second match moved rewritten; no other id,
    and nothing of another shape, is touched."""
    if not renamed or not isinstance(items, list):
        return items
    out = []
    for it in items:
        ids = it.get("findings") if isinstance(it, dict) else None
        if isinstance(ids, list) and any(isinstance(i, str) and i in renamed for i in ids):
            it = dict(it, findings=[renamed[i] if isinstance(i, str) and i in renamed else i
                                    for i in ids])
        out.append(it)
    return out

def die(msg, code):
    sys.stderr.write(f"lexlint merge: {msg}\n")
    raise SystemExit(code)

def scalar(v):
    """One shape per value, so a client with no python3 can match it by hand."""
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    s = str(v)
    if any(escaped(c) for c in s):
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        s = s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        s = "".join(c if not escaped(c) else f"\\x{ord(c):02X}" if ord(c) <= 0xFF
                    else f"\\u{ord(c):04X}" for c in s)
        return f'"{s}"'
    return "'" + s.replace("'", "''") + "'"

def escaped(c):
    """A character YAML cannot carry raw: a control (C0, DEL, C1), U+FFFE and
    U+FFFF, which PyYAML refuses, and U+2028 and U+2029, which it reads as a
    line break (U+0085 is C1)."""
    o = ord(c)
    return o < 0x20 or 0x7F <= o <= 0x9F or o in (0x2028, 0x2029, 0xFFFE, 0xFFFF)

# A key YAML reads back as the same string, written bare; any other key
# (a newline in it, a leading digit, a boolean or null word) is quoted.
BARE_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_./-]*")
NOT_BARE = {"true", "false", "yes", "no", "on", "off", "null"}

def key(k):
    if isinstance(k, str) and BARE_KEY.fullmatch(k) and k.lower() not in NOT_BARE:
        return k
    return scalar(k)

def emit_map(d, ind, out, prefer=()):
    for k in [k for k in prefer if k in d] + sorted(set(d) - set(prefer)):
        v, pad = d[k], " " * ind
        if isinstance(v, dict) and v:
            out.append(f"{pad}{key(k)}:")
            emit_map(v, ind + 2, out, KEYS.get(k, ()))
        elif isinstance(v, list) and v:
            out.append(f"{pad}{key(k)}:")
            emit_seq(v, ind + 2, out, KEYS.get(k, ()))
        elif isinstance(v, (dict, list)):
            out.append(f"{pad}{key(k)}: " + ("{}" if isinstance(v, dict) else "[]"))
        else:
            out.append(f"{pad}{key(k)}: {scalar(v)}")

def emit_seq(items, ind, out, prefer=()):
    pad = " " * ind
    for it in items:
        if isinstance(it, (dict, list)) and it:
            sub = []
            (emit_map if isinstance(it, dict) else emit_seq)(it, ind + 2, sub, prefer)
            out.append(pad + "- " + sub[0][ind + 2:])
            out.extend(sub[1:])
        elif isinstance(it, dict):
            out.append(pad + "- {}")
        elif isinstance(it, list):
            out.append(pad + "- []")
        else:
            out.append(pad + "- " + scalar(it))

def split(text):
    """The manifest either side of the top-level lint: block, kept verbatim."""
    lines = text.split("\n")
    at = next((i for i, line in enumerate(lines) if re.match(r"^lint[ \t]*:", line)),
              None)
    if at is None:
        return text, ""
    end = next((j for j in range(at + 1, len(lines))
                if re.match(r"""^[A-Za-z_'"]""", lines[j])), len(lines))
    # `lint:` is the last top-level key the schema allows, so a run of blank
    # lines and column-0 comments at the end of that span is the developer's
    # footer rather than the block. Walk it back out, or the first merge eats
    # a file header nobody will notice is gone.
    while end > at + 1 and (not lines[end - 1].strip()
                            or lines[end - 1].startswith("#")):
        end -= 1
    return "\n".join(lines[:at]), "\n".join(lines[end:])

def load_run(paths):
    """Union every call, INTERSECT the per-run activity: findings."""
    calls = []
    for p in paths:
        try:
            with open(p, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            die(f"no run file at {p} ({exc.strerror or exc}); pass the files "
                f"step 3 wrote, one per run_lint call", EXIT_NO_RUNS)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            die(f"{p} is not UTF-8 text ({exc.reason} at byte {exc.start}); "
                f"re-save it as UTF-8 JSON, the run_lint response as it came",
                EXIT_RUN_SHAPE)
        try:
            call = json.loads(text)
        except ValueError as exc:
            die(f"{p} is not readable JSON: {exc}", EXIT_RUN_SHAPE)
        # The shape is checked before anything is read off the call, so a
        # root that is a list, a string or null stops here with its name.
        if not isinstance(call, dict) or not isinstance(call.get("findings"), list):
            die(f"{p} carries no findings list: expected the run_lint response "
                f"object with a findings array, so unwrap it first", EXIT_RUN_SHAPE)
        calls.append((p, call))
    stamps = sorted({str(c.get("corpus_built_at")) for _p, c in calls})
    if len(stamps) > 1:
        die("the calls report different corpus_built_at (" + ", ".join(stamps) +
            "): the law library rebuilt mid-run, so start again from the first call",
            EXIT_RUN_SHAPE)
    merged, per_call, ran = {}, [], set()
    for p, c in calls:
        # The slugs this call ran on, as the worker validated them: run_lint
        # echoes them as `jurisdictions`, findings or none.
        echo = c.get("jurisdictions")
        ran |= {j for j in echo if isinstance(j, str)} if isinstance(echo, list) else set()
        acts = set()
        for f in c["findings"]:
            fid = f.get("id") if isinstance(f, dict) else None
            if not isinstance(fid, str) or not fid:
                die(f"{p}: a finding carries no usable id: {fid!r}", EXIT_RUN_SHAPE)
            if fid.startswith("activity:"):
                acts.add(fid)
            merged.setdefault(fid, f)
        per_call.append(acts)
    keep = set.intersection(*per_call)
    return ([f for i, f in merged.items() if not i.startswith("activity:") or i in keep],
            sorted(set.union(*per_call) - keep), stamps[0], len(calls), ran)

def read_manifest(path):
    """A manifest's text and its parsed document, or a stop with EXIT_MANIFEST."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        die(f"cannot read {path}: {exc}", EXIT_MANIFEST)
    try:
        doc = yaml.safe_load(text)
    except (yaml.YAMLError, ValueError) as exc:
        # ValueError too: PyYAML raises it, not YAMLError, building a value
        # such as an impossible date (2026-02-30).
        die(f"{path} is not YAML this script can read: {exc}", EXIT_MANIFEST)
    return text, doc

def main():
    ap = argparse.ArgumentParser(
        description=DESCRIPTION, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", metavar="runs",
                    help="the run_lint response files step 3 wrote, one per call; "
                         "a split run passes every call, and activity: findings "
                         "are intersected across them")
    ap.add_argument("--manifest", required=True,
                    help="the manifest to merge into, normally lexlint.yml")
    ap.add_argument("--previous",
                    help="a manifest to take the previous triage from instead of "
                         "--manifest, such as one recovered with "
                         "git show HEAD:lexlint.yml")
    ap.add_argument("--run-at", required=True,
                    help="today's date, written to lint.run_at; the script never "
                         "reads a clock")
    ap.add_argument("--tool", required=True,
                    help="this bundle's own name and version, written to "
                         "lint.tool, such as 'lexlint 1.86.0'")
    ap.add_argument("--summary",
                    help="the one sentence you author, written to lint.summary")
    ap.add_argument("-o", "--output", required=True,
                    help="where to write the merged manifest; the same path as "
                         "--manifest merges in place")
    ap.add_argument("--allow-empty", action="store_true",
                    help="accept a run with no findings, which otherwise stops "
                         "the merge rather than overwrite triage with an empty block")
    ap.add_argument("--dry-run", action="store_true",
                    help="merge and print the counts, but write nothing")
    a = ap.parse_args()
    if yaml is None:
        die("PyYAML is not installed for this python3; run the script with "
            "`uv run`, which reads the dependency from its header, or write the "
            "lint: block by hand as step 4 describes", EXIT_USAGE)

    findings, act_gone, corpus, calls, ran = load_run(a.runs)
    if not findings and not a.allow_empty:
        die("this run has no findings: refusing to overwrite a manifest with an "
            "empty lint block (--allow-empty if that is really the run)",
            EXIT_NO_RUNS)
    text, doc = read_manifest(a.manifest)
    if not isinstance(doc, dict) or not isinstance(doc.get("profile"), dict):
        die(f"{a.manifest} carries no profile block, so it is not a lexlint.yml",
            EXIT_MANIFEST)
    prev_doc = doc
    if a.previous:
        _prev_text, prev_doc = read_manifest(a.previous)
        if prev_doc is None:
            prev_doc = {}
        if not isinstance(prev_doc, dict):
            die(f"{a.previous} is not a manifest: expected a mapping at the top",
                EXIT_MANIFEST)
    prev = prev_doc.get("lint") or {}
    if not isinstance(prev, dict):
        die(f"the lint: block of {a.previous or a.manifest} is not a mapping, so "
            f"its triage cannot be read", EXIT_MANIFEST)
    # A hand-edited manifest can hold anything. An entry with no string id is
    # skipped rather than crashing the merge or matching something by accident.
    prev_f = {f["id"]: f for f in prev.get("findings") or []
              if isinstance(f, dict) and isinstance(f.get("id"), str)}
    prev_v = {v["id"]: v for v in prev.get("vanished") or []
              if isinstance(v, dict) and isinstance(v.get("id"), str)}

    # An id that moved while its law did not (a collision suffix gained or
    # lost, a citation edited upstream) is matched by rule, not left to
    # vanish; a matched entry never goes to lint.vanished.
    moved = second_match(findings, prev, prev_f, prev_v)
    out_f, carried, restored, first, unknown = [], 0, 0, 0, set()
    for f in findings:
        # The run has no opinion about the four: drop them, then take the
        # developer's, matched on id, or on the id the second match found. A
        # key the schema does not name is dropped too, and named in the
        # summary: `finding` is closed, so writing it out lands a manifest
        # that fails the schema this bundle ships with.
        new = {k: v for k, v in f.items()
               if k in KEYS["findings"] and k not in CARRY}
        unknown |= set(f) - set(KEYS["findings"])
        old = moved.get(f["id"], f["id"])
        was = prev_f.get(old) or prev_v.get(old)
        new.update({k: was[k] for k in CARRY if was and was.get(k) not in (None, "")})
        new.setdefault("state", "new")
        if not was:
            first += 1
        elif new["state"] == "acknowledged" or any(new.get(k) for k in CARRY[1:]):
            carried += old in prev_f
            restored += old not in prev_f
        out_f.append(new)

    live = {f["id"] for f in out_f}
    kept = set(moved.values())                # matched by rule: never vanished
    vanished, topics, forgotten = [], 0, 0
    for pid, pf in prev_f.items():
        if pid in live or pid in kept:
            continue
        if pid.startswith("topic:"):
            topics += 1                       # dropped, never moved to vanished
        elif pf.get("state") != "acknowledged":
            forgotten += 1
        else:
            e = {"id": pid, "last_seen": prev.get("run_at")}
            e.update({k: pf[k] for k in CARRY if pf.get(k) not in (None, "")})
            # The note link, the citation and the name go too: the first can
            # match the entry back, and the other two prove (or refuse) its id
            # when a law comes to sit under the same base id.
            for k in ("note_url", "citation", "name"):
                if isinstance(pf.get(k), str) and pf[k]:
                    e[k] = pf[k]
            vanished.append(e)
    added = {e["id"] for e in vanished}
    for vid, ve in prev_v.items():
        if (vid not in live and vid not in kept and vid not in added
                and not vid.startswith("topic:")):
            vanished.append(dict(ve))
    vanished.sort(key=lambda e: e["id"])

    lint = {"run_at": a.run_at, "tool": a.tool}
    if a.summary:
        lint["summary"] = a.summary
    lint["findings"] = out_f
    if prev.get("work_items") is not None:
        # Each id the second match moved is rewritten to the new one, so no
        # work item cites an id the manifest no longer holds.
        lint["work_items"] = follow(prev["work_items"],
                                    {old: new for new, old in moved.items()})
    if vanished:
        lint["vanished"] = vanished

    body = []
    emit_map({"lint": lint}, 0, body, ("lint",))
    head, tail = split(text)
    head = head.rstrip("\n")
    doc_out = (head + "\n\n" if head else "") + "\n".join(body) + "\n"
    if tail.strip():
        doc_out += "\n" + tail.strip("\n") + "\n"
    if not a.dry_run:
        # The temp is created exclusively, under a name nobody can predict. A
        # fixed name let a repository commit a symlink there, and
        # opening it for writing overwrote whatever file it pointed at.
        tmp = None
        try:
            try:
                mode = os.stat(a.output).st_mode & 0o777
            except FileNotFoundError:
                mask = os.umask(0)
                os.umask(mask)
                mode = 0o666 & ~mask
            fd, tmp = tempfile.mkstemp(
                dir=os.path.dirname(os.path.abspath(a.output)),
                prefix="." + os.path.basename(a.output) + ".", suffix=".lexlint-tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(doc_out)
            os.chmod(tmp, mode)
            os.replace(tmp, a.output)
        except (OSError, ValueError) as exc:
            # ValueError covers UnicodeEncodeError: a lone surrogate is valid
            # in JSON and cannot be written as UTF-8. Either way the temp
            # file goes, so nothing is left beside the manifest.
            if tmp and os.path.lexists(tmp):
                os.remove(tmp)
            if isinstance(exc, ValueError):
                die(f"the merged manifest cannot be written as UTF-8 ({exc}); a "
                    f"finding in the run carries a character that is not text, "
                    f"so {a.output} was left as it was", EXIT_MANIFEST)
            die(f"cannot write {a.output}: {exc}", EXIT_MANIFEST)

    # A finding about one place has the id `<declared slug>:<key>`, keyed on
    # the slug as the worker validated the declaration, and a slug holds no
    # colon: the id's first segment IS the slug that was DECLARED. Its
    # `jurisdiction` is the slug the law was READ FROM, which is another place
    # in two cases: a parent whose law reaches the declared one (and then
    # `resolved_from` repeats the declared slug), and the held place an alias
    # names (its Atlas path, its URN, a renamed law slug's old spelling),
    # which carries no `resolved_from` at all. Either way the finding mirrors
    # the same key under the slug that answered it -- an exact id match, never
    # a citation guess, and the only match that also folds a citation-less
    # coverage pair (a state and a city both reporting "not shown" carry no
    # citation to group on, and a join keyed on citation cannot see them).
    def declared(f):
        fid = f.get("id")
        if not (isinstance(fid, str) and ":" in fid and isinstance(f.get("jurisdiction"), str)):
            return None                       # activity: and derived: are about no place
        return fid.split(":", 1)[0] or None
    by_id = {f["id"]: f for f in out_f if isinstance(f.get("id"), str)}
    elected = {}
    mirrors = 0
    for f in out_f:
        fid = f.get("id")
        answered_by = f.get("jurisdiction")
        rf = declared(f)
        if not (rf and answered_by and answered_by != rf):
            continue
        parent_id = answered_by + ":" + fid[len(rf) + 1:]
        parent = by_id.get(parent_id)
        if parent is None:
            # No entry for the parent in this run: the first sibling to reach
            # it stands for the law, and later siblings mirror THAT one, so
            # two cities sharing one absent parent count as one mirror, never
            # zero and never two.
            head = elected.get(parent_id)
            if head is None:
                elected[parent_id] = f
                continue
            parent = head
        if (f.get("citation") or "").strip() == (parent.get("citation") or "").strip():
            mirrors += 1

    # A declared jurisdiction came back when a call echoed it or a finding is
    # keyed on it. The profile may spell it any way the schema allows, so it is
    # compared as the worker's validateSlug writes it; the worker's ISO
    # crosswalk (a territory's own code, a changed one) is the server's alone,
    # so such a code in a hand-edited profile still reads as not linted. The
    # profile set_profile writes always holds the slug.
    def spelled(j):
        if not isinstance(j, str):
            return None
        s = re.sub(r"^(urn:(?:via|ungovr):|https?://(www\.)?(ungovr\.org|lexlint\.io/law)/)", "",
                   j.strip().translate(ASCII_LOWER)).strip("/")
        return re.sub(r"^([a-z]{2})-([a-z0-9]{1,3})$", r"\1/\2", s)
    seen = ran | {declared(f) for f in out_f}
    # "N kept under a new id": present only when N is not zero, so a merge
    # where no id moved prints the counts it always did. These entries are
    # also in triage_carried or triage_restored when they held triage.
    moved_count = {"kept_under_a_new_id": len(moved)} if moved else {}
    json.dump({
        **moved_count,
        "calls": calls, "corpus_built_at": corpus, "findings": len(out_f),
        "distinct_instruments": len(out_f) - mirrors, "mirrors": mirrors,
        "triage_carried": carried, "triage_restored": restored,
        "first_seen": first, "vanished_added": len(added),
        "vanished_total": len(vanished), "topic_notices_dropped": topics,
        "unacknowledged_gone": forgotten,
        "finding_fields_this_bundle_does_not_know": sorted(unknown),
        "activities_unlinted": sorted(i for i in live if i.startswith("activity:")),
        "activity_findings_intersected_away": act_gone,
        "work_items": len(lint.get("work_items") or []),
        "jurisdictions_missing": [j for j in doc["profile"].get("jurisdictions") or []
                                  if spelled(j) not in seen - {None}],
        "output": None if a.dry_run else a.output,
        "dry_run": a.dry_run,
    }, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return EXIT_OK

if __name__ == "__main__":
    sys.exit(main())
