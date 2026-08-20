# LexLint

A compliance lint for AI and scraping law. Declare what your app does and where it
will operate, and get cited, jurisdiction-specific findings before you ship.

Like a code linter: it catches basic issues early, it certifies nothing, and it
replaces neither QA nor legal review.

## Install

LexLint runs on your own UnGovr Open Data key, so set that first.

```
export UNGOVR_API_KEY=your-key-here
```

Mint one free at https://www.ungovr.org/open-data/api-keys

**Minting revokes any key you already hold**, and no surface warns you at the
time. If a key is already in use somewhere, mint deliberately.

Then add the marketplace and install the plugin. Either form works:

```
claude plugin marketplace add ungovr/lexlint
claude plugin install lexlint@lexlint
```

or, inside a session, `/plugin marketplace add ungovr/lexlint` then
`/plugin install lexlint@lexlint`. The non-interactive form is the one to use
in a script or a container image.

**Restart your session after installing.** Plugins load at process start, and
so does `UNGOVR_API_KEY`. A `/clear` is not a restart. Until you restart, the
status commands will report the server healthy while the plugin is absent.

Then run `/lexlint` and read the preflight line. It reports whether the key
reached LexLint, whether it is valid, and how much of today's allowance is
left, which is the check the next three steps depend on.

## What it costs

LexLint stores no keys. Yours is passed straight through to the UnGovr Open
Data API on every call, and the upstream free tier is the only meter:
**50 requests per key per UTC day**, resetting at 00:00 UTC.

A lint costs roughly one request per declared jurisdiction, so a six
jurisdiction app runs several times a day well inside the free tier. A very
large declaration is a different matter: budget it against the number above
before you spend it.

## Use

Run `/lexlint` in any repo. The skill runs a preflight, asks what your app does
and where it operates, previews what the corpus holds for those jurisdictions,
runs the lint, collapses the findings into a short plan you approve, and then
works that plan: shipping diffs, drafting the documents your findings call for,
and routing what is not yours to act on alone.

## `lexlint.yml`

Manifest-first, not detection-first. LexLint does not read your code to guess
what it does: you declare that, and the declaration is committed, so a re-run
diffs cleanly when the law changes underneath you.

```yaml
version: 1
app:
  name: research-assistant

profile:
  activities: [crawls_web, generates_content]
  jurisdictions: [us, de, eu, kr]
  domains:
    stadt-koeln.de: de

lint:
  run_at: "2026-08-14"
  tool: lexlint/1.1.0
  summary: "0 errors, 2 warnings, 1 info: no basic issues found"
  findings:
    - id: eu:dsm-directive-art-4-3
      severity: warn
      kind: obligation
      jurisdiction: eu
      summary: "TDM opt-outs are enforceable rights reservations"
      citation: "DSM Directive Art. 4(3)"
      as_of_date: "2026-07-27"
      stale: false
      state: acknowledged
      where: fetcher.py
      note: "skips on machine-readable reservation signal"
  vanished: []
```

`state` has exactly two values, `new` and `acknowledged`. There is no
`resolved`, and that is on purpose: an obligation applies whether or not you
have met it, so a finding never goes away. `acknowledged` records that you saw
it and where you handled it, which stays true.

The full format is described by `schema/lexlint.schema.json`.

## What this is not

A research summary, not legal advice, and not authorization to access any
system. A clean run means the basics were checked against the data LexLint holds
today, in the jurisdictions you declared, for the activities you declared. It
does not mean you are in the clear.

## More

- Product: https://lexlint.org
- Docs and tool reference: https://mcp.lexlint.org/docs
- A worked example, end to end: https://mcp.lexlint.org/example

Powered by UnGovr. https://www.ungovr.org
