# LexLint for agents

LexLint is a lint for AI, scraping, and privacy law. Like a code linter, it
catches basic issues early, it certifies nothing, and it replaces neither QA nor
legal review.
This file is the same procedure the `lexlint` skill carries, written for any
agent that reads `AGENTS.md` instead. The tools are served over MCP at
https://mcp.lexlint.org/mcp and the connection details are in `.mcp.json` beside
this file. Follow the loop below in order, and do not paraphrase the reporting
rules in section 7: they are what makes a lint worth trusting.

**LexLint does not read your code to work out what your app does.** You declare
that, in a committed `lexlint.yml`, and the declaration is what gets linted.
Manifest-first, not detection-first: a guessed declaration produces a
confidently wrong lint, and a committed one produces a diff a reviewer can read
when the law changes underneath it.

## Setup

The tools need an UnGovr Open Data API key, passed as `X-API-Key` and read from
`UNGOVR_API_KEY`. If the developer has no key, do not describe the problem and
stop. Run the `/lexlint-key` flow: hand over

https://ungovr.org/settings/api-keys?cli=lexlint

ask them to sign in, copy the key and paste it back, then persist it and tell
them to restart. Signing in lands them on the page that mints, beside a Copy
Key button. The value is read at process start, so a key set inside a running
session is read by nothing, which is why the restart is a step rather than a
footnote.

**Run `check_access` before anything else**, pass `client_version: "1.12.0"`,
and **do not pass `jurisdictions`**: `set_profile` answers coverage off the
same upstream request, so asking here pays twice for one answer. Show the
developer the result as one line:

```
lexlint 1.12.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
```

**That version string is yours and it is `1.12.0`.** State it, do not go looking
for it: it is checked against the bundle's own `plugin.json` before this file
ships, and a version read out of a file at runtime is a version that can be
read from the wrong tree.

Pass the same `client_version` on every `run_lint` call. A run that skips the
preflight still deserves to learn a newer plugin exists, and the server can
only compare a version it was sent.

If `key_present` is false, stop and run the setup flow above. Do not ask what
the app does first: they cannot act on the answer.

### When the response says a newer LexLint exists

An installed plugin is frozen at the version it was installed at. Nothing
updates it on its own, and a developer running a stale one gets today's data
through last month's instructions: the server can hand back a field that the
installed skill has never heard of, and the run quietly does nothing with it.
That has already happened once, which is why `check_access` answers the
question at all.

`update_available` is three-valued, and only `true` is an instruction:

- **`true`**: say so once, plainly, in the run's opening lines, and give the
  command. Do not make it the whole report and do not repeat it: it is a
  footnote to their lint, not the reason they came.

  ```
  lexlint 1.4.0 · a newer LexLint (1.12.0) is available
    claude plugin update lexlint@lexlint     (then restart Claude Code)
  ```

  Two things worth adding when they ask why it did not take: the update only
  loads at session start, and `--scope` defaults to `user`, so a project that
  installed LexLint locally needs
  `claude plugin update lexlint@lexlint --scope local` run from that project's
  directory or it keeps loading the old copy.

- **`false`**: nothing to say. Print the version on the status line and move
  on.
- **`null`**: LexLint learned nothing about your version, which is not the
  same as being current. Say nothing about updates at all: a guess here either
  sends a current developer to run a pointless command or reassures a stale one.

The lint is what they asked for. Run it either way: a stale plugin still lints,
and refusing to work until someone updates would be a worse failure than the
one this exists to catch.

Once the repo has a cache, that same line carries its state: see "Cache what
you fetched".

### When you are not running a model LexLint is tested against

Every `check_access` response also says which models LexLint's procedure is
exercised against. `tested_model_families` holds lowercase family tokens, and
`model_notice` is the sentence to show. The policy comes down; nothing about
your model goes up. LexLint is never told which model you are, and
`check_access` has no argument that could carry it, because the only thing that
knows which model is reading this file is you.

**You know which model you are. Do not go looking for it.** A model id read out
of a config file, an environment variable or a settings dump names whatever that
file says, which is not necessarily the model reading this line.

Lowercase your own model id and test whether it contains any token in
`tested_model_families`. If it does, say nothing. A developer told their setup
is fine learns to skim the preflight, and this is a footnote to their lint
either way.

If it does not, name the model you are and print `model_notice` verbatim, then
ask:

```
LexLint on claude-sonnet-5.

  LexLint's procedure is written and tested against Claude Opus and
  Fable. Other models may follow it less closely, and a lint that
  skips a step is a lint that quietly under-reports.

  Continue on this model, or switch and re-run?
```

Then do what they say. **Continuing is a real answer**, and the lint that
follows is the normal one: this is an advisory rather than a gate, nothing here
can verify a model it was told about, and refusing to work would trade a
possible weakness for a certain failure.

**If there is nobody to ask, print it and lint anyway.** A CI job, a cron run
and a dispatched subagent have no developer in them, and silence must never
resolve to a refusal. The warning belongs in the transcript regardless, where
whoever reads the findings later can see what produced them.

If the fields are absent, say nothing about models at all. An older server does
not answer this, and absent is not the same as unsuitable.

`run_lint` returns the same two fields, for the run that never called the
preflight at all. **Say it once per session**, in the opening lines, exactly as
with a stale version: a warning repeated on every result is one an agent learns
to skip past. If you already showed it at the preflight, the copy on the lint is
the same policy arriving twice, not a second thing to report.

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
rejected, and that is the one case where minting belongs: run `/lexlint-key`
and follow the `rejected` steps.

`corpus_reachable` is three-valued for the same reason: true when the corpus
was read, false when the read failed, and null when it was never attempted.
Never render null as "unreachable".

LexLint stores no keys. Yours is passed through to the UnGovr Open Data API on
every call, and the upstream free tier is the only meter. A whole run costs a
handful of requests regardless of how many jurisdictions are declared: the
preflight, one for `set_profile`, and the lint's own reads of the bulk export.
Declaring more places does not cost more.

## The loop

### 1. Read or create `lexlint.yml`

If the repo has one, read it. If not, ask the developer two questions and write
their answers down.

**What does this app do?** One or more of: `crawls_web`, `trains_models`,
`generates_content`, `deploys_chatbot`, `processes_voice`,
`processes_biometrics`, `automated_outreach`, `high_risk_decisions`.

Read the code to inform your questions, never to answer them on the
developer's behalf. Declaring `trains_models` because you saw a model import,
when the app only calls an API, produces findings for obligations that do not
apply.

**Ask about voices and faces even when nothing here is AI.** `processes_voice`
and `processes_biometrics` reach privacy law rather than AI law, so they attach
to a support line that keeps call recordings or a kiosk that matches a face,
with no model anywhere in the product. Developers routinely leave both
undeclared for that reason. Declared, they return biometric statutes with their
own consent, retention and destruction duties, and in Illinois a private right
of action the person whose voiceprint you took can bring directly.

**Where will it operate?** This question has three plausible readings and
developers pick the wrong one. It is not where the users are, and it is not
where the servers are. **Server location is noise. What matters is the
jurisdiction of each operator whose content or systems the app touches, plus
every jurisdiction the app itself is offered in.** For a crawler, that means
the jurisdiction of each site it fetches, which step 2 resolves.

List every one of them. A jurisdiction left off is not passed, it is unlinted,
and unlinted is not clean.

**Quote every slug.** YAML reads a bare `no` as boolean false and Norway
disappears from the declaration without a trace.

`set_profile` in step 3 checks the slugs and returns the coverage preview.
Show it to the developer before spending the lint:

```
You declared 6 jurisdictions. LexLint holds data for all 6.
  us      19 instruments · reviewed 2026-08-12
  us/ca   14 instruments · reviewed 2026-08-12
  eu      12 instruments · reviewed 2026-08-12
  de       8 instruments · reviewed 2026-08-12
  gb       6 instruments · reviewed 2026-08-12
  kr       3 instruments · reviewed 2026-08-12

Depth varies. A low count is coverage LexLint has, not coverage the
jurisdiction lacks.
```

A slug with `held: false` returns a coverage warning, never a pass. Say so
here, not after the run.

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

### 3. Set the profile, then run the lint

Two calls. The first validates the declaration and tells you what the corpus
holds for it; the second returns findings.

```
set_profile(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"]
)
```

Unknown argument names and unknown activity values are refused here rather than
ignored, so a typo cannot produce a falsely clean run. Read three things off
the answer before going on:

- **A malformed slug is REFUSED here**, with every bad one named, and no
  request is spent. A slug LexLint cannot parse is not a jurisdiction with no
  data, it is one that never gets looked at, so fix the spelling with the
  developer and call again rather than proceeding without it.
- **`coverage`** says what is held for each slug, and `resolved_from_parent`
  says which ones answered from a parent. Tell the developer when a slug they
  named is answering from one rung up.
- **`profile`** is the canonical form. Write **that** into `lexlint.yml`, not
  what you typed: it is normalized, and the manifest should hold the same
  strings the next run will send.

**This step costs one upstream request, and it is the same one `check_access`
spends on coverage.** So call `check_access` with no `jurisdictions` argument
and let this step answer coverage. Asking both pays twice for one answer.

```
run_lint(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"],
  client_version="1.12.0"
)
```

The same declaration, from the profile you just had blessed, plus your own
`client_version`. The version is not part of the profile and never goes into
`lexlint.yml`: it describes the plugin making the call, not the app being
linted.

### 4. Merge the findings into the manifest

Rewrite only the `lint:` block. Never touch `version`, `app`, or `profile`:
those are the developer's declaration, not yours. And **carry
`lint.work_items` across untouched** if it is there: it is the plan the
developer approved in the last run's triage, the run does not produce it, and a
rewrite that drops it deletes their work silently. A work item whose findings
have all vanished stays: deciding it is finished is the developer's call.

For every finding in the new run:

- If its `id` appeared in the previous run, **carry `state`, `where`, `note`
  and `handled_by` across verbatim** and refresh everything else from the run.
  `handled_by` is a triage decision, not a fact about the law, so the run has
  no opinion about it and must not clear it.
- If its `id` is new, set `state: new`.

For every acknowledged finding whose `id` did **not** appear in the new run,
move the entry to `lint.vanished` with a `last_seen` date and tell the
developer. Do not delete it. The instrument may have been repealed, or its
citation may have been edited upstream so the derived id moved. Those have
opposite implications and the lint cannot tell them apart.

`state` has exactly two values, `new` and `acknowledged`. There is deliberately
no `resolved`, `fixed`, `waived`, or `ignored`. An obligation applies whether or
not you have met it, so a finding never goes away. `acknowledged` means "we have
seen this and here is where we handled it", which is true and stays true.

### 5. Triage: turn findings into a short plan

Findings arrive per jurisdiction, per instrument. Eight jurisdictions produce a
list nobody reads. Collapse it into **work items**: one per thing to actually
do, each carrying the findings it answers and the jurisdictions it spans.

The same mitigation usually answers several findings at once. Honoring
machine-readable TDM reservations answers the EU DSM article and its national
implementations together. Labeling synthetic output answers the AI Act, the KR
phase-in and several US state duties together. **The findings are many; the
things to build are few.**

Each work item takes one of exactly three lanes:

- `code`: a change to this repository. Ship a diff.
- `doc`: an artifact this repository should carry: a usage statement, a crawl
  policy, a procedure note. Draft it into the repo.
- `counsel`: not yours to act on alone. Record it and route it. This is a
  real bucket, not a paywall, and nothing here is dressed as one.

Write the plan to `lint.work_items` and point each finding at its item with
`handled_by`. Then show the developer:

```
12 findings across 8 jurisdictions → 5 things to do

  CODE     honor machine-readable TDM reservations before fetch
           eu · de · fr
  CODE     label synthetic content on generated output
           eu · kr · us/ca
  DOC      AI-usage statement in the product README
           eu · kr

  2 findings routed to counsel, listed with their citations linked.
```

**Get their approval before touching a file.** They may merge items, split
them, or strike one. This is the step where a list becomes a plan, and it is
theirs.

`handled_by` is a slug you choose. It records which work item answers a
finding. It is not a claim that the obligation is discharged.

### 6. Work the lanes

**Code lane.** Find the file the work item implicates, ship the diff, and
record the location in `where` with a short `note` on every finding the item
answers.

**Doc lane.** Draft the artifact into the repository where it belongs: a README
section, a policy page, a docs entry. Use `docs/compliance/` only when the repo
offers no natural home. These are the developer's documents, not LexLint's.

Every draft opens with a header naming the citations that prompted it, marking
it as a draft for the developer to own and edit, and stating plainly that it is
not legal advice and that its existence discharges nothing.

**Counsel lane.** Do not draft user-facing legal text or advise on it. Record
the finding with `handled_by: counsel` and list it with its citation, linked as
below, so the developer can hand a lawyer something specific rather than a
warning.

Every lane sets `state: acknowledged`. There is no `resolved`.

### Link every citation that has a page

A finding whose instrument has a LexLint page carries `note_url`. Everywhere
you show that finding, show its citation as a link to that page: in the triage
list, in the work item, in the counsel list, in `lexlint.yml`. A citation alone
is a string to go and search for. The page behind it holds the summary, the
status, the effective date, what the instrument asks of an app, and the source
the research was read from.

```
  COUNSEL  Confirm whether the labeling duty reaches this product
           eu - [AI Act Art. 50](https://lexlint.org/l/eu-2024-1689-50)
```

**Never construct that URL.** `note_url` is a short code stored with the
record, not something derivable from the citation, and an instrument the
research engine has not reached carries none. No `note_url`, no link: show the
citation plain. A guessed link 404s underneath a statute the developer is about
to act on, which is worse than the citation on its own.

Carry `note_url` into the manifest beside `citation`, so the committed file
stays readable in six months.

### 7. Report only what the lint can claim

The passing state is **"no basic issues found"**. Never restate it as clearance,
certification, or a clean bill of health, and never suppress a coverage warning
to make a summary look tidier. A jurisdiction LexLint has no data for is a
warning, never a silent pass, and unlinted is not the same as clean.

## Cache what you fetched

A jurisdiction payload is roughly 10 KB and costs one upstream request every
time it is read, plus one more for each parent the resolution walk passes
through on the way. A triage pass that re-reads the same six jurisdictions
while working the lanes spends most of a day's free tier re-downloading law
that did not change.

So persist what `get_law` returns, into the repo you
are working in:

```
.lexlint/
  jurisdictions/
    us.json
    us/ca.json
    eu.json
```

Add `.lexlint/` to `.gitignore` unless the developer asks for it committed.
Committing it deliberately is a reasonable choice and often a good one: it
turns "the law changed underneath us" into a diff a reviewer can read.
Committing it by accident is neither, so ask rather than assume.

Each file holds the payload plus the two fields that make it checkable:

```json
{
  "slug": "us/ca",
  "as_of_date": "2026-08-12",
  "cached_at": "2026-08-25T20:31:00Z",
  "payload": { }
}
```

`as_of_date` is the payload's own `provenance.as_of_date`, lifted to the top
level so the check below can run without parsing the whole file.

**Key on the resolved slug, never the requested one.** `get_law("us/ca/sf")`
walks up and answers from `us/ca`, reporting the walk in `resolved_from`. Filed
under what was asked for, one corpus row lands in the cache repeatedly under
slugs `check_access` has never heard of, and not one of those entries can be
revalidated.

### Revalidating is free, so do it every run

`set_profile` is already a call of every run, and it reports `as_of_date` for
each declared slug in that one request. That is the whole freshness check:
compare each cached `as_of_date` against what `set_profile` just reported, and
re-fetch only what moved. A cache of any size revalidates inside a call you were
making anyway, so there is no size at which checking costs more than not
checking.

Do **not** pass `jurisdictions` to `check_access` to get these dates. It answers
the same question off the same upstream request, so asking both spends two
requests for one answer, which is the cost the two-step split was arranged to
avoid.

Re-fetch a jurisdiction when any of these holds:

- `set_profile` reports an `as_of_date` the cached copy does not carry.
- The cached entry is more than 24 hours old. `as_of_date` is a review date
  rather than a build stamp, so a correction that does not move it is invisible
  to the comparison above, and the 24-hour bound is what limits how long such
  an edit can be served from disk.
- The file does not parse, or its envelope disagrees with the payload inside.
  Delete it and fetch. An entry LexLint cannot read is not a cache hit.

### What the cache must never do

**It must never create coverage.** If `check_access` reports `held: false` for
a slug, a copy cached while it was held does not make it held. Report the
coverage warning exactly as a run with no cache would. Coverage is what the
corpus holds now, and a local file answering otherwise is the reassuring wrong
answer with a cache in front of it.

**It must never feed the lint.** `run_lint` reads the corpus
server-side and verifies it against the published manifest, by row count, byte
count and digest, on every run. Nothing hands it a cached copy, and that is
deliberate: the verification is what stops a half-published corpus from linting
clean, so a cache able to reach it would be a way to skip it. Findings are not
cached either, for the same reason `lint.vanished` exists.

**It must never be quiet about itself.** Extend the status line the run already
prints:

```
lexlint 1.12.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
cache: 5 jurisdictions held, 1 refreshed
```

Someone reading a citation is owed the knowledge of whether it was read from
the corpus this minute or from a copy taken yesterday.

Domain resolutions need none of this. `profile.domains` in `lexlint.yml`
already records them, so a domain sitting there is not resolved a second time.

## The severity model

| Severity | Meaning |
|----------|---------|
| `error` | The declared activity appears prohibited or presumptively unlawful there. Stop and get counsel. |
| `warn` | An obligation applies to the declared profile, or LexLint lacks current data for a declared jurisdiction. Either way: go look. |
| `info` | A disclosure, labeling, or registration duty worth knowing about, typically with a phase-in date. |

Every finding carries `as_of_date` and `stale`, because laws change faster than
corpora do. A stale finding is still worth acting on; it just may lag the law.

Findings also carry a `kind`:

| `kind` | Meaning |
|--------|---------|
| `obligation` | A specific instrument binds the declared profile. |
| `coverage` | LexLint could not read something, or holds no data. Never a pass. |
| `posture` | How this jurisdiction's law treats crawling as a whole: whether browsewrap binds, what weight robots.txt carries, whether a public page is outside computer-crime law. Jurisdiction-wide attributes rather than instruments, so they bind nobody on their own and cite nothing. They appear only when `crawls_web` is declared. |
| `pending` | An instrument that is not law yet: proposed, in committee, or enacted with a future effective date. Also covers an instrument that is enacted but whose enforcement a court has enjoined. An injunction can be lifted, so treat this as a duty to watch, not one to ignore. |

A `posture` finding whose value is `unsettled` is a warning, not a pass. "The
law here is silent, untested, or in flux" is among the most actionable things a
crawler author can be told.

## Sending feedback

There is one tool that writes rather than reads: `submit_feedback`. It sends
the developer's feedback on LexLint to the people who build it, recorded
against their UnGovr account so we can write back.

**It runs only when the developer asks for it, and sends only what they have
explicitly approved.** Never volunteer it. Never offer it as a next step after
a lint. Never run it in a headless or CI session, where there is nobody to
approve anything. And never read the session transcript to build the summary: a
key pasted into a session is recorded there, and a summary built from one would
carry the developer's own key to us.

The shape:

1. Draft a short usage summary from what you actually did this session. If no
   lint ran, omit it rather than inventing one.
2. Ask what they want to say.
3. Print the exact payload, in full, and wait for an explicit yes.
4. Call `submit_feedback(comments, usage_summary?)` and report the receipt.

If the call fails, say plainly that nothing was sent. Never report a submission
you did not get a receipt for. One submission per session.

One other thing is sent automatically, and it is the whole of the rest of the
list: which plugin version you are running. It rides the `check_access`
preflight LexLint already makes, and is stored on its own, in a place that holds
nothing but version numbers. It is how we tell whether anyone is still on a
bundle old enough that retiring an old tool name would break them. A version
string and nothing else: not the key, not an address, and no record of what was
linted.

Nothing else about a session is collected automatically.

## What this is not

LexLint is a research summary, not legal advice, and not authorization to access
any system. It does not certify anything. A clean run means the basics were
checked against the data LexLint holds today, in the jurisdictions you declared,
for the activities you declared. It does not mean you are in the clear.

Full documentation: https://mcp.lexlint.org/docs

A worked example, end to end: https://mcp.lexlint.org/example
