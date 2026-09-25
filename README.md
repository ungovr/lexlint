<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://lexlint.io/static/lexlint/lexlint-mark-dark.svg">
  <img src="https://lexlint.io/static/lexlint/lexlint-mark.svg" alt="LexLint" width="76">
</picture>

# LexLint

A compliance lint for AI, scraping, privacy, cybersecurity, communications, age-gating, and news-aggregation law.
All seven topics are matched by run_lint, not reference-only. Declare what your app does
and where it will operate, and get cited, jurisdiction-specific findings before
you ship.

Like a code linter: it catches basic issues early, it certifies nothing, and it
replaces neither QA nor legal review.

<a href="https://lexlint.io/is-the-risk-real">
  <img src="https://lexlint.io/static/lexlint/need-lexlint.png" width="560"
       alt="You need LexLint if you or your AI agent crawl, train on, or republish other sites' content, AI writes any content your users see, your app holds personal data, voices, or faces, under-18s can reach your app or you check that they can't, or your app has users in more than one country. One checked box is enough.">
</a>

The law behind every one of those rows is readable without installing anything.
https://lexlint.io/law is what LexLint tracks, jurisdiction by jurisdiction,
down to the individual instrument, and https://lexlint.io/news is the same law
as it moves in the press. Both are the corpus the lint runs against, so they are
also the way to see what a run would have to say about your jurisdictions before
you set one up.

Thin by design, so you can see exactly what you are installing:

- **No executables.** The bundle is one skill, three commands, and the schema.
  Everything that runs here runs in your own agent, where you can read it.
- **One execution path.** The lint is deterministic and happens in one place,
  a stateless worker; the law data behind it updates server-side, not in this
  bundle. To avoid hallucinations, which law applies is decided by a fixed,
  rule-based match against the corpus, never by asking the LLM to reason
  about the law itself.
- **No stored keys.** Yours passes straight through to the UnGovr Open Data
  API on every call, and LexLint keeps nothing.

## Get a key

Take the key first. The plugin reads `UNGOVR_API_KEY` at process start, the
same moment it loads, so a key that is in your shell profile before you
install costs one restart, and a key taken afterwards costs a second one.
The restart is the inconvenience and the server is the decision: once
installed, every later session in this client carries LexLint's server and can
call its tools, until you remove it.

LexLint runs on your own UnGovr Open Data key, and there are two ways to get
one. Neither is a fallback for the other:

- **No account.** Open https://lexlint.io/trial and press the button. It
  mints a 30-day key good for 50 requests over its whole life and shows it
  once. Or hand your coding agent https://lexlint.io/first-run and it
  runs the first lint and takes the key on the way.
- **With an account**, which is free. Sign in at
  https://ungovr.org/cli-login?client=lexlint and copy the key. The full value
  is shown once, when it is created. An account key never expires and has no
  lifetime total, so pick this route if you plan to keep using LexLint past
  the trial.

Then put it in your shell profile as `UNGOVR_API_KEY`. That is
`export UNGOVR_API_KEY=<your-key>` in bash and zsh,
`set -gx UNGOVR_API_KEY <your-key>` in fish, and
`$env:UNGOVR_API_KEY = '<your-key>'` in PowerShell. The value is read at
process start, so a key exported into a running session is read by nothing.

**An account can hold several keys**, so creating one here leaves any key you
already have on another machine working. They share one daily allowance between
them: a second key is not a second free tier. Revoke the ones you no longer
recognise at https://ungovr.org/settings/api-keys (each row says which client
asked for it).

A key you paste into a session is recorded in that session's transcript. Treat
it the way you would any other secret in a log.

**Already installed and no key yet?** Run `/lexlint-key` and it hands you the
sign-in link, takes the key you paste back, and puts it where your next
session will read it. Or ask your session to call `claim_trial_key`, which
mints the same 30-day trial key and returns it in the result, recorded in the
transcript the same way a pasted key is. Either way it is the next session
that has it.

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

Two settings on the cloud environment go with it. Add `mcp.lexlint.io` to its
allowed domains, because the default network access tier reaches GitHub, which
is what makes the marketplace fetch above work, and does not reach the LexLint
server, so without it the plugin installs and then no tool call connects. Then
set `UNGOVR_API_KEY` as an environment variable there, which is where the
bundle's server configuration reads the key from at session start.

Full setup for every client, including Codex and the plain JSON block:
https://mcp.lexlint.io/#setup

**Restart your session after installing.** Plugins load at process start, and
so does the key, which is why it went into your profile first: one restart
covers both. A `/clear` is not a restart. Until you restart, the status
commands will report the server healthy while the plugin is absent.

**What installing adds is a server, not a restart.** The restart happens once.
From then on, every later session in this client carries LexLint's server and
can call its tools, whether or not that session lints anything. At the default
`user` scope that is every project on the machine. It stays until you remove
it:

```
claude plugin uninstall lexlint@lexlint
```

Then run `/lexlint` and read the preflight line. It reports whether the key
reached LexLint, whether it is valid, and how much of today's allowance is
left, which is the check the next three steps depend on.

**If it reads `key: not set` and you did save a key, do not take another
one.** A key that is saved and did not arrive is not a missing key: `/lexlint`
looks for it by file name, never by value, and says where it is and why it did
not reach the server. A second trial key spends one of the limited mints your
address gets each day and leaves the first one stranded.

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
exists, so the skill will say so at the top of a run when it matters. The
bundle's server entry sends its own version on every call, so that answer
does not depend on the session remembering to ask.

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

A lint run is not something you have to ask for. A run that found anything
closes by uploading itself, so a run reaches the LexLint portal only at the
close of the run that produced it, after your agent has shown you exactly what
it contains and you have approved the upload. From there it is kept against
your UnGovr account, and a trial key's run comes back with a share link that
needs no sign-in, never against a session or a repository.

You can delete a run or delete a project at any time from the portal.
Deleting a run removes it immediately and its stored payload is purged
within 30 days; deleting a project removes it, and everything under it,
right away. You can also export a project's own runs as JSON. A run can be
shared by an unguessable, expiring link that works without signing in, and
revoking it deletes the link immediately, not merely marks it inactive. A
trial key's account has no sign-in. To keep its runs, sign in at
https://ungovr.org/cli-login?client=lexlint (an account is free) and paste the
trial key at https://my.lexlint.io/claim and the runs, their project and the
key move to your account, where the portal's delete button is yours. To have a
trial's run deleted without an account, write to hello@ungovr.org quoting the
share link and we delete the run, or the link alone, within one working day.

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
      note_url: "https://lexlint.io/l/eu-2019-790-4"
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

- Product: https://lexlint.io
- The law it tracks, jurisdiction by jurisdiction: https://lexlint.io/law
- Relevant law in the press: https://lexlint.io/news
- Docs and tool reference: https://mcp.lexlint.io/#tools
- A worked example, end to end: https://mcp.lexlint.io/example

Powered by UnGovr. https://www.ungovr.org
