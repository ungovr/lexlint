# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Merge a LexLint run into lexlint.yml. Needs python3 with PyYAML."""
import argparse
import json
import os
import re
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
id; lint.work_items is kept as it was; an acknowledged finding the run no
longer returns moves to lint.vanished; only the lint: block is rewritten, and
everything above and below it is kept byte for byte. stdout carries exactly
one JSON object of counts for the report; every diagnostic goes to stderr."""

EPILOG = """\
examples:
  one run_lint call, merged into the manifest in place:
    python3 %(prog)s lint.json --manifest lexlint.yml -o lexlint.yml \\
        --run-at 2026-10-22 --tool 'lexlint 1.64.3' \\
        --summary 'Six findings, five instruments, across three jurisdictions.'

  a split run of three calls, counted without writing anything:
    python3 %(prog)s lint-1.json lint-2.json lint-3.json \\
        --manifest lexlint.yml -o lexlint.yml \\
        --run-at 2026-10-22 --tool 'lexlint 1.64.3' --dry-run

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
KEYS = {
    "lint": ("run_at", "tool", "summary", "findings", "work_items", "vanished"),
    "findings": (
        "id", "severity", "kind", "jurisdiction", "jurisdiction_name",
        "jurisdiction_flag", "summary", "name", "detail", "why", "matched_by", "posture", "basis",
        "citation", "url", "note_url", "status", "requires", "applies_to",
        "owed", "requires_elsewhere", "role", "flows", "reading", "customer_duty_id", "instrument_id",
        "capability", "stated_by", "inferred_from", "derived_from", "moments",
        "effective_date", "lifecycle", "in_force", "certainty", "settledness",
        "court_action", "as_of_date",
        "stale", "confidence", "resolved_from") + CARRY,
    "work_items": ("id", "lane", "title", "findings", "jurisdictions"),
    "vanished": ("id", "last_seen") + CARRY,
}

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
    merged, per_call = {}, []
    for p, c in calls:
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
            sorted(set.union(*per_call) - keep), stamps[0], len(calls))

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
                         "lint.tool, such as 'lexlint 1.64.3'")
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

    findings, act_gone, corpus, calls = load_run(a.runs)
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

    out_f, carried, restored, first, unknown = [], 0, 0, 0, set()
    for f in findings:
        # The run has no opinion about the four: drop them, then take the
        # developer's, matched on id and on nothing else. A key the schema
        # does not name is dropped too, and named in the summary: `finding`
        # is closed, so writing it out lands a manifest that fails the schema
        # this bundle ships with.
        new = {k: v for k, v in f.items()
               if k in KEYS["findings"] and k not in CARRY}
        unknown |= set(f) - set(KEYS["findings"])
        was = prev_f.get(f["id"]) or prev_v.get(f["id"])
        new.update({k: was[k] for k in CARRY if was and was.get(k) not in (None, "")})
        new.setdefault("state", "new")
        if not was:
            first += 1
        elif new["state"] == "acknowledged" or any(new.get(k) for k in CARRY[1:]):
            carried += f["id"] in prev_f
            restored += f["id"] not in prev_f
        out_f.append(new)

    live = {f["id"] for f in out_f}
    vanished, topics, forgotten = [], 0, 0
    for pid, pf in prev_f.items():
        if pid in live:
            continue
        if pid.startswith("topic:"):
            topics += 1                       # dropped, never moved to vanished
        elif pf.get("state") != "acknowledged":
            forgotten += 1
        else:
            e = {"id": pid, "last_seen": prev.get("run_at")}
            e.update({k: pf[k] for k in CARRY if pf.get(k) not in (None, "")})
            vanished.append(e)
    added = {e["id"] for e in vanished}
    for vid, ve in prev_v.items():
        if vid not in live and vid not in added and not vid.startswith("topic:"):
            vanished.append(dict(ve))
    vanished.sort(key=lambda e: e["id"])

    lint = {"run_at": a.run_at, "tool": a.tool}
    if a.summary:
        lint["summary"] = a.summary
    lint["findings"] = out_f
    if prev.get("work_items") is not None:
        lint["work_items"] = prev["work_items"]
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

    # `jurisdiction` is the slug a finding was READ FROM. `resolved_from`, set
    # only when a parent answered, is the slug that was DECLARED. A mirror's
    # id is `<declared>:<instrument key>`, so the entry it mirrors is that
    # same key under the slug that answered it -- an exact id match, never a
    # citation guess, and the only match that also folds a citation-less
    # coverage pair (a state and a city both reporting "not shown" carry no
    # citation to group on, and a join keyed on citation cannot see them).
    def declared(f):
        rf = f.get("resolved_from")
        return [rf] if isinstance(rf, str) else list(rf or [f.get("jurisdiction")])
    by_id = {f["id"]: f for f in out_f if isinstance(f.get("id"), str)}
    elected = {}
    mirrors = 0
    for f in out_f:
        fid = f.get("id")
        answered_by = f.get("jurisdiction")
        rf = f.get("resolved_from")
        candidates = [rf] if isinstance(rf, str) else list(rf or [])
        rf = next((c for c in candidates if isinstance(c, str) and c
                   and isinstance(fid, str) and fid.startswith(c + ":")), None)
        if not (rf and isinstance(answered_by, str) and answered_by and answered_by != rf):
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
    seen = {s for f in out_f for s in declared(f)}
    json.dump({
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
                                  if j not in seen],
        "output": None if a.dry_run else a.output,
        "dry_run": a.dry_run,
    }, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return EXIT_OK

if __name__ == "__main__":
    sys.exit(main())
