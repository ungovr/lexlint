# LexLint

A compliance lint for AI, scraping, and privacy law. Declare what your app does
and where it will operate, and get cited, jurisdiction-specific findings before
you ship.

Like a code linter: it catches basic issues early, it certifies nothing, and it
replaces neither QA nor legal review.

Thin by design, so you can see exactly what you are installing:

- **No executables.** The bundle is one skill, one command, and the schema.
  Everything that runs here runs in your own agent, where you can read it.
- **One execution path.** The lint is deterministic and happens in one place,
  a stateless worker; the law data behind it updates server-side, not in this
  bundle.
- **No stored keys.** Yours passes straight through to the UnGovr Open Data
  API on every call, and LexLint keeps nothing.

## Install

Add the marketplace and install the plugin. Either form works:

```
claude plugin marketplace add ungovr/lexlint
claude plugin install lexlint@lexlint
```

or, inside a session, `/plugin marketplace add ungovr/lexlint` then
`/plugin install lexlint@lexlint`. The non-interactive form is the one to use
in a script or a container image.

**Restart your session after installing.** Plugins load at process start. A
`/clear` is not a restart. Until you restart, the status commands will report
the server healthy while the plugin is absent.

## Update

**LexLint moves, and your installed copy does not.** The law data behind the
lint updates server-side and reaches you without doing anything. The bundle in
this repository is the other half, and it is frozen at the version you
installed until you update it: the skill's instructions, the command, and
`lexlint.schema.json` all sit on your machine.

That matters more here than for most plugins, because the skill is the product.
A stale copy runs a workflow the server has moved past, and validates
`lexlint.yml` against a schema that is no longer the current one.

```
claude plugin update lexlint@lexlint
```

**Then restart your session.** Plugins load at process start, so an update
applied inside a running session is read by nothing until the next one.

Two things worth knowing when an update looks like it did not take:

- **`--scope` defaults to `user`.** If you installed LexLint into a single
  project with `--scope local`, the user-scope update does not touch it. Run
  `claude plugin update lexlint@lexlint --scope local` from that project's
  directory.
- **`claude plugin marketplace update` and `claude plugin update` are
  different commands.** The first refreshes the catalog, the second moves your
  installed copy. Running only the first leaves you exactly where you were.

You do not have to track releases yourself. Every `check_access` and every
`run_lint` reply tells you the version you are running and whether a newer one
exists, so the skill will say so at the top of a run when it matters.

## Get a key

LexLint runs on your own UnGovr Open Data key. Run `/lexlint-key` and it will
hand you a link, take the key you paste back, and put it where your next
session will read it. If you would rather do it by hand:

1. Sign in at https://ungovr.org/settings/api-keys?cli=lexlint
2. Copy the key. The full value is shown once, when it is created.
3. Put it in your shell profile as `UNGOVR_API_KEY`. That is
   `export UNGOVR_API_KEY=<your-key>` in bash and zsh,
   `set -gx UNGOVR_API_KEY <your-key>` in fish, and
   `$env:UNGOVR_API_KEY = '<your-key>'` in PowerShell.
4. Start a new session. The value is read at process start, so a key exported
   into a running session is read by nothing.

**An account holds one key at a time, so generating a new one revokes the old
one** and anything still using it stops working. If a key is already in use
somewhere, that is the one to use here.

A key you paste into a session is recorded in that session's transcript. Treat
it the way you would any other secret in a log.

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

## Feedback

`/lexlint-feedback` sends your feedback on LexLint to the people who build it,
recorded against your UnGovr account so we can write back. It runs only when
you ask for it, it shows you the exact text before it sends anything, and it
sends nothing you have not approved.

One other thing is sent, automatically, and it is the whole of the rest of
the list: **which plugin version you are running**. It rides the preflight
LexLint already makes, and we store it on its own, in a place that holds
nothing but version numbers. It is how we tell whether anyone is still on a
bundle old enough that retiring an old tool name would break them. A version
string and nothing else: not your key, not your address, and no record of what
you linted.

Nothing else about your sessions is collected automatically.

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
      note_url: "https://lexlint.org/l/eu-2019-790-4"
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
