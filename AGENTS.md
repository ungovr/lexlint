<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# LexLint for agents

LexLint is a lint for AI, scraping, privacy, cybersecurity, age-gating, and news-aggregation law.
Like a code linter, it
catches basic issues early, it certifies nothing, and it replaces neither QA nor
legal review.
This file and the `lexlint` skill are two renderings of one procedure, and this
is the client-neutral one, for any agent that reads `AGENTS.md` instead. The
tools are served over MCP at https://mcp.lexlint.org/mcp and the connection
details are in `.mcp.json` beside this file. Follow the loop below in order, and
do not paraphrase the reporting rules in section 7: they are what makes a lint
worth trusting.

**LexLint does not read your code to work out what your app does.** You declare
that, in a committed `lexlint.yml`, and the declaration is what gets linted.
Manifest-first, not detection-first: a guessed declaration produces a
confidently wrong lint, and a committed one produces a diff a reviewer can read
when the law changes underneath it.

## Setup

The tools need an UnGovr Open Data API key, passed as `X-API-Key` and read from
`UNGOVR_API_KEY`. If the developer has no key, do not describe the problem and
stop. Run the key flow: hand over

https://ungovr.org/cli-login?client=lexlint

ask them to sign in, copy the key and paste it back, then persist it and tell
them to restart the session. Signing in lands them on the page that mints,
beside a Copy Key button. The value is read at process start, so a key set
inside a running session is read by nothing, which is why the restart is a step
rather than a footnote.

Persisting means `UNGOVR_API_KEY` in the environment the client starts from.
Where a step differs by client, "Client setup" at the end of this section
gives it per client, and no command from another client's entry is worth
offering: it is a dead end at the moment the developer is already stuck.

**Run `check_access` before anything else**, pass `client_version: "1.30.0"`.
Do not pass `jurisdictions`, even on a re-run whose manifest already declares
them: `check_access` spends this one request either way, and `set_profile`
answers the same coverage question later, off its own separate request, so that
is the one place to read it. Show the developer the result as one line:

```
lexlint 1.30.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
```

**That version string is yours and it is `1.30.0`.** State it, do not go looking
for it: it is checked against the bundle's own `plugin.json` before this file
ships, and a version read out of a file at runtime is a version that can be
read from the wrong tree.

Pass the same `client_version` on every `run_lint` call. A run that skips the
preflight still deserves to learn a newer plugin exists, and the server can
only compare a version it was sent.

If `key_present` is false, stop and run the setup flow above. Do not ask what
the app does first: they cannot act on the answer.

### When you cannot reach the server

**Every LexLint finding comes from a payload the server sent you in this
session. When no payload arrived, there is no lint, and there is nothing to
report.**

**The line is whether the server answered.** A connection refused, a host that
does not resolve, a request that times out, a sandbox that denies egress, a
tool call that comes back with no response at all, a 5xx: nothing answered, so
stop at that point. Say which call failed and quote the error you actually got,
and **report no findings at all**. No table, no severities, no instrument
names, no coverage section, no list of law that is "likely" to apply.

**A refusal is an answer, and it is not this case.** A slug `set_profile` sends
back as malformed, a key the server rejects, a spent quota, a declaration
returned with the allowed values: the server read what you sent and told you
what is wrong with it. Every one of those is recoverable, each has its own
instruction elsewhere in this document, and stopping on one turns a typo into a
dead end.

Name the declaration you were about to send, so the developer can re-run once
the network is there. **If the preflight is what failed, you do not have one
yet: say that instead of guessing one to fill the line.** `check_access` runs
before you have read the repository, and a declaration invented to round out a
failure report is the same defect as an invented finding, one field over.

**Do not fill the gap.** Not from your own memory of what these laws say, not
from training data, not from a web search, not from any other copy of a corpus
you find on disk. Asked for a lint it cannot run, a model will reach for
whichever route still produces an answer, and every one of those routes returns
something that looks exactly like a lint result and is not one: plausible
instrument names, plausible severities, nothing behind any of them. A developer
reading the report cannot tell the two apart, which is why this is a rule and
not a matter of judgment.

This is the sibling of "a truncated tool result is not the run" in step 3 of
the loop. **A call that did not return is not the run either**, and neither one
is visible in the report unless you put it there.

Name what it looks like from where you are sitting, because the developer can
act on the difference: a refusal that names LexLint is ours to fix, and a
network your client is not allowed to use is theirs. Then stop.

### When the response says a newer LexLint exists

An installed plugin is frozen at the version it was installed at. Nothing
updates it on its own, and a developer running a stale one gets today's data
through last month's instructions: the server can hand back a field that the
installed skill has never heard of, and the run quietly does nothing with it.
That has already happened once, which is why `check_access` answers the
question at all.

`update_available` is three-valued, and only `true` is an instruction:

- **`true`**: say so once, plainly, in the run's opening lines. Do not make it
  the whole report and do not repeat it: it is a footnote to their lint, not
  the reason they came.

  ```
  lexlint 1.4.0 · a newer LexLint (1.30.0) is available
  ```

  There is no installed client to update: the tools are served remotely and
  are always current. What goes stale is this procedure itself. Re-read it
  from the current bundle at https://github.com/ungovr/lexlint

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

Lowercase your own model id, split it into words on every character that is
not a letter, and test whether any one of those words is exactly a token in
`tested_model_families`. **Whole words, never substrings.** `solar-pro` is not
`sol` and `octopus-v2` is not `opus`, and a substring rule clears both: it
fails by staying silent about a model nobody has tested, which is the one
failure this section exists to prevent.

If one of your words is a token, say nothing. A developer told their setup is
fine learns to skim the preflight, and this is a footnote to their lint either
way.

If it does not, name the model you are and print `model_notice` verbatim, then
ask:

```
LexLint on claude-sonnet-5.

  <model_notice, printed verbatim, wrapped to your output width>

  Continue on this model, or switch and re-run?
```

The notice is **not reproduced here on purpose.** It is server-owned so that
which models are tested can change without every frozen install having to be
updated, and a copy of its wording in this file would be a second source of
truth that goes stale the first time the tested set moves. It did: this block
quoted a two-model sentence for as long as the set had two models in it. Print
what the response hands you.

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
rejected, and that is the one case where minting belongs: run the key flow
above and follow the `rejected` steps.

`corpus_reachable` is three-valued for the same reason: true when the corpus
was read, false when the read failed, and null when it was never attempted.
Never render null as "unreachable".

LexLint stores no keys. Yours is passed through to the UnGovr Open Data API on
every call, and the upstream free tier is the only meter. `check_access`,
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

### Client setup

The tools are identical in every client. Registering the server, updating the
bundle, and persisting the key are not. Use the entry for the client you are
running, and never offer a command from another entry.

**Claude Code**

- **Install**
  `claude plugin marketplace add ungovr/lexlint && claude plugin install lexlint@lexlint`

  The bundle carries the skill, the three commands, and this server already
  configured.
- **Key** `/lexlint-key`, which persists it to the `env` block of
  `~/.claude/settings.json`

  The command hands over the sign-in link, takes the paste, and writes the
  value where the next session reads it, never into a file that gets
  committed.
- **Update** `claude plugin update lexlint@lexlint`

  `--scope` defaults to `user`, so a project that installed LexLint locally
  needs `claude plugin update lexlint@lexlint --scope local` run from that
  project's directory or it keeps loading the old copy.

**Codex**

- **Install** `codex mcp add lexlint --url https://mcp.lexlint.org/mcp`

  That registers the transport and not the key: `mcp add` has no flag for a
  custom header, and `--bearer-token-env-var` sends `Authorization`, which
  this server does not read. Add
  `env_http_headers = { "X-API-Key" = "UNGOVR_API_KEY" }` by hand to the
  `[mcp_servers.lexlint]` entry the command just wrote in
  `~/.codex/config.toml`.
- **Key** persisted to `UNGOVR_API_KEY` in the environment Codex starts from,
  named by the `env_http_headers` line in `~/.codex/config.toml`

  The value in that line is the variable's NAME, not the key itself. Codex
  reads it at connect time, so a key exported into a running session is read
  by nothing.
- **Update** not available here.

  There is no installed client to update: the tools are served remotely and
  are always current. What goes stale is this procedure itself. Re-read it
  from the current bundle at https://github.com/ungovr/lexlint

**Codex in the browser**

- **Install** not available here.

  The Codex web app at https://chatgpt.com/codex is the one Codex surface with
  nowhere to put this: it exposes no server configuration, so there is no
  version of these steps that can be done there. Set LexLint up in the Codex
  CLI, the IDE extension, or the desktop app, which share one
  `~/.codex/config.toml`. That is a statement about this one surface and not
  about ChatGPT's own connector settings, which are a different product
  LexLint has not tested.
- **Key** not available here.

  There is nowhere on this surface to put a header or an environment variable.
  Say that plainly rather than walking a developer through steps their surface
  cannot take.
- **Update** not available here.

  Nothing is installed there to update.

**Any other MCP client**

- **Install** `https://mcp.lexlint.org/mcp`

  Any client that speaks streamable HTTP works. Register that endpoint with an
  `X-API-Key` header carrying the key; an `Authorization` header is ignored.
  The server is stateless and holds no session of its own, so nothing has to
  be kept between calls.
- **Key** persisted to `UNGOVR_API_KEY` in the environment the client starts
  from

  Some clients expand `${UNGOVR_API_KEY}` inside a config file and some do
  not. If yours does not, the key is written literally and the file is then
  the secret it contains.
- **Update** not available here.

  There is no installed client to update: the tools are served remotely and
  are always current. What goes stale is this procedure itself. Re-read it
  from the current bundle at https://github.com/ungovr/lexlint

## Four tools that make this cheaper, and none of them required

Everything below works with no shell at all. Four ordinary tools make it
cheaper, and it is worth knowing which you have before you need them:

| Tool | What it saves | Where |
|---|---|---|
| `jq` | keeps a `run_lint` response out of your context entirely | step 3, and the hash below |
| `python3` with PyYAML | writes the merged `lint:` block without it passing through your output | step 4 |
| `curl` | keeps the upload payload out of your own output | "Uploading a run" |
| `sha256sum` | computes `payload_hash` without the bytes reaching you | "Uploading a run" |

**Check once, lazily, and remember the answer.** The first time you want one of
them, ask in a single command rather than probing per call:

```bash
command -v jq curl sha256sum shasum python3
python3 -c 'import yaml'
```

**PyYAML is the thing being asked about in the second line, not `python3`.**
It is not in the standard library, so an interpreter on the PATH is not an
answer on its own, and the second line exits non-zero on the machines where
they part. Nothing else in this procedure needs it.

**`shasum` is in that list on purpose**: macOS ships it and does not ship
`sha256sum`, so probing only the GNU name reports the hash tool missing on a
Mac that has one. Either name counts as present, and where you use it, it is
`shasum -a 256`. **If the command itself cannot run, you have no shell**, which
is a different situation from a missing tool and is answered in step 3 by a
route that needs neither.

**When one is missing, the flows still work.** Every place these appear names
the route to take without them, and none of those routes is a degraded lint:
they cost more tokens or more upstream requests, never accuracy. Take the route
you have and say which one you took.

### Say so once, and only when it actually cost something

A developer who would never notice the difference should never be told about
it. So **do not report a missing tool because it is missing.** Report it in the
run where its absence had a measurable cost, with the number from that run, and
then not again:

- The response went past the tool-result limit and you had no `jq`, so you
  split the declaration across calls and spent three upstream requests per
  call.
- You wrote the manifest and had no `python3` with PyYAML, so the whole
  `lint:` block came out through your own output.
- An upload happened and you had no `curl`, so the payload went through your
  own output to reach the tool.

One line, in the report, phrased as the fact it is:

    This run's response was 147 KB and had to come back through my own
    context. `jq` would have kept it out of it. Not required, and nothing
    here failed.

**Once per session, never repeated**, on the same reasoning as the
newer-version notice: it is a footnote to their lint, not the reason they came.
Never make it a recommendation to act on before the findings, never list tools
they already have, and never say a run was degraded, because it was not.

**Two cases get no line at all.** A headless or CI session, where nobody is
there to install anything. And a client with no shell, where installing `jq`
changes nothing, because an agent that cannot run a command cannot run that
one either: telling someone to install a tool their client cannot invoke is
noise wearing the clothes of advice.

## The loop

### How to show a list

Four of the things below are lists with a repeating shape: the coverage
preview, the triage plan, the counsel list, the instruments table in a brief
for counsel. **Show each of those as a markdown
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
  `jurisdiction_name`: "Ireland", "European Union", "California (US)". That
  is the word in every table and every sentence; the slug (`us/ca`) belongs in
  `lexlint.yml` and nowhere a person reads. A finding without a name (a slug
  the corpus does not name) shows its slug, which is the gap it marks.
- **`summary` is one sentence; the paragraph is `detail`.** The lint writes
  the instrument's name, a colon, and one sentence, and puts the whole
  research summary in `detail`. Show the sentence in every list. Read
  `detail` before acting on a warn, and show it when the developer asks for
  a finding, never in place of the sentence.
- **`why` comes before the law.** Every instrument finding carries `why`, one
  sentence in basic language saying which declared activity reached it and
  what the corpus tags it for ("Pulled in because the app records and
  processes voices, and the corpus tags this instrument for exactly that.").
  Wherever a finding is shown on its own (a triage entry, a work item's
  findings, a brief for counsel), that sentence goes first, above `summary`,
  so the reader knows why before they meet the statute. In a table it is the
  line under the row, never a fifth column.

### 1. Read or create `lexlint.yml`

If the repo has one, read it. If not, ask the developer two questions and write
their answers down.

**What does this app do?** One or more of: `crawls_web`, `trains_models`,
`generates_content`, `deploys_chatbot`, `processes_voice`,
`processes_biometrics`, `automated_outreach`, `high_risk_decisions`,
`publishes_adult_content`, `operates_social_platform`, `serves_minors`,
`operates_app_store`, `ships_mobile_app`, `aggregates_content`,
`distributes_software_product`.

Four of these are wider than they sound. `serves_minors` is not only for
apps built for children: design codes bind a service that is merely **likely
to be accessed** by them, which catches general-purpose apps that were never
aimed at minors at all. `ships_mobile_app` is for distributing an app through
somebody else's store, which is almost every mobile developer, while
`operates_app_store` is for running the store or the operating system that
carries it. Declare the one whose duties are yours to discharge.
`distributes_software_product` is for making software available to others in
any form at all: a desktop application, a library, a package, a CLI, firmware,
or a server somebody else self-hosts. Product-security law binds the
manufacturer of a product with digital elements, which is close to every
shipped piece of software, so declare it alongside `ships_mobile_app` rather
than instead of it where you ship both.

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

**Where will it operate?** This question has four plausible readings and
developers pick the wrong one. It is not where the users are, and it is not
where the servers are. **Server location is noise. What matters is the
jurisdiction of each operator whose content or systems the app touches, plus
every jurisdiction the app itself is offered in.** For a crawler, that means
the jurisdiction of each site it fetches, which step 2 resolves.

List every one of them. A jurisdiction left off is not passed, it is unlinted,
and unlinted is not clean.

**Ask the fourth reading as its own question, because nobody volunteers it:
where are the people and the property the app acts on?** A small number of city
ordinances bind the software itself rather than whoever buys it, and each one
keys off a location the readings above never reach. Where the job candidate
sits decides whether New York City's automated employment decision rules apply.
Where the rental unit sits decides whether San Francisco's and San Jose's bans
on supplying rent-setting software apply, and those reach the vendor selling
it, not only the landlord using it. Where the premises sit decides whether
Portland's ban on private face recognition applies. A team offering a hiring
tool nationwide from Austin names none of those cities when asked about
operators or offering, and is bound by all three.

Name the city when one is in play, not just the state: `us/ca/san-francisco`
rather than `us/ca`. A city LexLint holds nothing for answers from its state
parent and reports that in `resolved_from_parent`, so naming one is never worse
than leaving it off, and leaving it off is what hides the finding.

**Quote every slug.** YAML reads a bare `no` as boolean false and Norway
disappears from the declaration without a trace.

`set_profile` in step 3 checks the slugs and returns the coverage preview.
Show it to the developer before spending the lint, as a table:

You declared 6 jurisdictions. LexLint holds data for all 6.

| Jurisdiction | Instruments | Reviewed |
|---|---:|---|
| United States (federal) | 19 | 2026-08-12 |
| California (US) | 14 | 2026-08-12 |
| European Union | 12 | 2026-08-12 |
| Germany | 8 | 2026-08-12 |
| United Kingdom | 6 | 2026-08-12 |
| South Korea | 3 | 2026-08-12 |

Depth varies. A low count is coverage LexLint has, not coverage the
jurisdiction lacks.

A slug with `held: false` returns a coverage warning, never a pass. Say so
here, not after the run, and give it a row of its own rather than dropping it
from the table: a jurisdiction missing from the preview reads as one nobody
declared.

**Scope: which files you read, never which law applies.** By default the lint
reads the whole repository. A manifest narrows that with `app.scope`:

```yaml
app:
  name: crawl4ai
  repo: https://github.com/unclecode/crawl4ai
  scope:
    include:
      - crawl4ai/
    exclude:
      - crawl4ai/js_snippet/
```

- No `scope` means the whole repository, which is what every existing manifest
  says by saying nothing.
- `include` present means those paths only. Paths are relative to the
  manifest's own directory. An absolute path, or one that climbs out with
  `..`, is a manifest error: say so and stop.
- `exclude` subtracts, with or without an `include`.
- A trailing `/` is a directory and everything under it. Anything else is a
  glob.
- **An `include` that matches no file stops the run.** Falling back to the
  whole repository there would read everything while reporting that it read
  one directory, and the report is what the developer trusts.

Scope is a reading instruction. It does not narrow the declaration, and this
is the mistake to expect: a crawler scoped to its fetch layer still operates
in every jurisdiction it was declared in, and it draws exactly the findings it
drew before. Narrowing the read never narrows a duty. If the developer means
that a subtree is a different app with a different profile, that is a second
manifest with its own `app.name`, not a scope.

State the scope in the run header and again in the report, so a scoped run is
never read as a whole-repo one:

Scope: `crawl4ai/`, minus `crawl4ai/js_snippet/`. 118 files.

Carry it into the uploaded record too, under `app.scope`, for the same reason,
**whichever place it came from**. The portal renders that field as the run's
coverage claim and says `whole repository` when it is absent, so a scoped run
uploaded without it is not an omission, it is a false claim about what was
read.

The developer may also narrow one run without editing the manifest, by naming
a path when they ask for the lint. It is the same narrowing under the same
rules, and it is not written to the manifest, so say in the report that the
scope came from the request rather than from the file.

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

**The `set_profile` call costs one upstream request, separate from
`check_access`'s own.** It answers the same coverage question that passing
`jurisdictions` to `check_access` would have answered, and that argument rides
a request `check_access` spends either way, so asking both just repeats the
answer. Neither order costs more.

```
run_lint(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"],
  client_version="1.30.0"
)
```

The same declaration, from the profile you just had blessed, plus your own
`client_version`. The version is not part of the profile and never goes into
`lexlint.yml`: it describes the plugin making the call, not the app being
linted.

**The response can be larger than your client will hand you.** A
three-jurisdiction declaration returning 57 findings came back at 147 KB,
roughly 2.5 KB a finding, and it went past the tool-result limit of the
harness that asked for it: the call succeeded, the server sent all of it, and
none of it reached the model. Nothing has gone wrong when this happens, and
the declarations that reach it are not unusual ones. Expect it somewhere above
forty findings, and remember that a parent-resolved child inflates that count
without adding any law (step 4).

**A truncated tool result is not the run.** Reporting the findings from the top
of a cut response as though they were the whole lint is the failure this
paragraph exists to prevent, and it is invisible in the report unless you put
it there.

There are three routes to the whole response, and **they do not need the same
things from you.** The first two need a shell, and one of them needs `jq`
specifically; the third needs nothing you do not already have. **Say which of
these you can actually do before picking one**, and say in the report which
one you took:

1. **Read the full response from wherever your client put it.** Some clients
   write an oversized tool result to a file and name the path. Needs a shell,
   and the slicing below needs `jq`.
2. **Make the same call over plain HTTPS and write the body to disk
   yourself.** These tools are JSON-RPC over HTTPS, so an ordinary HTTP client
   can make any call they make. The recipe, the headers, and the one common
   client that does not work are in "Uploading a run" below. Needs a shell and
   an HTTP client. This also spends the upstream requests a second time, which
   is the real price of the route, so say so on the quota line.
3. **Split the declaration across several `run_lint` calls and union the
   results.** Needs no shell and no tools beyond the ones already in front of
   you, so this is the route when you cannot run a command at all.

**Route 3, in full, because it is the one with no fallback behind it.**
Nearly every finding is per jurisdiction and per instrument, and those do not
depend on what was declared beside them: a slug returns the same findings
called alone as it does called with five others, with the same ids. So call
`run_lint` with one jurisdiction, or a few, until every declared slug has been
covered exactly once, and treat the union as the run.

**One finding is not per jurisdiction, and it is the reason this route needs a
rule rather than just an instruction.** A finding whose `id` begins
`activity:` says the corpus tags no instrument anywhere for a declared
activity, so that activity is unlinted rather than clean. It carries
`jurisdiction: null` because it is about the run, not about a place, and the
run that answers it is the call: `run_lint` reports it when nothing in **that
call's** jurisdictions carried the tag. Split the calls and each one answers a
smaller question than you asked.

So **`activity:` findings are intersected across the calls, while everything
else is unioned.** An activity is genuinely unlinted only when **every** call
reported it; a single call omitting it means some jurisdiction did carry the
tag, and the warning is wrong for the declaration as a whole. Getting this
backwards produces a coverage warning about law the corpus actually holds,
which is the one kind of false alarm that teaches a developer to skim the
coverage section.

Nine activities can raise it, because the corpus maps them on the flag axis
alone: `processes_voice`, `processes_biometrics`, `serves_minors`,
`ships_mobile_app`, `operates_app_store`, `publishes_adult_content`,
`operates_social_platform`, `aggregates_content` and
`distributes_software_product`. Those are ordinary
declarations rather than exotic ones, so expect the case rather than treating
it as a corner. Say in the report that the run was split and that these were
intersected, so a reader can tell this run from a single-call one.

**Where the calls landed in files, keep one file per call** and unwrap each
one separately: `lint-1.json`, `lint-2.json`, and so on. Step 4's merge does
the intersection itself, and it can only do it while the calls are still told
apart. Union them into a single file first and the rule above has already been
broken, invisibly, by the tidying.

**This is not narrowing the declaration**, which the paragraph below forbids.
Every declared slug is still linted; only the calls are divided. The two look
alike and are told apart by one question, asked at the end: **is any declared
jurisdiction missing from the union?** If one is, that is the forbidden thing,
whatever the intention was.

Two costs come with it, and one rule that is not optional:

- **Requests.** `run_lint` spends three upstream requests per call however many
  jurisdictions the call carries, so four calls cost twelve rather than three.
  Count that against the quota line before starting, exactly as with resolving
  domains.
- **`corpus_built_at` has to be the same on every call.** If it moves between
  them, the corpus was rebuilt underneath you and the union is two runs wearing
  one date, which this procedure forbids everywhere else it can happen (see
  "Never pair one run's findings with another run's envelope"). Start again from
  the first call. Expect this rather than treating it as bad luck: the corpus
  rebuilds daily, and a split run is the one shape that can straddle the
  rebuild.

**Unwrap the file before reading anything out of it, because the two routes
hand you different shapes.** A client's tool-result file usually holds the lint
itself. A file written by an HTTP client holds the JSON-RPC envelope around it,
and the lint is a JSON *string* inside `result.content[0].text`. Normalize
once, and work only from what comes out:

```bash
jq -e '
  if .error then
    "the server returned an error, not a lint: "
      + (.error.message // "no message") | error
  elif (.result.content[0].text? // null) != null then
    .result.content[0].text | fromjson
  elif has("findings") then .
  else "this file is neither a lint nor a reply carrying one" | error
  end' response.json > lint.json
```

**Every branch of that is load-bearing, and the two that raise an error are
the ones worth understanding.** Skipping the unwrap fails silently: `jq
'.findings | length'` against an un-unwrapped envelope does not error, it
prints `0`, because an envelope genuinely has no `findings` key. And an
envelope carrying `error` instead of `result` fails the same way for the same
reason, which is why it is caught by name and not left to a fallback. **An
auth failure, a spent quota or a malformed hand-built request all arrive as
that shape**, and a fallback that treated it as an already-unwrapped lint
would report a failed call as a clean run. A run of 57 findings reported as a
clean lint, or a refused call reported as one, is the exact failure this
section exists to prevent, and on the way past each looks like a command that
worked. So `lint.json` is written only where there is a lint to write, and
anything else stops with a reason in it.

Then read `lint.json` in slices rather than whole: the count with `jq
'.findings | length'`, the list with `jq -r '.findings[] | [.id, .severity,
.summary] | @tsv'`, and one finding's full body only when you are about to act
on that finding. Check the count against the coverage table `set_profile`
returned before you report it: a count you were not expecting means something
was truncated, or never unwrapped, or never a lint in the first place.

**Never narrow the declaration to make a response fit.** A jurisdiction dropped
to shrink a payload goes unlinted while the report says the run covered it,
which is the trade this whole procedure is written against.

### 4. Merge the findings into the manifest

Rewrite only the `lint:` block. Never touch `version`, `app`, or `profile`:
those are the developer's declaration, not yours. And **carry
`lint.work_items` across untouched** if it is there: it is the plan the
developer approved in the last run's triage, the run does not produce it, and a
rewrite that drops it deletes their work silently. A work item whose findings
have all vanished stays: deciding it is finished is the developer's call.

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
rung up. Every finding read from a parent carries `resolved_from` naming that
parent. This is the declaration reported as it was made rather than a
duplicate to clean up, and both entries stay in the manifest: the developer
declared the city, and the record should say what the city returned.

Three rules stop the mirror from inflating everything downstream:

- **A finding carrying `resolved_from` mirrors the finding with the same
  citation under the slug `resolved_from` names.** Match on that pair, never
  by comparing summaries.
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
  topic `run_lint` could not evaluate. Every topic in the corpus is evaluated
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

**With `python3` and PyYAML, do it on disk.** The script below applies every
rule in this step: it reads the run out of the files step 3 left on disk,
reads the previous triage out of the manifest, rewrites **only** the `lint:`
block, and prints the numbers your report needs so that counting them never
costs you a finding read into context. Write it to `/tmp/lexlint_merge.py`,
run it, delete it. **Never into the repository**, which is a working tree you
are about to ask the developer to commit.

```python
#!/usr/bin/env python3
"""Merge a LexLint run into lexlint.yml. Needs python3 with PyYAML."""
import argparse, json, os, re, sys
import yaml

CARRY = ("state", "where", "note", "handled_by")
KEYS = {
    "lint": ("run_at", "tool", "summary", "findings", "work_items", "vanished"),
    "findings": (
        "id", "severity", "kind", "jurisdiction", "jurisdiction_name",
        "summary", "detail", "why", "matched_by", "posture", "basis",
        "citation", "url", "note_url", "status", "requires", "applies_to",
        "effective_date", "lifecycle", "settledness", "as_of_date", "stale",
        "confidence", "resolved_from") + CARRY,
    "work_items": ("id", "lane", "title", "findings", "jurisdictions"),
    "vanished": ("id", "last_seen") + CARRY,
}

def die(msg):
    sys.stderr.write("lexlint merge: %s\n" % msg)
    raise SystemExit(1)

def scalar(v):
    """One shape per value, so a client with no python3 can match it by hand."""
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    s = str(v)
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in s):
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        s = s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        s = "".join(c if 0x20 <= ord(c) != 0x7F else "\\x%02X" % ord(c) for c in s)
        return '"%s"' % s
    return "'%s'" % s.replace("'", "''")

def emit_map(d, ind, out, prefer=()):
    for k in [k for k in prefer if k in d] + sorted(set(d) - set(prefer)):
        v, pad = d[k], " " * ind
        if isinstance(v, dict) and v:
            out.append("%s%s:" % (pad, k))
            emit_map(v, ind + 2, out, KEYS.get(k, ()))
        elif isinstance(v, list) and v:
            out.append("%s%s:" % (pad, k))
            emit_seq(v, ind + 2, out, KEYS.get(k, ()))
        elif isinstance(v, (dict, list)):
            out.append("%s%s: %s" % (pad, k, "{}" if isinstance(v, dict) else "[]"))
        else:
            out.append("%s%s: %s" % (pad, k, scalar(v)))

def emit_seq(items, ind, out, prefer=()):
    pad = " " * ind
    for it in items:
        if isinstance(it, (dict, list)) and it:
            sub = []
            (emit_map if isinstance(it, dict) else emit_seq)(it, ind + 2, sub, prefer)
            out.append(pad + "- " + sub[0][ind + 2:])
            out.extend(sub[1:])
        elif isinstance(it, dict):
            out.append(pad + "- {}")
        elif isinstance(it, list):
            out.append(pad + "- []")
        else:
            out.append(pad + "- " + scalar(it))

def split(text):
    """The manifest either side of the top-level lint: block, kept verbatim."""
    lines = text.split("\n")
    at = next((i for i, l in enumerate(lines) if re.match(r"^lint[ \t]*:", l)), None)
    if at is None:
        return text, ""
    end = next((j for j in range(at + 1, len(lines))
                if re.match(r"""^[A-Za-z_'"]""", lines[j])), len(lines))
    # `lint:` is the last top-level key the schema allows, so a run of blank
    # lines and column-0 comments at the end of that span is the developer's
    # footer rather than the block. Walk it back out, or the first merge eats
    # a file header nobody will notice is gone.
    while end > at + 1 and (not lines[end - 1].strip()
                            or lines[end - 1].startswith("#")):
        end -= 1
    return "\n".join(lines[:at]), "\n".join(lines[end:])

def load_run(paths):
    """Union every call, INTERSECT the per-run activity: findings."""
    calls = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as fh:
                calls.append(json.load(fh))
        except Exception as exc:
            die("%s is not readable JSON: %s" % (p, exc))
    stamps = sorted({str(c.get("corpus_built_at")) for c in calls})
    if len(stamps) > 1:
        die("the calls report different corpus_built_at (%s): the corpus rebuilt "
            "mid-run, so start again from the first call" % ", ".join(stamps))
    merged, per_call = {}, []
    for c in calls:
        if not isinstance(c.get("findings"), list):
            die("a run file carries no findings list; unwrap it first")
        acts = set()
        for f in c["findings"]:
            fid = f.get("id") if isinstance(f, dict) else None
            if not isinstance(fid, str) or not fid:
                die("a finding carries no usable id: %r" % (fid,))
            if fid.startswith("activity:"):
                acts.add(fid)
            merged.setdefault(fid, f)
        per_call.append(acts)
    keep = set.intersection(*per_call)
    return ([f for i, f in merged.items() if not i.startswith("activity:") or i in keep],
            sorted(set.union(*per_call) - keep), stamps[0], len(calls))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--previous", help="manifest to take triage from, if not --manifest")
    ap.add_argument("--run-at", required=True)
    ap.add_argument("--tool", required=True)
    ap.add_argument("--summary")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--allow-empty", action="store_true")
    a = ap.parse_args()

    findings, act_gone, corpus, calls = load_run(a.runs)
    if not findings and not a.allow_empty:
        die("this run has no findings: refusing to overwrite a manifest with an "
            "empty lint block (--allow-empty if that is really the run)")
    try:
        text = open(a.manifest, encoding="utf-8").read()
    except OSError as exc:
        die("cannot read %s: %s" % (a.manifest, exc))
    doc = yaml.safe_load(text) or {}
    if not isinstance(doc, dict) or not isinstance(doc.get("profile"), dict):
        die("%s carries no profile block" % a.manifest)
    prev_text = open(a.previous, encoding="utf-8").read() if a.previous else text
    prev = (yaml.safe_load(prev_text) or {}).get("lint") or {}
    # A hand-edited manifest can hold anything. An entry with no string id is
    # skipped rather than crashing the merge or matching something by accident.
    prev_f = {f["id"]: f for f in prev.get("findings") or []
              if isinstance(f, dict) and isinstance(f.get("id"), str)}
    prev_v = {v["id"]: v for v in prev.get("vanished") or []
              if isinstance(v, dict) and isinstance(v.get("id"), str)}

    out_f, carried, restored, first, unknown = [], 0, 0, 0, set()
    for f in findings:
        # The run has no opinion about the four: drop them, then take the
        # developer's, matched on id and on nothing else. A key the schema
        # does not name is dropped too, and named in the summary: `finding`
        # is closed, so writing it out lands a manifest that fails the schema
        # this bundle ships with.
        new = {k: v for k, v in f.items()
               if k in KEYS["findings"] and k not in CARRY}
        unknown |= set(f) - set(KEYS["findings"])
        was = prev_f.get(f["id"]) or prev_v.get(f["id"])
        new.update({k: was[k] for k in CARRY if was and was.get(k) not in (None, "")})
        new.setdefault("state", "new")
        if not was:
            first += 1
        elif new["state"] == "acknowledged" or any(new.get(k) for k in CARRY[1:]):
            carried += f["id"] in prev_f
            restored += f["id"] not in prev_f
        out_f.append(new)

    live = {f["id"] for f in out_f}
    vanished, topics, forgotten = [], 0, 0
    for pid, pf in prev_f.items():
        if pid in live:
            continue
        if pid.startswith("topic:"):
            topics += 1                       # dropped, never moved to vanished
        elif pf.get("state") != "acknowledged":
            forgotten += 1
        else:
            e = {"id": pid, "last_seen": prev.get("run_at")}
            e.update({k: pf[k] for k in CARRY if pf.get(k) not in (None, "")})
            vanished.append(e)
    added = {e["id"] for e in vanished}
    for vid, ve in prev_v.items():
        if vid not in live and vid not in added and not vid.startswith("topic:"):
            vanished.append(dict(ve))
    vanished.sort(key=lambda e: e["id"])

    lint = {"run_at": a.run_at, "tool": a.tool}
    if a.summary:
        lint["summary"] = a.summary
    lint["findings"] = out_f
    if prev.get("work_items") is not None:
        lint["work_items"] = prev["work_items"]
    if vanished:
        lint["vanished"] = vanished

    body = []
    emit_map({"lint": lint}, 0, body, ("lint",))
    head, tail = split(text)
    head = head.rstrip("\n")
    doc_out = (head + "\n\n" if head else "") + "\n".join(body) + "\n"
    if tail.strip():
        doc_out += "\n" + tail.strip("\n") + "\n"
    with open(a.output + ".lexlint-tmp", "w", encoding="utf-8") as fh:
        fh.write(doc_out)
    os.replace(a.output + ".lexlint-tmp", a.output)

    cited = {(f.get("jurisdiction"), f.get("citation")) for f in out_f if f.get("citation")}
    mirrors = 0
    for f in out_f:
        rf = f.get("resolved_from")
        parents = [rf] if isinstance(rf, str) else (rf or [])
        mirrors += bool(f.get("citation")) and any((p, f["citation"]) in cited for p in parents)
    seen = {f.get("jurisdiction") for f in out_f}
    json.dump({
        "calls": calls, "corpus_built_at": corpus, "findings": len(out_f),
        "distinct_instruments": len(out_f) - mirrors, "mirrors": mirrors,
        "triage_carried": carried, "triage_restored": restored,
        "first_seen": first, "vanished_added": len(added),
        "vanished_total": len(vanished), "topic_notices_dropped": topics,
        "unacknowledged_gone": forgotten,
        "finding_fields_this_bundle_does_not_know": sorted(unknown),
        "activities_unlinted": sorted(i for i in live if i.startswith("activity:")),
        "activity_findings_intersected_away": act_gone,
        "work_items": len(lint.get("work_items") or []),
        "jurisdictions_missing": [j for j in doc["profile"].get("jurisdictions") or []
                                  if j not in seen],
    }, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")

main()
```

Run it against the manifest in place, then remove the script:

```bash
python3 /tmp/lexlint_merge.py lint.json --manifest lexlint.yml -o lexlint.yml \
    --run-at 2026-09-10 --tool 'lexlint 1.30.0' \
    --summary 'Six findings, five instruments, across three jurisdictions.'
rm /tmp/lexlint_merge.py
```

**One file per `run_lint` call, and hand it every one of them.** A split run
(step 3) is several calls, and the intersection rule that makes it safe cannot
be applied to a union that has already happened: pass `lint-1.json
lint-2.json lint-3.json` and let the script intersect. Handing it a
pre-unioned file is not a smaller version of the same thing, it is the run
with a coverage warning in it that the declaration as a whole does not have.

Four flags carry the run's own facts, because a script must not read them off
a clock or invent them: `--run-at` is today's date, `--tool` is your own
`lexlint 1.30.0`, and `--summary` is the one sentence you author.
`--previous <path>` takes the triage from somewhere other than the manifest,
which is the `git show HEAD:lexlint.yml > /tmp/previous.yml` recovery above.

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
question about a declared slug that never came back. A `triage_carried` of 0
against a manifest that had acknowledgments is the failure this whole section
is written against, and it is a number rather than a silence.

`finding_fields_this_bundle_does_not_know` is the one to read even when it is
the only thing that changed. A name in it means the corpus is ahead of your
installed schema, which is the ordinary shape of an additive change and not a
fault: say which fields were left out and that an update picks them up. It is
also the most direct evidence there is that an update is worth taking, so
pair it with the newer-version notice if you saw one.

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
  single-quoted scalar folds newlines into spaces and would lose them.
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
  frozen at install and the corpus is not, so this is the ordinary way a
  newer field arrives: say which fields you left out, say that upgrading
  picks them up on the next run, and do not invent a place to keep them.
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

### 5. Triage: turn findings into a short plan

**First, separate what binds this app from what does not.** One field on the
finding answers most of it, and reading the statute yourself answers none of
it.

**`applies_to` says whom the instrument binds**, as the corpus records it, and
it takes three values: `government`, `private`, `both`. A `government` finding
does not bind a private app. Read it that way, and read it that way every run:
the LexLint portal already renders such a finding as "applies to government
bodies, not this app", so a run that presents it as a live duty disagrees with
the stored copy of itself. `private` and `both` bind. **Absent is not
`private`.** Most instruments carry no value at all, and there the field
decides nothing and your own reading is what is left, exactly as before the
field existed.

`run_lint` reports `applies_to` and does not filter on it, deliberately.
Deciding that a government-only duty misses this caller means knowing what
kind of body the caller is, which the profile does not collect and no tool
here asks for. So the field comes to you and the reading lives here, which is
the reason it is written down: a session that does not think to look reports
duties binding state agencies to a private studio as work to do.

**A threshold in the instrument's own text is a different thing, and it is not
`applies_to`.** A duty reaching providers of generative AI above a revenue,
user-count or compute threshold binds on a fact about the developer that
LexLint does not hold and never asks for. Those stay live obligations. Do not
decide one either way on the developer's behalf: put the threshold into the
work item's own title, in the instrument's words ("if we pass one million
monthly users in California"), so it is answered inside the plan approval they
are already giving rather than as a question of its own.

**A finding that does not bind is not a work item, and it is not a document to
write.** It keeps `state: new`, takes no `handled_by`, and stays in the
manifest exactly as the run returned it, `applies_to` and all. The manifest is
already the register of what came back and why, and a second file restating it
is a copy that starts going stale the day it is written. Report the set as a
counted line rather than as rows:

6 findings bind government bodies rather than this app, and 5 bind providers
of generative AI above thresholds this app is nowhere near. Both sets stay in
`lexlint.yml` with their citations, and neither is a work item.

Never drop such a finding from the report to tidy it. A duty that does not
reach this app today reaches it the day the app changes, and the developer is
the one who knows which change that would be.

**Then collapse what is left.** Findings arrive per jurisdiction, per
instrument. Eight jurisdictions produce a list nobody reads. Collapse them
into **work items**: one per thing to actually do, each carrying the findings
it answers and the jurisdictions it spans.

The same mitigation usually answers several findings at once. Honoring
machine-readable TDM reservations answers the EU DSM article and its national
implementations together. Labeling synthetic output answers the AI Act, the KR
phase-in and several US state duties together. **The findings are many; the
things to build are few.**

Each work item takes one of exactly three lanes:

- `code`: a change to this repository. Ship a diff.
- `doc`: an artifact this repository should carry: a usage statement, a crawl
  policy, a procedure note. Draft it into the repo.
- `counsel`: not yours to act on alone. This lane is for findings that turn
  on legal judgment rather than work: whether the declared activity is
  permitted at all, whether a duty reaches this product, anything a
  restrictive or unsettled posture leaves as a question a diff cannot answer.
  Record it and route it. This is a real bucket, not a paywall, and nothing
  here is dressed as one.

**A finding whose `settledness.band` is `unsettled` goes to the counsel lane.
This is not a judgment you make: the corpus made it, and the fields beside
the band say why.** The band is derived in the research corpus from whether a
regulator or a court has construed the duty, whether the instrument is under
challenge, and what questions the research left open. Route it even when the
finding also looks answerable with a diff, and say so in the plan: a
mitigation you can ship does not settle whether the duty reaches this
product.

- `developing` is a signal to weigh, not a rule. Someone with authority has
  read the duty and questions remain.
- `settled` routes nothing on its own. Your own reading still can, and should.
- **Absent is not `settled`.** Most instruments carry no band yet. There the
  lane is your judgment, exactly as it was before this field existed.

`settledness.open_questions` is what the brief for counsel opens with. Show
those questions verbatim wherever you show the finding, and never rewrite one
into a recommendation: the question is the research's, and the answer is the
lawyer's.

Write the plan to `lint.work_items` and point each finding at its item with
`handled_by`, except the `topic:` tool-coverage notices, which answer to no
work item. Then show the developer:

31 findings across 22 jurisdictions, and 5 things to do.

| Lane | What to do | Jurisdictions |
|---|---|---|
| CODE | Honor machine-readable TDM reservations before fetch | European Union, Germany, France +17 more |
| CODE | Label synthetic content on generated output | European Union, South Korea, California (US) |
| DOC | AI-usage statement in the product README | European Union, South Korea |

The TDM item spans the European Union and its declared national
implementations: Germany, France, Italy, Spain, Netherlands, Poland, Sweden,
Denmark, Finland, Austria, Belgium, Czechia, Ireland, Portugal, Romania,
Hungary, Bulgaria, Croatia, Slovakia.

2 findings are routed to counsel, listed below with their citations linked.

A work item that spans many jurisdictions keeps its one row: three names, a
count, and a line under the table naming the span in full. Twenty names in
the cell wrap the row until `What to do`, the one column the developer acts
on, is unreadable. Splitting the item into one row per jurisdiction is worse:
it quietly rebuilds the per-jurisdiction list this step exists to collapse,
and hides the most useful fact the plan carries, one mitigation answering
twenty findings. The committed `lexlint.yml` holds each item's full list
wherever the table shows a count.

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
the finding with `handled_by: counsel`, then write the one artifact this lane
produces: a **brief for counsel**, one per counsel-lane work item, so the
developer hands a lawyer a file rather than a warning. A lawyer wants the
facts and the question, not a list of statutes, and a citation on its own is
a string most developers cannot read and most lawyers cannot act on without
the facts around it. The brief is the developer's document and lives in
their repository beside the doc-lane drafts. It carries, in this order:

1. **The question.** The work item's title, phrased as a question a lawyer
   can answer: "Does the labeling duty in AI Act Art. 50 reach this product?"
   **Where any finding in the item carries `settledness.open_questions`,
   those questions come first, verbatim and each attributed to its
   instrument**, and your title follows them. They were written by a
   researcher against the primary source and reviewed; your phrasing was
   not. Never merge two of them into one, and never answer one.
2. **What the app does.** The declared activities in words, and the
   jurisdictions the question spans. This is the declaration restated, never
   a description of the code.
3. **The instruments.** One row per finding: the jurisdiction by
   `jurisdiction_name`, status, as-of date, then the citation last, linked
   where `note_url` exists and plain where it does not. Under the table, one
   line per finding, so the table keeps its four columns: first the finding's
   `why`, in the lint's words, so counsel reads the reason before the law;
   then the finding's `summary` exactly as the lint gave it (the instrument's
   name and one sentence), the name linked to the LexLint page where
   `note_url` exists,
   then **where in the code** the question arises: the `where` the developer
   recorded on the finding (a path and line, an issue, a document), as a
   link into the repository when the manifest declares one and plain
   otherwise. A lawyer who can see where the question comes from reads it
   differently from one handed a statute. A
   `posture` or `coverage` finding routed here is not an instrument and
   arrives with `citation: null` and no status: its row carries the kind in
   the status column and its `basis` (the field and value the lint read,
   `crawl_policy = unsettled`) in the citation column. Never supply a
   citation for a row the lint gave none; a lawyer handed an invented
   reference has been handed something worse than a blank. Last on the line,
   where the finding carries `settledness`: its band, then the guidance link
   and the case citation the corpus recorded. A lawyer reading "unsettled"
   wants to know what has already been said about the duty, and a band with
   no evidence under it is the same non-answer a bare citation is.
4. **What is already handled.** The code and doc work items that answer the
   neighboring findings, by title and with each item's `where` (the file, the
   issue or the document it lives in), so counsel sees what the team has
   done, where it lives, and what is left to decide.
5. **The standing line.** That the brief was produced by a lint from a
   research summary of published law, that it is not legal advice, that the
   passing state is "no basic issues found", and that nothing in it
   discharges an obligation.

The summary on each finding is written for the developer; the citation is
written for the lawyer. The brief keeps both, so each reader has their half.
Do not add analysis, a recommendation, or a proposed answer: those are the
lawyer's, and a brief that argues for one is the user-facing legal text the
first sentence of this lane forbids.

Every lane sets `state: acknowledged`. There is no `resolved`.

### Link every citation that has a page

A finding whose instrument has a LexLint page carries `note_url`. Everywhere
you show that finding, show its citation as a link to that page: in the triage
list, in the work item, in the counsel list, in the brief for counsel, in
`lexlint.yml`. A citation alone
is a string to go and search for. The page behind it holds the summary, the
status, the effective date, what the instrument asks of an app, and the source
the research was read from.

| Lane | What to do | Where | Citation |
|---|---|---|---|
| COUNSEL | Confirm whether the labeling duty reaches this product | European Union | [AI Act Art. 50](https://lexlint.org/l/eu-2024-1689-50) |

**Never construct that URL.** `note_url` is a short code stored with the
record, not something derivable from the citation, and an instrument the
research engine has not reached carries none. No `note_url`, no link: show the
citation plain. A guessed link 404s underneath a statute the developer is about
to act on, which is worse than the citation on its own.

Carry `note_url` into the manifest beside `citation`, so the committed file
stays readable in six months.

### 7. Report only what the lint can claim

**A report requires a run.** Everything below is about findings the server
actually sent. If the calls in step 3 never returned a payload, there is no
report to write: see "When you cannot reach the server" in Setup, which is
where that case is answered in full.

The passing state is **"no basic issues found"**. Never restate it as clearance,
certification, or a clean bill of health, and never suppress a coverage warning
to make a summary look tidier. A jurisdiction LexLint has no data for is a
warning, never a silent pass, and unlinted is not the same as clean.

**Say what this run did not reach, every run, as its own section.** "Unlinted
is not clean" is the rule above; this is the part that makes it operational,
and it is the one thing in the report nobody can reconstruct afterwards. It is
a fixed section, it appears whether or not the run found anything, and it is
never empty, because its last line is always there:

**What this run did not reach**

- **Jurisdictions declared that LexLint holds nothing for**, by name, or that
  there were none. This is the coverage warning above, restated where a reader
  looking for gaps will find it.
- **Activities this app does that were not declared**, or that you found none.
  You read the code in step 1 to inform the questions; this is where that
  reading earns its keep, and an activity you noticed and did not declare is a
  gap you already know about.
- **Topics outside the six LexLint covers.** Name the ones a reader of this
  particular app would expect to see and LexLint does not hold. A studio that
  records identifiable people gets no right-of-publicity law out of a lint
  whose corpus does not cover it, and a report that does not say so reads as
  though the question was asked and answered.
- **The standing line.** LexLint covers AI, scraping, privacy, cybersecurity,
  age-gating and news-aggregation law, in the jurisdictions declared, for the
  activities declared. Everything else is unlinted, and unlinted is not clean.

Name the instrument where you can ("California's right of publicity, Cal. Civ.
Code section 3344") and say plainly that it did not come back under the
declared activities. Then stop: do not research it, do not summarize it, and
do not advise on it. Naming the gap is the whole job, and it is the most
useful thing a lint can say about law it does not hold.

**Then close the run.** A terminal summary is the short version of what just
happened: it collapses findings to fit, and it is gone when the session is. A
run that produced findings therefore ends with one offer to store it, said
plainly and in a line, never as a pitch:

> Want me to upload this run? It keeps the full findings with their citations
> where you can read them again and compare against your next run. I will show
> you exactly what leaves the repository first, and nothing goes without your
> say-so.

A yes goes to "Uploading a run" below, and that section is unchanged: build the
payload, print the consent preview in full, and wait. **The offer is not the
consent.**

On a no, ask once for feedback instead, and take that second answer as final
whatever it is:

> Understood, nothing leaves the repository. If you have a minute, anything you
> would change about this run is worth more to the people who build LexLint
> than the run itself.

Then stop. One offer, one fallback, no third ask, and silence is a no. Skip the
sequence entirely when the run found nothing, when the manifest did not end up
written, and in any headless or CI session, where there is nobody to ask and an
unanswered question reads as a prompt to act.

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
the same question `set_profile` already answers, off a request `check_access`
spends either way: asking both costs nothing extra, it just gives you the same
dates twice. Read them from `set_profile`, so there is one place to look, not two.

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
lexlint 1.30.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
cache: 5 jurisdictions held, 1 refreshed
```

Someone reading a citation is owed the knowledge of whether it was read from
the corpus this minute or from a copy taken yesterday.

Domain resolutions need none of this. `profile.domains` in `lexlint.yml`
already records them, so a domain sitting there is not resolved a second time.

## The severity model

| Severity | Meaning |
|----------|---------|
| `warn` | Something to act on. Three different things arrive this way, and `kind` tells them apart: a live obligation applies to the declared profile (`obligation`); a jurisdiction-wide crawl-law attribute LexLint flags as worth acting on, such as an unsettled or restrictive posture (`posture`); or LexLint lacks current data for a declared jurisdiction (`coverage`). |
| `info` | Context, not a live duty on you. Three different things arrive this way, and `kind` tells them apart: an instrument LexLint cannot say is currently binding (`pending`); a jurisdiction-wide statement of how the local law treats crawling as a whole (`posture`), which cites nothing and binds nobody on its own; and a note about what was not reported (`coverage`), such as instruments that exist but no longer bind. |

LexLint never reports an `error` severity. A lint cannot be sure an activity is
prohibited rather than merely regulated, and it will not assert unlawfulness on
the strength of a matched instrument. Treat a live `warn` obligation as the
thing to act on.

Every finding carries `as_of_date` and `stale`, because laws change faster than
corpora do. A stale finding is still worth acting on; it just may lag the law.

Findings also carry a `kind`:

| `kind` | Meaning |
|--------|---------|
| `obligation` | A specific instrument binds the declared profile. |
| `coverage` | A note about what was not reported, never a pass: LexLint could not read something, holds no data, cannot map what it holds to a declared activity, or holds an instrument that no longer binds. |
| `posture` | How this jurisdiction's law treats crawling as a whole: whether browsewrap binds, what weight robots.txt carries, whether a public page is outside computer-crime law. Jurisdiction-wide attributes rather than instruments, so they bind nobody on their own and cite nothing. They appear only when `crawls_web` is declared. |
| `pending` | An instrument LexLint cannot say is currently binding: proposed or in committee, enacted with a future effective date, enacted with no commencement date on record, enjoined by a court, or carrying a status LexLint has no policy for. An injunction can be lifted and a missing commencement date does not mean the law never took effect, so treat this as a duty to watch, not one to ignore. |

A `posture` finding whose value is `unsettled` is a warning, not a pass. "The
law here is silent, untested, or in flux" is among the most actionable things a
crawler author can be told.

## Sending feedback and uploading runs

Two tools write rather than read. `submit_feedback` sends the developer's own
words about LexLint to the people who build it. `upload_lint_run` stores one
completed run on the LexLint portal, against the account the key belongs to.
Both follow the same consent rule: run only on an explicit yes from the
developer, given this session, never assumed and never inferred from the
plugin being installed or from what a previous session agreed to. Never
run either in a headless or CI session, where there is nobody to approve
anything.

**Step 7 is the one place either tool may be raised unprompted**, and it is
written out in full there: one offer of the upload, and one invitation to
send feedback if that offer is declined. Everywhere else, never volunteer
either one. Raising a tool is not running it, and step 7 changes nothing
below this line: the payload preview and the explicit yes still stand
between an offer and a call.

A run reaches the portal only on the developer's own explicit upload, this
session, and from then on it is kept against their UnGovr account. A plain
lint run never leaves the repository, and the offer that ends step 7 is an
offer: nothing below sends anything without the yes it asks for.

The developer can delete a run or delete a project at any time from the
portal. Deleting a run removes it immediately and its stored payload is
purged within 30 days; deleting a project removes it, and everything under
it, right away. The developer can also export a project's own runs as
JSON. A run can be shared by an unguessable, expiring link that works
without signing in, and revoking it deletes the link immediately, not
merely marks it inactive.

### Sending feedback

`submit_feedback` sends the developer's feedback on LexLint to the people who
build it, recorded against their UnGovr account so we can write back.

**Never read the session transcript to build the summary**: a key pasted into
a session is recorded there, and a summary built from one would carry the
developer's own key to us.

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

Nothing else about a session is collected automatically by LexLint. The key is
an UnGovr Open Data key, and that API keeps a request log of its own, set out
at https://www.ungovr.org/open-data/api-keys and holding which collection was
asked for and a one-way hash of the key, never which jurisdiction was looked
up.

### Uploading a run

`upload_lint_run` stores one complete lint run on the LexLint portal, against
the account the key belongs to, and hands back the portal URL. It is the only
way a run ever leaves the repository: nothing else in this procedure sends
findings, work items, or the manifest anywhere. A run is stored only on the
developer's own explicit upload, this session, and only against their own
UnGovr account.

**Preconditions.** Two things, and they are the two the payload is built out
of: the `run_lint` response from a completed `/lexlint` run in this session,
and a `lexlint.yml` on disk carrying `app` and `profile`. Missing either one,
do not build a partial payload: say so, run `/lexlint` first, and stop.

**A manifest with no `lint:` block is not a missing precondition.** The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by step 4 and step 5, and step 5 waits on an approval that may not have
come yet. Upload the run and say the work items are empty. Stopping here
instead strands a completed run behind an unrelated approval gate, which is the
defect this paragraph exists to close.

**Build the payload.** It is the versioned object `schema:
"ungovr.lexlint-upload/1"`, `generated_at` (now, in UTC), `client_version`
(`1.30.0`), `payload_hash`, and `record`. Take each part from whatever
owns it, which is not all one file:

- `record.app`: the manifest's `app` block, with `scope` set to what this run
  actually read. Verbatim is right for every other key, and wrong for this one
  whenever the scope came from the request rather than the file: a one-off
  scope is deliberately never written to the manifest, so copying `app`
  wholesale uploads a run over one directory with no scope at all, and the
  portal captions it `whole repository`. Nothing downstream catches it. When
  the run read the whole repository, leave `scope` off.
- `record.profile`: the manifest's `profile` block, verbatim.
- `record.lint.findings`: **this session's `run_lint` response**, which is the
  run being uploaded. Where the manifest's merged block covers this same run,
  carry `state`, `where`, `note` and `handled_by` across per finding id, the
  same four fields step 4 carries: they are the developer's, and the run has no
  opinion about them. The set of findings is always the run's.
- `record.lint.work_items` and `record.lint.vanished`: the manifest's,
  verbatim, when its `lint:` block is from this run. Otherwise `work_items` is
  empty. **Triage that lives only in this conversation never uploads**: a plan
  the developer has not approved and the repo does not hold is not part of the
  record, and sending it files their name to work items they never agreed to.
- `record.envelope`: the run's own metadata, at minimum `corpus_built_at`
  from that same `run_lint` response, so the portal can show how current the
  corpus was when the run happened.

**Never pair one run's findings with another run's envelope.** A committed
manifest normally holds the *previous* run's `lint:` block, so copying it
wholesale while `corpus_built_at` comes from today's run files a run that never
happened: older findings stamped with a newer corpus date. Nothing downstream
catches it. The hash is computed over whatever you assembled, so it matches,
and the server accepts it. Compare the manifest's `lint.run_at` and its finding
ids against the response in hand, and on any disagreement treat the block as
the previous run's and take only the four overlay fields from it.

Never put into the payload: the API key or any other credential, source
files, prompts or transcripts, or git usernames, emails, or remote URLs. None
of those are part of the record schema, and none belong on a page anyone but
the developer can see.

**Compute `payload_hash` exactly.** It is the sha256 hex digest of the
canonical JSON encoding of `record`, and the server recomputes that same
digest from the `record` you send and refuses the upload on any mismatch, so
"close" does not pass. Canonical means three things together: object keys
sorted, the two JSON separators tightened to `,` and `:` with no space after
either, and every non-ASCII character left as raw UTF-8 rather than
backslash-escaped. That is exactly what Python's `json.dumps` returns when
called with `record`, `sort_keys=True`, `separators=(",", ":")` and
`ensure_ascii=False`, hashed with `hashlib.sha256` and hex-encoded:

```python
hashlib.sha256 (json.dumps (record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode ()).hexdigest ()
```

That is the reference for any language, not only Python: reproduce the three
properties above exactly, not "compact JSON" in general, because a library's
own default separators or its own escaping of non-ASCII characters will not
match the server's and the upload will 400.

**With `jq` and a hash tool you never need the bytes at all.** Write `record`
to a file and canonicalize and hash it on disk. This is byte-identical to the
reference above, because `-S` sorts keys at every level, `-c` gives exactly the
two tight separators, and jq emits raw UTF-8 rather than escaping it:

```bash
jq -cS . record.json | tr -d '\n' | sha256sum | cut -d' ' -f1
```

`tr` removes the newline jq adds, which is not part of the digest. On macOS use
`shasum -a 256` in place of `sha256sum`. Together with posting the file
directly, this means the payload is built, hashed and sent without one byte of
it passing through you, so a 100 KB record costs what a small one does.

**Numbers are the one place the two can part, so check for them rather than
assuming.** No part of a record is *supposed* to hold one: nothing in the
upload schema declares a numeric field, and a `run_lint` response carries no
numbers at any path. But `app`, `profile`, `lint` and each finding are all
deliberately open to fields a newer client might add, and `app` and `profile`
are copied out of the developer's own `lexlint.yml` verbatim, so "supposed to"
is not the same as "cannot". Two commands settle it, on the same file you are about to hash. Both should
answer `0`:

```bash
jq '[.. | numbers] | length' record.json
jq -r '.. | strings' record.json | grep -c $'\x7f'
```

The first counts numbers. **The second is for one character, and it is the
only non-number case where the two encoders part: DEL, U+007F.** The reference
writes it as a raw byte and jq writes the six-character escape `\u007f`, so a
record carrying one hashes two different ways while the number count still
answers zero. It is checked at the value level rather than by grepping the
file, because the character can arrive either as a raw byte or as a `\u007f`
escape in the manifest and only the parsed value shows both. Every other
control character, every C1 byte, U+2028 and U+FEFF all agree.

**Both zero, and the pipeline is exact.** Either one non-zero, and something
arrived from the manifest rather than from LexLint: look at it, and hash the
record with the reference implementation instead of the pipeline, saying in
the report that you did.

The reason to know the rule anyway is that it is not a short list of
exceptions you can check off. jq passes the number literal through as you
wrote it; the reference re-renders whatever it parsed. So they differ for any
literal that is not already exactly what the reference would print, and that
is more shapes than it sounds:

- `1e3` and `1E3` both become `1000.0` through the reference, and `1E+3` to jq.
- `0.1234567890123456789` keeps its digits in jq and rounds to
  `0.12345678901234568` through the reference, which holds it as a double.
- `1.7976931348623157e309` becomes `Infinity` through the reference, which is
  not JSON at all.
- `-0` becomes `0` through the reference, which reads it as an integer and
  drops the sign, while jq keeps `-0`.

Those are illustrations, not a checklist: treat any number you type as
suspect. If a record ever genuinely needs one, compute the digest with the
reference implementation rather than the pipeline, and note in the report that
you did.

Without both tools, use the reference implementation in whatever language you
have, and if that means the payload passes through your own output, that is the
cost rather than a fault: say so once at the end, as "Three tools that make
this cheaper" describes, and upload normally.

**Show the consent preview, then wait.** Before calling the tool, print
exactly what is about to leave the repository:

| Field | Value |
|---|---|
| Findings | 31 |
| Jurisdictions | `us` `us/ca` `eu` +3 more |
| Work items | 5 |
| Size | 14.2 KB |
| Destination | the account of key `ung_live_<prefix>...` |
| Payload hash | the sha256 hex digest just computed |

Give the jurisdictions cell the same three-and-a-count treatment as
everywhere else in this procedure, and name the full list in a line under the
table when there are more than three. **When the work items are empty because
the manifest holds no merged block, say so in that cell** ("0, the manifest
holds no merged run yet") rather than printing a bare zero: the developer is
approving what leaves, and an unexplained zero next to 31 findings reads as a
bug in the preview. For the destination, read the key from
wherever it persists for this client, the same place the setup steps above
read it from, and show only its first sixteen characters (`ung_live_` plus
seven more) followed by `...`, the same truncation the settings page itself
uses. Never show more of the key than that, and if you cannot find where it
persists, say the destination is unknown rather than guessing at it.

Then ask for an explicit yes. **No yes, no call.** Not because the plugin is
installed, not because a previous session said yes, and never in a headless
or CI session, where there is nobody to give one.

**Send the payload from disk rather than through your own output.** A real
payload is around 100 KB of legal text, and passing it as a tool argument means
reproducing every one of those bytes in your own output, where the server's
hash check turns the smallest slip into a refused upload. The relay buys
nothing: these tools are ordinary JSON-RPC over HTTPS, and the key you already
hold authenticates a direct call. Write the request to a file, with the payload
nested where the tool call expects it:

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
 "params": {"name": "upload_lint_run",
            "arguments": {"payload": {"schema": "ungovr.lexlint-upload/1"}}}}
```

then post that file:

```bash
curl -sS https://mcp.lexlint.org/mcp \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $UNGOVR_API_KEY" \
  --data-binary @upload-request.json
```

No `initialize` call first, no session to carry, and no `Accept:
text/event-stream`: the server keeps no state and answers a plain JSON POST
with plain JSON. Read `run_url` and `duplicate` out of the reply exactly as you
would out of a tool result.

**Then delete both files, and write them outside the repository in the first
place.** There are two: the request, and the `record.json` the hash pipeline
above reads. Each holds the complete findings and the developer's own triage,
and a file left in the working tree is a file that gets committed by the next
`git add .` This procedure says elsewhere that nothing about an upload is
recorded in the repo, and a stray `record.json` in the project root is exactly
that record. Put both in a temporary directory, delete both when the reply is
read, and if a write outside the repository is not possible, delete them
immediately and say in the report that they existed. On a machine other people can read, keep the key out of the process
list by handing curl its configuration on standard input instead of passing
`-H`:

```bash
curl -sS --config - <<CFG
url = "https://mcp.lexlint.org/mcp"
header = "Content-Type: application/json"
header = "X-API-Key: $UNGOVR_API_KEY"
data-binary = "@upload-request.json"
CFG
```

**`curl` works against this endpoint and Python's `urllib` does not.** The
identical request from `urllib.request` comes back `403` with Cloudflare error
`1010`, "browser signature banned", because the edge in front of this endpoint
refuses that client's signature. That is a fact about our edge rather than
about your machine, so try a second ordinary client before concluding the route
is closed. Not doing that is what cost the first session to try this several
steps.

**A blocked client is never a reason to forge an identity.** Do not set a
`User-Agent` to look like a browser or like some other tool, here or anywhere
else: it circumvents an access control the operator chose, and the operator
being us changes nothing about that. Where no ordinary HTTP client is
available, call `upload_lint_run(payload)` as a tool and accept the relay. That
path works, and it is not going away.

**Report what came back, by whichever route sent it.** On success, print the
returned `run_url` and say the run is stored. If `duplicate` came back true, say the run was
already stored under that URL rather than uploaded again: the portal keys on
the account and the payload hash together, so re-sending the same run is
always safe and never files a second copy.

If the call fails outright, say plainly that nothing was stored, give the
reason, and offer to try again. If the connection drops after the request was
sent, the state is unknown rather than failed: say that plainly too, and offer
to retry rather than assuming either outcome, because the upload is
idempotent per payload hash and a retry never creates a duplicate.

**Record nothing about the upload in the repo.** No run URL, run code, or
receipt goes into `lexlint.yml` or anywhere else in the working tree. The
portal resolves which project a run belongs to from `app.name` alone, on its
own side, so there is no local identifier to track and nothing here for
`.lexlint/` or any other cache to hold.

## What this is not

LexLint is a research summary, not legal advice, and not authorization to access
any system. It does not certify anything. A clean run means the basics were
checked against the data LexLint holds today, in the jurisdictions you declared,
for the activities you declared. It does not mean you are in the clear.

Full documentation: https://mcp.lexlint.org/

A worked example, end to end: https://mcp.lexlint.org/example
