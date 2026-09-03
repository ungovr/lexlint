<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://lexlint.org/static/lexlint/lexlint-mark-dark.svg">
  <img src="https://lexlint.org/static/lexlint/lexlint-mark.svg" alt="LexLint" width="76">
</picture>

# LexLint

A compliance lint for AI, scraping, privacy, age-gating, and news-aggregation law.
All five topics are matched by run_lint, not reference-only. Declare what your app does
and where it will operate, and get cited, jurisdiction-specific findings before
you ship.

Like a code linter: it catches basic issues early, it certifies nothing, and it
replaces neither QA nor legal review.

<a href="https://lexlint.org/is-the-risk-real">
  <img src="https://lexlint.org/static/lexlint/need-lexlint.png" width="560"
       alt="You need LexLint if your code or your AI agent crawls, trains on, or republishes content from sites you don't own, AI writes any content your users see, your app holds personal data, voices, or faces, under-18s can reach your app or you check that they can't, or your app has users in more than one country. One checked box is enough.">
</a>

The law behind every one of those rows is readable without installing anything.
https://lexlint.org/law is what LexLint tracks, jurisdiction by jurisdiction,
down to the individual instrument, and https://lexlint.org/news is the same law
as it moves in the press. Both are the corpus the lint runs against, so they are
also the way to see what a run would have to say about your jurisdictions before
you set one up.

Thin by design, so you can see exactly what you are installing:

- **No executables.** The bundle is one skill, three commands, and the schema.
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

**On Claude Code for the web there is no terminal and no `/plugin`, so the
repository carries the install.** Commit this as `.claude/settings.json` and
every cloud session on the repository starts with LexLint already installed:

```json
{
  "extraKnownMarketplaces": {
    "lexlint": { "source": { "source": "github", "repo": "ungovr/lexlint" } }
  },
  "enabledPlugins": { "lexlint@lexlint": true }
}
```

Two settings on the cloud environment go with it. Add `mcp.lexlint.org` to its
allowed domains, because the default network access tier reaches GitHub, which
is what makes the marketplace fetch above work, and does not reach the LexLint
server, so without it the plugin installs and then no tool call connects. Then
set `UNGOVR_API_KEY` as an environment variable there, which is where the
bundle's server configuration reads the key from at session start.

Full setup for every client, including Codex and the plain JSON block:
https://mcp.lexlint.org/#setup

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

1. Sign in at https://ungovr.org/cli-login?client=lexlint
2. Copy the key. The full value is shown once, when it is created.
3. Put it in your shell profile as `UNGOVR_API_KEY`. That is
   `export UNGOVR_API_KEY=<your-key>` in bash and zsh,
   `set -gx UNGOVR_API_KEY <your-key>` in fish, and
   `$env:UNGOVR_API_KEY = '<your-key>'` in PowerShell.
4. Start a new session. The value is read at process start, so a key exported
   into a running session is read by nothing.

**An account can hold several keys**, so creating one here leaves any key you
already have on another machine working. They share one daily allowance between
them: a second key is not a second free tier. Revoke the ones you no longer
recognise at https://ungovr.org/settings/api-keys (each row says which client
asked for it).

A key you paste into a session is recorded in that session's transcript. Treat
it the way you would any other secret in a log.

Then run `/lexlint` and read the preflight line. It reports whether the key
reached LexLint, whether it is valid, and how much of today's allowance is
left, which is the check the next three steps depend on.

## What it costs

LexLint stores no keys. Yours is passed straight through to the UnGovr Open
Data API on every call, and the upstream free tier is the only meter:
**50 requests per key per UTC day**, resetting at 00:00 UTC.

`check_access`, `set_profile`, and `run_lint` together cost five upstream
requests, however many jurisdictions you declare: one for the preflight, one
for `set_profile`, and three for `run_lint`'s read of the published corpus,
which is filtered to your declaration in memory rather than fetched per
jurisdiction. Narrowing a declaration to conserve quota buys nothing: six
jurisdictions and sixty cost the same five requests. That total does not
include resolving a domain the app talks to (`resolve_domain_jurisdiction`),
which costs one to four more requests per domain not already recorded in
`profile.domains`.

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

A lint run you upload deliberately works the same way: it reaches the LexLint
portal only when you explicitly upload it from the CLI, after your agent has
shown you exactly what it contains and you have said yes. From there it is
kept against your UnGovr account, never against a session or a repository.

One other thing is sent, automatically, and it is the whole of the rest of
the list: **which plugin version you are running**. It rides the preflight
LexLint already makes, and we store it on its own, in a place that holds
nothing but version numbers. It is how we tell whether anyone is still on a
bundle old enough that retiring an old tool name would break them. A version
string and nothing else: not your key, not your address, and no record of what
you linted.

Nothing else about your sessions is collected automatically by LexLint. Your
key is an UnGovr Open Data key, and that API keeps a request log of its own,
set out at https://www.ungovr.org/open-data/api-keys and holding which
collection was asked for and a one-way hash of the key, never which
jurisdiction you looked up.

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
  summary: "2 warnings, 1 info: no basic issues found"
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
- The law it tracks, jurisdiction by jurisdiction: https://lexlint.org/law
- Relevant law in the press: https://lexlint.org/news
- Docs and tool reference: https://mcp.lexlint.org/#tools
- A worked example, end to end: https://mcp.lexlint.org/example

Powered by UnGovr. https://www.ungovr.org
