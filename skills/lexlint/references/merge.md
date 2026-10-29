<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# Step 4 in detail: merge the findings into the manifest

**A missing `lint:` block is not proof there was no previous run.** A manifest
gets rewritten between runs, by hand or by an older tool, and a rewrite that
drops the block deletes triage the developer did rather than output the run
produced. The manifest is committed, so the previous block is one command
away:

```
git show HEAD:lexlint.yml
```

Recover `work_items` and the four per-finding fields from there, carry them
forward as below, and say in the report that you did and where they came from.
If the file is not tracked, or the last commit holds no `lint:` block either,
say that too and start clean. An acknowledgment nobody can find is not one to
invent.

**That command assumes a git repository and a way to run it, and neither is
guaranteed.** Where you cannot run it, say the previous block could not be
recovered and treat the triage as unknown rather than absent. The two are not
the same thing to report: absent invites starting clean, unknown says a
developer may have work here that this run cannot see.

**A child jurisdiction that answered from a parent mirrors the parent's
findings, and both sets arrive.** Declare `us/ca` and `us/ca/santa-barbara`
and the city's findings are the state's a second time under city ids, because
`id` is keyed on the slug that was declared while the answer came from one
rung up. Two fields say which slug is which, and they are easy to read the
wrong way round. **`jurisdiction` names the slug the law was read from**, so
on the city's findings it is `us/ca`. **`resolved_from` names the slug that
was declared**, here `us/ca/santa-barbara`, and it is present only on a
finding a parent answered for: a finding read where it was declared carries
none. (`resolved_from_parent` in the coverage preview is the other way round
and names the parent, so do not read one as the other.) This is the
declaration reported as it was made rather than a duplicate to clean up, and
both entries stay in the manifest: the developer declared the city, and the
record should say what the city returned.

Three rules stop the mirror from inflating everything downstream:

- **A finding carrying `resolved_from` mirrors the entry with the same
  instrument key under the slug `jurisdiction` names, kept only when the two
  share a citation.** `id` is `<declared slug>:<instrument key>`, so the
  mirror's own instrument key, read off its id, is the same key the parent
  carries under the answering slug: an exact id match, never a citation
  guess, and never a fuzzy read of the summary. This is also the only match
  that folds a citation-less coverage pair (a state and its city both
  reporting "not shown" cite nothing to group on). **When the answering slug
  was not itself declared, there is no parent entry to match against**: two
  cities of one undeclared state still mirror each other, but the first one
  read stands for the law and the rest mirror that one, so the pair counts
  as one mirror, never zero and never two.
- **Report distinct instruments, with the mirror count beside it**, never a
  bare total: "57 findings, 40 distinct instruments; the 17 under
  `us/ca/santa-barbara` are the `us/ca` ones again, which is where that city
  answered from." A bare 57 tells the developer they face more law than they
  do.
- **One obligation, one work item.** A mirror and its parent share a
  `handled_by`. Two rows for one duty quietly rebuilds the per-jurisdiction
  list step 5 exists to collapse.

**A mirror is not interchangeable with its parent, though**, and this is the
case to expect: triage is carried per finding id and the ids differ, so a
parent holding the last run's `state: acknowledged`, `where` and `note` has a
mirror that is correctly `state: new` with none of them. Carry the four fields
by id exactly as below, and never copy a parent's triage onto its mirror to
make the two look alike. The developer acknowledged one entry, not two.

For every finding in the new run:

- If its `id` appeared in the previous run, **carry `state`, `where`, `note`
  and `handled_by` across verbatim** and refresh everything else from the run.
  `handled_by` is a triage decision, not a fact about the law, so the run has
  no opinion about it and must not clear it.
- If its `id` is new, set `state: new`.
- A finding whose `id` begins `topic:` is a **tool-coverage notice** from an
  older LexLint, not a finding about this app. It said LexLint held law on a
  topic `run_lint` could not evaluate. Every topic in the law library is evaluated
  now, so no run raises one any more, and a manifest written before that can
  still be carrying one. If your previous manifest has a `topic:` entry and this
  run does not, that is what happened: **drop the entry** rather than moving it
  to `lint.vanished`, and expect real findings on that topic in its place. It
  never had a `handled_by` or a work item, so there is nothing to reassign.

For every acknowledged finding whose `id` did **not** appear in the new run, a
`topic:` notice excepted as above, move the entry to `lint.vanished` with a
`last_seen` date and tell the developer. Do not delete it. The instrument may
have been repealed, or its citation may have been edited upstream so the
derived id moved. Those have opposite implications and the lint cannot tell
them apart.

**A vanished finding that comes back brings its triage with it.** Read the four
fields off the `lint.vanished` entry exactly as you would off a finding, and
take the entry out of `vanished`. An id that reappears is usually a citation
that moved and moved back, or an instrument restored, and either way the
acknowledgment is about the same duty it was always about. Asking the developer
to make it again because the id took a round trip is the same silent deletion
in slower motion. This is why a vanished entry carries the four fields and why
the schema leaves it open to them: `id` and `last_seen` are what it is *for*,
not all it may hold.

`state` has exactly two values, `new` and `acknowledged`. There is deliberately
no `resolved`, `fixed`, `waived`, or `ignored`. An obligation applies whether or
not you have met it, so a finding never goes away. `acknowledged` means "we have
seen this and here is where we handled it", which is true and stays true.

**Everything above is a join, and a join is the wrong thing to spend your own
output on.** A three-jurisdiction run wrote a 110 KB `lexlint.yml`, every byte
of it through the model. That is larger than the upload payload, and output
tokens are the expensive kind. None of it is authored prose: `lint.findings`
is the `run_lint` response reshaped into YAML with four fields carried across
by id, which is a join and a format conversion, and both are things a script
does better than you do.

**With `python3` and PyYAML, do it on disk.** This skill ships the script
that applies every rule in this step, `scripts/merge.py`, under the directory
that holds this skill's `SKILL.md`. It reads the run out of the files step 3
left on disk, reads the previous triage out of the manifest, rewrites **only**
the `lint:` block, and prints the numbers your report needs so that counting
them never costs you a finding read into context. Run it by its installed
path, from the repository root, so `lexlint.yml` and the run files resolve
where they are. **Never into the repository**: do not copy it into the
working tree you are about to ask the developer to commit.

No client sets `SKILL_DIR` for you, so set it first, to the base directory
your client named when it loaded this skill (`references/clients.md` says
where yours names it). Left unset, the path below becomes `/scripts/merge.py`,
python3 cannot open it and exits 2, and that reads like a flag missing. Then
run it against the manifest in place:

```bash
SKILL_DIR='<the base directory your client named for this skill>'
python3 "$SKILL_DIR/scripts/merge.py" lint.json --manifest lexlint.yml -o lexlint.yml \
    --run-at 2026-09-10 --tool 'lexlint 1.63.0' \
    --summary 'Six findings, five instruments, across three jurisdictions.'
```

Where `python3` has no PyYAML, `uv run "$SKILL_DIR/scripts/merge.py"` with the
same arguments fetches it for that one run, because the script declares its
own dependency in its header. `python3 "$SKILL_DIR/scripts/merge.py" --help`
lists every flag.

**If `scripts/merge.py` is not on disk beside `SKILL.md`**, because your
client handed you the skill's text without its files, fetch the published
bundle's `AGENTS.md` from https://github.com/ungovr/lexlint/blob/main/AGENTS.md
and write its one Python block to `merge.py` inside a new private directory
from `mktemp -d "${TMPDIR:-/tmp}/lexlint.XXXXXX"`, never a fixed name in a
shared directory. **Check its version before you run it.** That page follows
the newest bundle, not this one, and the block's `--tool` examples name the
bundle it belongs to: they must read `lexlint 1.63.0`, this skill's own.
Then it is the same script, byte for byte, and a test holds the two together;
run it with the same arguments, then delete the directory. If they name any
other version, do not run it: delete the directory, write the block by hand as
below, and
tell the developer that the plugin has a newer version to update to.
Never retype it from memory: a script rebuilt from recall is a program nobody
tested, run against the developer's triage.

**One file per `run_lint` call, and hand it every one of them.** A split run
(step 3) is several calls, and the intersection rule that makes it safe cannot
be applied to a union that has already happened: pass `lint-1.json
lint-2.json lint-3.json` and let the script intersect. Handing it a
pre-unioned file is not a smaller version of the same thing, it is the run
with a coverage warning in it that the declaration as a whole does not have.

Four flags carry the run's own facts, because a script must not read them off
a clock or invent them: `--run-at` is today's date, `--tool` is your own
`lexlint 1.63.0`, and `--summary` is the one sentence you author.
`--previous <path>` takes the triage from somewhere other than the manifest,
which is the recovery above written to a file: make a private directory with
`mktemp -d "${TMPDIR:-/tmp}/lexlint.XXXXXX"`, write `git show
HEAD:lexlint.yml` into `previous.yml` inside it, pass that full path, and
remove the directory once the merge is done.

`--dry-run` does the whole merge and prints the same counts but writes
nothing, so a merge you are unsure of can be read before it touches the
manifest. Its stdout is only ever that one JSON object, and every diagnostic
goes to stderr. When it stops, the exit code says why: 3 for a run file that
is not there or a run with no findings, 4 for a manifest it cannot read or
write, 5 for a run file of the wrong shape, and 2 for a flag missing. `--help`
lists them.

**It stops rather than guesses, in three places**, each of them a way the
merge could otherwise delete triage without saying so:

- The calls disagree about `corpus_built_at`. That is the rebuild straddle
  from step 3, and the answer is to run again, not to merge.
- The run has no findings at all. A manifest holding acknowledgments is not
  overwritten with an empty block on a response that may simply have failed.
  `--allow-empty` says you looked and the run is genuinely empty.
- The manifest has no `profile`, so it is not a manifest.

**Read the JSON summary it prints, and put its numbers in the report.** They
are the ones step 7 asks for and the ones that make a mishandled merge visible
the same day: `findings` and `distinct_instruments` with `mirrors` between
them, `triage_carried` and `triage_restored`, `vanished_added` and
`vanished_total`, `topic_notices_dropped`, `activity_findings_intersected_away`
for a split run, and `jurisdictions_missing`, which answers step 3's closing
question about a declared slug that never came back. A slug counts as having
come back when any finding names it in `resolved_from`, or in `jurisdiction`
with no `resolved_from` beside it, so a city that answered from its state is
not listed: it was linted, one rung up. A `triage_carried` of 0
against a manifest that had acknowledgments is the failure this whole section
is written against, and it is a number rather than a silence.

`finding_fields_this_bundle_does_not_know` is the one to read even when it is
the only thing that changed. A name in it means the law library is ahead of your
installed schema, which is the ordinary shape of an additive change and not a
fault: say which fields were left out. Say that an update picks them up only
when the preflight reported one (`update_available: true`), and pair the two
notices then. When the preflight said this bundle is current, say that
instead: the field is newer than any published bundle, no command the
developer can run will bring it in, and promising that one will sends them
after an update that changes nothing.

**Without `python3` and PyYAML, write the block yourself**, to the same rules,
which the script only mechanises. They fix the shape completely, and following
them gets you the same bytes:

- Two-space indent, block style throughout, one item per line, no wrapping and
  no flow style. A list item's first key sits on its `-`.
- **Every string value is single-quoted**, with an interior `'` doubled. Yes,
  including `state: 'new'`. Uniform quoting is what stops YAML from reading
  the Norway slug `no` as boolean false, and it means no value ever needs the
  judgment call.
- A string containing a newline or a control character is double-quoted on one
  line instead, with `\n`, `\r`, `\t` and `\xNN` escapes, because a
  single-quoted scalar folds newlines into spaces and would lose them. A
  control character here is any of U+0000 to U+001F and U+007F to U+009F;
  U+2028, U+2029, U+FFFE and U+FFFF count too, escaped as `\uNNNN`. Raw, the
  first range and the last two make the whole file unreadable to PyYAML.
- A key is written bare when it starts with an ASCII letter or `_`, holds
  only ASCII letters, digits and `_ . / -`, and is not `true`, `false`, `yes`, `no`,
  `on`, `off` or `null` in any case. Any other key is quoted the way a value
  is, so a key can never start a line of its own.
- `null`, `true`, `false` and numbers are bare. An empty list is `[]` and an
  empty mapping is `{}`.
- Keys go in the order `lexlint.schema.json` declares them, for the four
  mappings it names: the `lint:` block, a finding, a work item and a vanished
  entry. Every other mapping, a finding's own `matched_by` or `posture`
  included, is sorted, and a key the schema does not name goes after the ones
  it does.
- **On a finding, a key the schema does not name is left out**, and named in
  the report instead. `finding` is `additionalProperties: false`, so writing
  one through lands a manifest that fails the schema this bundle ships with,
  on the lint's own output, where the developer cannot fix it. Your schema is
  frozen at install and the law library is not, so this is the ordinary way a
  newer field arrives: say which fields you left out, say that upgrading
  picks them up on the next run only where the preflight reported a newer
  version, and do not invent a place to keep them.
- `lint.vanished` is sorted by `id`. Findings stay in the order the run
  returned them.

**And leave everything outside the `lint:` block exactly as you found it**,
byte for byte, comments included. `version`, `app` and `profile` are the
developer's declaration, and a footer under the `lint:` block is theirs too:
`lint:` is the last top-level key the schema allows, so anything trailing it
is a comment somebody wrote, never leftover output. The script splices for
that reason rather than reformatting.

**Inside the block, a comment does not survive**, at any indent, because the
block is regenerated from the run every time rather than edited in place.
That is equally true of writing it by hand and is not new here, but it is
worth saying once: a note that has to last belongs above `lint:`, or in
`note` on the finding it is about, which is a field and does survive.


**Then commit the manifest.** Everything above rests on it: the committed file
is what the next run diffs against, what carries this triage into the next
session, and what turns a change in the law into a diff a reviewer can read. A
manifest left sitting in the working tree is none of those, and it is the
ordinary way a session's triage gets lost. So write it, then commit it, on its
own, with a message that names the run:

```
lexlint: 40 instruments across 3 jurisdictions, 9 work items
```

That commit is the manifest and nothing else. The lanes' own diffs and drafts
are separate commits in step 6, because a reviewer asking what changed in the
law should not be reading a feature at the same time.

**Where that commit goes next is the repository's business, not LexLint's.**
Do not push it, do not open a pull request, and do not merge anything: branch
rules, review gates and release process belong to whoever owns the repo, and a
lint that pushes to satisfy its own design is doing something nobody asked it
for. If the repository's contribution rules mean you cannot commit at all,
follow them, leave the file written, and say in the report that the manifest is
uncommitted and why. The same goes for having no way to run git at all. Be
accurate about what that costs, because it is less than it sounds: the next run
reads `lexlint.yml` off disk whether or not it was committed, so the triage is
not lost. What is lost is the recovery route above, and the diff a reviewer
reads when the law changes. An uncommitted manifest that the report names is a
result; one nobody mentions is how the next run starts from nothing.
