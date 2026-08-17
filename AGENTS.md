# LexLint for agents

LexLint is a lint for AI and scraping law. Like a code linter, it catches basic
issues early, it certifies nothing, and it replaces neither QA nor legal review.
This file is the same procedure the `lexlint` skill carries, written for any
agent that reads `AGENTS.md` instead. The tools are served over MCP at
https://mcp.lexlint.org/mcp and the connection details are in `.mcp.json` beside
this file. Follow the loop below in order, and do not paraphrase the reporting
rules in section 6: they are what makes a lint worth trusting.

**LexLint does not read your code to work out what your app does.** You declare
that, in a committed `lexlint.yml`, and the declaration is what gets linted.
Manifest-first, not detection-first: a guessed declaration produces a
confidently wrong lint, and a committed one produces a diff a reviewer can read
when the law changes underneath it.

## Setup

The tools need an UnGovr Open Data API key, passed as `X-API-Key`. Mint one free
at https://www.ungovr.org/open-data/api-keys and set it as `UNGOVR_API_KEY` in
your environment before the first run.

A missing key fails quietly rather than loudly: the server still reports itself
connected and the header simply goes out empty, so the first sign of trouble is
a tool call rejected upstream rather than a message about a missing key. If a
call comes back as an authorization failure, check the variable before you
suspect the tool.

LexLint stores no keys: yours is passed through to the UnGovr Open Data API on
every call, and the upstream free tier is the only meter.

## The loop

### 1. Read or create `lexlint.yml`

If the repo has one, read it. If not, ask the developer two questions and write
their answers down:

- **What does this app do?** One or more of: `crawls_web`, `trains_models`,
  `generates_content`, `deploys_chatbot`, `processes_voice`,
  `processes_biometrics`, `automated_outreach`, `high_risk_decisions`.
- **Where will it operate?** Jurisdiction slugs, lowercase, `/`-separated:
  `us`, `us/ca`, `eu`, `de`, `kr`. List every one of them. A jurisdiction left
  off is not passed, it is unlinted, and unlinted is not clean.

Read the code to inform your questions, never to answer them on the developer's
behalf. Declaring `trains_models` because you saw a model import, when the app
only calls an API, produces findings for obligations that do not apply.

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
those are the developer's declaration, not yours.

For every finding in the new run:

- If its `id` appeared in the previous run, **carry `state`, `where`, and
  `note` across verbatim** and refresh everything else from the run.
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

### 5. Act on the findings

This is where the lint earns its keep. The findings are structured, cited, and
specific enough to map onto the code that was just written. For each one, find
the file it implicates, fix what is cheap to fix now, and record the location in
`where` with a short `note`.

### 6. Report only what the lint can claim

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

## What this is not

LexLint is a research summary, not legal advice, and not authorization to access
any system. It does not certify anything. A clean run means the basics were
checked against the data LexLint holds today, in the jurisdictions you declared,
for the activities you declared. It does not mean you are in the clear.

Full documentation: https://mcp.lexlint.org/docs

A worked example, end to end: https://mcp.lexlint.org/example
