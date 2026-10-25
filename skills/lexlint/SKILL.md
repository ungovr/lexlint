---
name: lexlint
description: Use this skill first, before reading or editing code, whenever a request would add or change what an app does with people, their data, or other sites, even if it never mentions law or compliance. That covers code that collects or stores personal data or device identifiers, sends people automated email or messages, adds a chatbot or other generative AI feature, trains or tunes a model on user data, crawls or scrapes other sites, records or transcribes voices or captures faces, or lets software make decisions about people such as employment, credit or eligibility. It returns cited findings on the AI, scraping, privacy, cybersecurity, communications, content-moderation, product-liability, age-gating, and reuse law of the jurisdictions the app operates in. Not for questions about what a particular law says, edits to legal documents, styling, tests, renames, hardening, or bug fixes that change no data use.
license: MIT
compatibility: Needs network access to https://mcp.lexlint.io and python3 with PyYAML for the merge step.
metadata:
  version: "1.59.0"
  publisher: UnGovr
  homepage: https://lexlint.io
---

<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# LexLint

A lint for AI, scraping, privacy, cybersecurity, communications, content-moderation, product-liability, age-gating, and reuse law,
backed by the LexLint law library, researched jurisdiction by jurisdiction. Like a code linter, it catches basic
issues early, it certifies nothing, and it replaces neither QA nor legal review.

**LexLint does not read your code to work out what your app does.** You declare
that, in a committed `lexlint.yml`, and the declaration is what gets linted.
Manifest-first, not detection-first: a guessed declaration produces a
confidently wrong lint, and a committed one produces a diff a reviewer can read
when the law changes underneath it.

Once the declaration is written down, which law applies is decided by a
fixed, rule-based match against the law library, never by asking the
LLM to reason about the law itself: the same declaration, the same snapshot
of the law library, and the same judging instant always produce the same
findings. A finding's kind, severity, staleness and certainty rung move with
the clock as well as with the law library, so a run repeated later against an
unchanged law library can still answer differently.

## Setup

The tools need an UnGovr Open Data API key, passed as `X-API-Key` and read from
`UNGOVR_API_KEY`. If the developer has no key, do not describe the problem and
stop.

**"No key" is two different states, and getting a key fixes only one of
them.** The preflight below reports `key_present: false` when no key exists,
and reports exactly the same thing when a key is saved on this machine and did
not reach the server. Look before you offer either route: "When the preflight
says there is no key", below (its file is named further down), is one command, and it comes first.

**The lint is advisory and never blocks the work.** If the developer declines a
key, the sign-in, or the lint itself, say in one line that the lint was offered
and declined, then go back to the request that brought you here and do it.

**There are two routes to a key and the developer picks, so ask BEFORE you
start either one.** Neither is a fallback for the other. One needs an account,
which is free; the other needs none: `claim_trial_key`, called from this
session, mints a 30-day key good for 50 requests over its whole life and
returns it in the result. Say that an account key is the one without an expiry
or a lifetime total, and say that a trial key will be recorded in this
session's transcript. Then run only the route they chose. Never run
`claim_trial_key` because no key was found, and never run it twice.

**Twice includes a key you cannot see from here.** Do not run
`claim_trial_key` when the look below found a key on disk, when a key was
minted earlier in this conversation, or when your own memory or notes for this
machine record one. The one exception is a developer who, told that a first
key exists, asks for a new key in so many words. A needless mint is not free
to them: it spends one of the limited trial mints their address gets each
day, and it leaves the earlier key stranded, still valid and saved somewhere
nothing reads.

`check_access` reports which routes this deployment actually offers in
`setup.steps`; read them from the response rather than from memory, because a
deployment that cannot mint a trial names only the account route and offering
the other one there sends the developer to a dead end.

If they choose the account route:
run the key flow: hand over

https://ungovr.org/cli-login?client=lexlint

ask them to sign in, copy the key and paste it back, then persist it and tell
them to restart. Signing in lands them on the page that mints, beside a Copy
Key button. The value is read at process start, so a key set inside a running
session is read by nothing, which is why the restart is a step rather than a
footnote.

The whole key flow, with the check before the key is saved and where it is
saved, is a skill of its own: read `../lexlint-key/SKILL.md` to run it.

Where the key persists, the command that persists it when your client has one,
and how to restart all differ by client, and no command from another client's
entry is worth offering: it is a dead end at the moment the developer is
already stuck.
Read `references/clients.md` before any install, key, update, restart or
sign-in step, or to scope one run by path, to find your own client.

**Run `check_access` before anything else**, pass `client_version: "1.59.0"`.
Do not pass `jurisdictions`, even on a re-run whose manifest already declares
them: `check_access` spends this one request either way, and `set_profile`
answers the same coverage question later, off its own separate request, so that
is the one place to read it. Show the developer the result as one line:

```
lexlint 1.59.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
```

**That version string is yours and it is `1.59.0`.** State it, do not go looking
for it: it is checked against the bundle's own `plugin.json` before this file
ships, and a version read out of a file at runtime is a version that can be
read from the wrong tree.

Pass the same `client_version` on every `run_lint` call. A run that skips the
preflight still deserves to learn a newer plugin exists, and the server can
only compare a version it was sent.

If `key_present` is false, stop, and read the next section (the file named next) before you say
anything about keys. Do not ask what the app does first: they cannot act on
the answer.

Read `references/no-key.md` when `key_present` is false.

Read `references/signed-in.md` when `credential` is `"none"`.

Read `references/unreachable.md` when `check_access`, or any call after it,
fails to answer.

Read `references/update.md` when the response names a newer version.

Read `references/untested-model.md` when `model_notice` is present.

Every response that reports a key problem carries a `setup` object with the
URL and the steps in it, and every tool's error carries the same thing under
`error.data.setup`. Walk those steps. `setup.reason` distinguishes the two
cases and they differ on one point that matters: `missing` means use an
existing key if there is one, because minting revokes it, while `rejected`
means mint. `setup` is null on a healthy call and on an upstream outage, so a
null there is not a key problem to go looking for.

If `key_valid` is true and `quota_remaining` is 0, the key WORKS and today's
free allowance is spent. Say when it returns. **Do not suggest minting a new
key**: minting silently revokes the one they hold.

If `key_valid` is null, LexLint learned nothing about the key: the Open Data
API did not answer. Report it as our outage, not their setup, and again **do
not suggest minting**. Only `key_valid: false` means the key was actually
rejected, and that is the one case where minting belongs: run the key flow
above and follow the `rejected` steps.

`corpus_reachable` is three-valued for the same reason: true when the law
library was read, false when the read failed, and null when it was never attempted.
Never render null as "unreachable".

LexLint stores no keys. Every call checks yours and spends from its
allowance, the same one it has on the UnGovr Open Data API, and that
allowance is the only meter. `check_access`,
`set_profile`, and `run_lint` together cost five upstream requests, however
many jurisdictions are declared: one for the preflight, one for `set_profile`,
and three for `run_lint`'s reads of the bulk export, which are filtered to
your declaration in memory rather than fetched per jurisdiction.
`check_access`'s own coverage preview rides the preflight's one request
either way; `set_profile` answers the identical question off its own separate
request, so asking both is redundant, not costlier, and neither order saves
anything. That five does not cover step 2 of the loop below: resolving a
domain the app talks to costs one to four more requests per domain not
already recorded in `profile.domains`, so a run that resolves several domains
costs more than five.

## Gotchas

Each of these is stated in full where it applies, and each has to be known
before its situation arises.

- **"No key" is two different states.** A key saved on this machine that did
  not reach the server also reads as `key_present: false`, so look on disk
  before offering a route, and never run `claim_trial_key` because no key was
  found.
- **`state` has exactly two values, `new` and `acknowledged`.** There is
  deliberately no `resolved`, `fixed`, `waived`, or `ignored`: an obligation
  applies whether or not you have met it, so a finding never goes away.
- **Unlinted is not clean.** A jurisdiction LexLint has no data for is a
  warning, never a silent pass, and every report says what the run did not
  reach.
- **A drafted artifact is not legal advice.** Every doc-lane draft says so in
  its header, and says that its existence discharges nothing.
- **A cell never carries an unbounded list.** Show three items and a count,
  and name the full set in a line under the table.
- **A truncated tool result is not the run.** Never report the findings at
  the top of a cut response as the whole lint: step 3 gives three routes to
  the whole response.
- **Write nothing into the repository but the manifest.** The run's JSON, the
  upload preview and a report of your own go under `/tmp` or your client's
  scratch space. The exceptions are step 6's doc and counsel artifacts and the
  `.lexlint/` cache.
- **Manifest-first, never inferred from code.** Read the code to build the
  candidate and its evidence, never to declare on the developer's behalf:
  nothing unconfirmed is ever sent.

## The loop

Read `references/cheaper-tools.md` before step 2, once per run.

Read `references/cache.md` the first time a `get_law` is about to be fetched.

### How to show a list

Five of the things below are lists with a repeating shape: the declaration
candidates in step 1, the coverage preview, the triage plan, the counsel list,
the instruments table in a brief for counsel. **Show each of those as a markdown
table**, the way the examples do. Every surface that runs LexLint renders GFM
tables, and a fenced code block is the one construct none of them prettifies:
fencing a table opts out of the rendering on purpose, for no gain.

Five rules keep the tables readable, and the last one is about the reader
rather than the layout:

- **Three or four columns, never more.** A terminal is roughly 80 to 100
  columns wide, and a six-column table with a citation in it wraps into mush.
  If a fifth column is tempting, the row is really two rows, or the column
  belongs in `lexlint.yml` rather than on screen.
- **A cell never carries an unbounded list.** Bounding the columns bounds
  nothing if one cell can eat the terminal by itself. When a cell would hold
  more than three items, show three and a count, European Union, Germany,
  France +17 more, and name the full set in a line under the table, where a
  wrap costs nothing.
- **The citation goes last**, because it is the widest cell and the only one
  that can be allowed to wrap.
- **Keep the fences where they belong.** An install or update command, the
  `.lexlint/` tree, and the JSON cache envelope are all things to copy verbatim
  rather than read. Those stay fenced. The status line stays fenced too: it is
  one line, not a list.
- **The summary is for the developer; the citation is for the lawyer.** A
  finding carries both because it has two readers, and every list keeps
  both where the finding has both: never drop the citation to save width,
  and never drop the summary to look precise. The developer acts on the
  sentence; the lawyer checks the citation, exactly as the lint gave it.

Two more rules are about the words in the cells rather than the layout:

- **A jurisdiction is shown by name, never by slug.** Every finding carries
  `jurisdiction_name`: "Ireland", "European Union", "US-California". That
  is the word in every table and every sentence; the slug (`us/ca`) belongs in
  `lexlint.yml` and nowhere a person reads. A finding without a name (a slug
  the law library does not name) shows its slug, which is the gap it marks.
- **The flag goes before the name.** A finding or coverage row that carries
  `jurisdiction_flag` gets it, then a space, before the name in every table
  and list: "🇪🇺 European Union", "🇮🇪 Ireland". Only a country, the EU and
  the UN have one. A state or city's name opens with its country's code
  instead, "US-California", which is as wide as a flag and its space, so the
  names still line up. Never borrow its country's flag, and never draw a flag
  the lint did not send.
- **`summary` is one sentence; the paragraph is `detail`.** The lint writes
  the instrument's name, a colon, and one sentence, and puts the whole
  research summary in `detail`. Show the sentence in every list. Read
  `detail` before acting on a warn, and show it when the developer asks for
  a finding, never in place of the sentence.
- **`why` comes before the law.** Every instrument finding carries `why`, one
  sentence in basic language saying which declared activity reached it and
  what the law library tags it for ("Pulled in because the app records and
  processes voices, and the law library tags this instrument for exactly
  that.").
  Wherever a finding is shown on its own (a triage entry, a work item's
  findings, a brief for counsel), that sentence goes first, above `summary`,
  so the reader knows why before they meet the statute. In a table it is the
  line under the row, never a fifth column.

**When a law binds is always the finding's `in_force.words`**, verbatim:
"in force since 2018-05-25", "not yet in force, from 2027-12-02, in 15
months", "blocked by a court", "no longer in force, repealed". In a table,
bold the words when `in_force.state` is `not_yet_in_force`, and strike the
date of an ended law, keeping its reason: `~~in force since 2024-02-01~~
repealed`, from `in_force.from` and `in_force.reason`. An ended law with no
`from` prints its words as they are. Never print `status` or
`lifecycle.label` for this: they are the law library's and the older band's
words, and a developer reads the same law at https://lexlint.io/law in
these.

### 1. Read or create `lexlint.yml`

If the repo has one, read it. If not, work the declaration out **with** the
developer, never for them and never without them: read the code, build a
candidate for each of the two lists below, show the candidates, and ask the
developer to confirm or correct them. **Nothing unconfirmed is ever sent.**

**A path given with the request is the manifest or the scope, read off the
path itself**, and your client's entry in Client setup says how to pass one.
One that ends `.yml` or `.yaml` is the manifest to use instead of the
repo-root one, and anything else is the scope for this run, narrowing which
files you read to that subtree under the same rules as `app.scope`. Both at
once is two arguments, manifest first. A path that is neither an existing file
nor an existing directory is a typo worth stopping on, because the alternative
is linting the whole repository while reporting a scope. A scope from the
request is not written to the manifest: say in the report that it came from
the request, and what it was.

Read `references/declaration.md` when there is no manifest, when the manifest
is missing an answer, or when the run is scoped.

### 2. Resolve any domains the app talks to

```
resolve_domain_jurisdiction(domain="stadt-koeln.de")
-> { domain: "stadt-koeln.de", jurisdiction: "de" }
```

Record the result in `profile.domains`. The response also names the method it
used, and the methods are not equally good: a mapping to a known operator is
evidence, while a fallback inference from the country code is a guess wearing a
label. A `null` result is not permission to guess either: a vanity TLD says
nothing about who operates the site. Check the operator's terms page, find the
establishment, and declare what you found.

This is the one step whose cost scales: each domain not already recorded in
`profile.domains` takes one to four upstream requests to resolve. Count the
unrecorded domains against the quota line the preflight showed before
resolving them, because an app that talks to many domains can spend the day's
budget here before the lint itself runs. If the list is longer than the quota
comfortably covers, resolve the domains the app actually fetches or writes to
first, tell the developer which ones wait for tomorrow's allowance, and record
the deferral rather than guessing a jurisdiction to fill the gap.

### 3. Set the profile, then run the lint

Two calls. The first validates the declaration and tells you what the law
library holds for it; the second returns findings.

Read `references/run.md` at step 3.

### 4. Merge the findings into the manifest

Rewrite only the `lint:` block. Never touch `version`, `app`, or `profile`:
those are the developer's declaration, not yours. The one exception is step 3's
`public_sector`, `regulated_sector`, `roles` and `flows` answers, which you
write into `profile` because the developer gave them to you. And **carry
`lint.work_items` across untouched** if it is there: it is the plan the
developer approved in the last run's triage, the run does not produce it, and a
rewrite that drops it deletes their work silently. A work item whose findings
have all vanished stays: deciding it is finished is the developer's call.

Read `references/merge.md` at step 4.

### 5. Triage: turn findings into a short plan

**First, separate what binds this app from what does not.** One field on the
finding answers most of it, and reading the statute yourself answers none of
it.

Read `references/triage.md` at step 5, and again for the lanes of step 6.

Read `references/severity.md` at step 5, or when a finding's severity is
questioned.

### 6. Work the lanes

Every lane sets `state: acknowledged`. There is no `resolved`.

### 7. Report only what the lint can claim

**A report requires a run.** Everything below is about findings the server
actually sent. If the calls in step 3 never returned a payload, there is no
report to write: see "When you cannot reach the server" in Setup (its file is named there), which is
where that case is answered in full.

The passing state is **"no basic issues found"**. Never restate it as clearance,
certification, or a clean bill of health, and never suppress a coverage warning
to make a summary look tidier. A jurisdiction LexLint has no data for is a
warning, never a silent pass, and unlinted is not the same as clean.

Read `references/report.md` at step 7.

Read `../lexlint-upload/SKILL.md`, a skill of its own, when the run closes
with its upload at step 7 or the developer asks to upload a run, and
`../lexlint-feedback/SKILL.md` when that upload is declined or the developer
asks to send feedback.

## What this is not

LexLint is a research summary, not legal advice, and not authorization to access
any system. It does not certify anything. A clean run means the basics were
checked against the data LexLint holds today, in the jurisdictions you declared,
for the activities you declared. It does not mean you are in the clear.

Full documentation: https://mcp.lexlint.io/

A worked example, end to end: https://mcp.lexlint.io/example
