# LexLint for agents

LexLint is a lint for AI and scraping law. Like a code linter, it catches basic
issues early, it certifies nothing, and it replaces neither QA nor legal review.
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

The tools need an UnGovr Open Data API key, passed as `X-API-Key`. Mint one
free at https://www.ungovr.org/open-data/api-keys

Set it as `UNGOVR_API_KEY` in your environment, and restart the session: the
value is read at process start, so exporting it in a running session does
nothing.

**Run `check_access` before anything else**, and show the developer the result
as one line:

```
key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
```

If `key_present` is false, stop there and give them the mint URL. Do not ask
what the app does first: they cannot act on the answer.

If `key_valid` is true and `quota_remaining` is 0, the key WORKS and today's
free allowance is spent. Say when it returns. **Do not suggest minting a new
key**: minting silently revokes the one they hold.

If `key_valid` is null, LexLint learned nothing about the key: the Open Data
API did not answer. Report it as our outage, not their setup, and again **do
not suggest minting**. Only `key_valid: false` means the key was actually
rejected, and that is the one case where the mint URL belongs.

`corpus_reachable` is three-valued for the same reason: true when the corpus
was read, false when the read failed, and null when it was never attempted.
Never render null as "unreachable".

LexLint stores no keys. Yours is passed through to the UnGovr Open Data API on
every call, and the upstream free tier is the only meter. A lint costs roughly
one request per declared jurisdiction, so a six-jurisdiction app runs several
times a day inside the free tier.

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

Then call `check_access` again with the slugs, and show the coverage preview
before spending the lint:

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

### 3. Run the lint

```
lint_app_profile(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"]
)
```

Unknown argument names and unknown activity values are refused rather than
ignored, so a typo cannot produce a falsely clean run.

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

  2 findings routed to counsel, listed with their citations.
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
the finding with `handled_by: counsel` and list it with its citation so the
developer can hand a lawyer something specific rather than a warning.

Every lane sets `state: acknowledged`. There is no `resolved`.

### 7. Report only what the lint can claim

The passing state is **"no basic issues found"**. Never restate it as clearance,
certification, or a clean bill of health, and never suppress a coverage warning
to make a summary look tidier. A jurisdiction LexLint has no data for is a
warning, never a silent pass, and unlinted is not the same as clean.

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

## What this is not

LexLint is a research summary, not legal advice, and not authorization to access
any system. It does not certify anything. A clean run means the basics were
checked against the data LexLint holds today, in the jurisdictions you declared,
for the activities you declared. It does not mean you are in the clear.

Full documentation: https://mcp.lexlint.org/docs

A worked example, end to end: https://mcp.lexlint.org/example
