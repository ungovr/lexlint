# LexLint

A compliance lint for AI and scraping law. Declare what your app does and where it
will operate, and get cited, jurisdiction-specific findings before you ship.

Like a code linter: it catches basic issues early, it certifies nothing, and it
replaces neither QA nor legal review.

## Install

LexLint runs on your own UnGovr Open Data key, so set that first. Mint one free
at https://www.ungovr.org/open-data/api-keys and put it in your environment
**before** you install:

```
export UNGOVR_API_KEY=your-key-here
```

Then add the marketplace and install the plugin:

```
/plugin marketplace add ungovr/lexlint
/plugin install lexlint@lexlint
```

The key comes first because a missing one fails quietly rather than loudly. The
plugin still installs, the server still reports itself connected, and the header
simply goes out empty, so nothing complains until your first tool call comes
back rejected from upstream. If a fresh install answers a lint with an
authorization failure, check `UNGOVR_API_KEY` before you suspect LexLint.

LexLint stores no keys. Yours is passed straight through to the UnGovr Open Data
API on every call, and the upstream free tier is the only meter.

## Use

Run `/lexlint` in any repo. The skill will ask what your app does and where it
operates, write a `lexlint.yml`, run the lint, and walk the findings back into
your code.

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
