<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# Step 3 in detail: set the profile, then run the lint

**Show the developer the two lists before you send them**, and their
`public_sector`, `regulated_sector` and `roles` answers beside them when the profile has
them, with every value you are unsure of marked as such, and wait for their
answer. What goes is
what they would have sent, and a value they strike or add changes the whole
lint: every finding downstream is drawn by one of these values. That holds on
a re-run as well, when the lists come out of a committed `lexlint.yml`: say
that they do, and mark any value the code no longer seems to support. In a
headless or CI session nobody can answer: send the lists as you read them,
and name the values you were unsure of in the report, in step 7, beside the
findings each one is carrying. The exceptions are `public_sector`,
`regulated_sector` and `roles`, which are never sent as you read them: send each only when
the developer or the committed manifest gave it, and otherwise leave it out.

```
set_profile(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"],
  public_sector=["none"],  # the developer's answer, not a default; omit if not given
  regulated_sector={"financial": "none"},  # likewise; only with provides_financial_services or a class
  roles={"ai_system": ["deployer"], "personal_data": ["controller"]}  # likewise
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
  strings the next run will send. It carries `public_sector`,
  `regulated_sector` and `roles` when you sent them; send every field of it to `run_lint`.

**The `set_profile` call costs one upstream request, separate from
`check_access`'s own.** It answers the same coverage question that passing
`jurisdictions` to `check_access` would have answered, and that argument rides
a request `check_access` spends either way, so asking both just repeats the
answer. Neither order costs more.

```
run_lint(
  activities=["crawls_web", "generates_content"],
  jurisdictions=["us", "de", "eu", "kr"],
  public_sector=["none"],  # the same answer set_profile was given
  regulated_sector={"financial": "none"},  # likewise
  roles={"ai_system": ["deployer"], "personal_data": ["controller"]},  # likewise
  client_version="1.57.0"
)
```

The same declaration, from the profile you just had blessed, plus your own
`client_version`. The version is not part of the profile and never goes into
`lexlint.yml`: it describes the plugin making the call, not the app being
linted.

**Never send `brief`.** It exists for a client with no procedure, which shows
each finding as one line. This procedure writes `lexlint.yml` and builds work
items from fields a brief finding does not carry, and a brief run merged into
the manifest would drop them.

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
   can make any call they make. This skill ships no recipe for that call, so
   take this route only if you already know how to make it, and otherwise take
   route 3. Needs a shell and an HTTP client. This also spends the upstream
   requests a second time, which is the real price of the route, so say so on
   the quota line.
3. **Split the declaration across several `run_lint` calls and union the
   results.** Needs no shell and no tools beyond the ones already in front of
   you, so this is the route when you cannot run a command at all.

**Route 3, in full, because it is the one with no fallback behind it.**
Nearly every finding is per jurisdiction and per instrument, and those do not
depend on what was declared beside them: a slug returns the same findings
called alone as it does called with five others, with the same ids. So call
`run_lint` with one jurisdiction, or a few, until every declared slug has been
covered exactly once, and treat the union as the run. Every call carries the
same `activities`, the same `public_sector`, the same `regulated_sector` and the
same `roles`, or the union mixes routed and unrouted findings.

**One finding is not per jurisdiction, and it is the reason this route needs a
rule rather than just an instruction.** A finding whose `id` begins
`activity:` says the law library tags no instrument anywhere for a declared
activity, so that activity is unlinted rather than clean. It carries
`jurisdiction: null` because it is about the run, not about a jurisdiction,
and the run that answers it is the call: `run_lint` reports it when nothing in
**that call's** jurisdictions carried the tag. Split the calls and each one answers a
smaller question than you asked.

So **`activity:` findings are intersected across the calls, while everything
else is unioned.** An activity is genuinely unlinted only when **every** call
reported it; a single call omitting it means some jurisdiction did carry the
tag, and the warning is wrong for the declaration as a whole. Getting this
backwards produces a coverage warning about law LexLint actually holds,
which is the one kind of false alarm that teaches a developer to skim the
coverage section.

These activities can raise it, because the law library maps them on the flag
axis alone: `automated_outreach`, `processes_voice`, `processes_biometrics`,
`publishes_adult_content`, `operates_social_platform`, `serves_minors`,
`operates_app_store`, `ships_mobile_app`, `aggregates_content`,
`distributes_software_product`, `handles_health_records`,
`provides_financial_services`, `operates_essential_service`,
`is_listed_company`, `provides_telecom_services`, `statutory_requests`,
`records_calls`, `records_text_chat`, `tracks_devices`, the license classes
`is_bank`, `is_lender`, `is_insurer`, `is_securities_firm`,
`is_payment_provider` and `is_crypto_asset_provider`. Those are ordinary
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
  them, the law library was rebuilt underneath you and the union is two runs wearing
  one date, which this procedure forbids everywhere else it can happen (see
  "Never pair one run's findings with another run's envelope"). Start again from
  the first call. Expect this rather than treating it as bad luck: the law
  library rebuilds daily, and a split run is the one shape that can straddle the
  rebuild.

**Unwrap the file before reading anything out of it, because the routes hand
you different shapes.** A client's tool-result file usually holds the lint
itself. A file written by an HTTP client holds the JSON-RPC envelope around it,
and the lint sits inside that in one of two places: as `result.structuredContent`
(always on `https://mcp.lexlint.io/rpc`, and on `/mcp` when the call carried
the `MCP-Protocol-Version: 2025-06-18` header), or only as a JSON *string*
inside `result.content[0].text`. On `/rpc` the text block is a one-line pointer
and not the lint, which is why the typed copy is tried first. Normalize once,
and work only from what comes out:

```bash
jq -e '
  if .error then
    "the server returned an error, not a lint: "
      + (.error.message // "no message") | error
  elif (.result.structuredContent? // null) != null then
    .result.structuredContent
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

**Then show the run, before you merge anything.** Print what came back in the
shape https://lexlint.io draws a run in: three lines saying what was linted, a block
for each finding the developer should read first, and a count. It is their
first look at the run, so it comes straight after `run_lint`, before step 4's
merge and step 5's plan, on every run that returned a lint.

```
declared     generates_content, crawls_web
operates     🇪🇺 European Union, 🇨🇦 Canada, US-California
law library  2026-09-30

WARN  🇨🇦 Canada  PIPEDA breach of security safeguards regime · in force since 2018-11-01
      Requires an organization to report to the Privacy Commissioner, and to
      notify the affected individual directly, any breach of security
      safeguards involving personal information under its control where it
      is reasonable to believe the breach creates a real risk of significant
      harm.
      read against its source 2026-09-02 · https://lexlint.io/l/ca-s-c-2000-c-5-ss-10-1-10-3

WARN  🇪🇺 European Union  AI Act, Article 50 (transparency obligations for AI systems and synthetic content) · in force since 2026-08-02
      Providers of AI systems that interact directly with people must ensure
      users are informed they are dealing with an AI system unless obvious
      from context, and providers of generative AI must mark synthetic audio,
      image, video, or text output in a machine-readable, detectable format.
      read against its source 2026-08-14 · https://lexlint.io/l/eu-2024-1689-50

WARN  US-California  California AI Transparency Act (SB 942, as amended by AB 853) · in force since 2026-08-02
      A covered provider of a generative AI system must offer a manifest
      disclosure option (a visible AI-generated content label), embed a
      latent disclosure of machine-readable provenance data in content it
      creates, and provide a free public AI-content detection tool.
      read against its source 2026-08-14 · https://lexlint.io/l/us-ca-cal-bus-prof-sections-22757-22757-6

INFO  US-California  AB 2839, election materially deceptive deepfake disclaimer law · blocked by a court
      blocked 2025-08-29 by Kohls v. Bonta (United States District Court for the Eastern District of California)
      As enacted, prohibited knowingly distributing, with actual malice,
      materially deceptive AI-generated election media within specified
      windows around an election, and required a conspicuous manipulation
      disclaimer for satire or parody content to qualify for that exemption.
      read against its source 2026-08-14, for counsel · https://lexlint.io/l/us-ca-cal-elec-20012

4 of 94 findings: 3 for code, 1 for counsel
The other 90: 69 warn, 21 info. All of them go into lexlint.yml in step 4,
and the plan in step 5 works through them.
```

It is fenced, like the status line: it is a printout, and its columns only line
up in a fence. The words are the ones "How to show a list" (in `SKILL.md`) asks for: a
jurisdiction is `jurisdiction_flag`, a space and `jurisdiction_name`, never a slug, and a
state has its country code and no flag; when a law binds is `in_force.words`,
verbatim. A fence prints a markdown link as its text, so each block's link is
the bare `note_url` at the end of its last line, which a terminal makes
clickable. With no `note_url` the line ends at the date: never build the URL.

**The three lines at the top.** `declared` is the activities you sent, in the
order you sent them, then `public_sector`, `regulated_sector` and `roles` when
the profile carried them.
`operates` is each jurisdiction you declared, by flag and name, read off a
finding for that slug; a slug no finding names stays a slug, which is the gap
it marks. `law library` is the day of the reply's `corpus_built_at`.

**Which findings get a block.** Three kinds, each once:

- **The lead for each declared jurisdiction**: its `warn` obligation that is in force
  (`in_force.state` is `in_force`) and `present`, preferring one with a
  `note_url`, and the newest `effective_date` among those.
- **Every finding for counsel**, whatever its severity. A finding is for
  counsel when `settledness.band` is `unsettled` or `lifecycle.band` is
  `blocked`: the law library routes it there, and you do not.
- **Every coverage warning.** A declared jurisdiction LexLint holds nothing
  for is never left out of a report, and this is the first report.

Warns first, then infos. A block is the severity upper-cased, the jurisdiction,
the law's name (the part of `summary` before its first ": "), a `·` and
`in_force.words`; then, where a court has acted on the law, its court lines;
then the rest of `summary`, whole and never cut, wrapped at
about 76 columns under a six-space indent; then `read against its source` and
the day of `as_of_date`, `, for counsel` when it is, and the link. A coverage
warning has no law and no date: its block is its first line with `summary`
after the jurisdiction.

**The court lines.** A finding carries `court_action` when a court has
blocked the law, struck it or part of it down, or upheld it after a block, or
when a suit against it is pending. Each ruling gets a line under the block's
first line, at the same indent: what the court did, with the parts of the law
it reached when it reached only some, the day, the ruling and its court, and
where the ruling stands now. A pending suit adds `under challenge in court`,
and never a name: the law library does not name it. The command below writes
these lines after the lane, one per column, in the order to print them. They
are the law library's words; print them as they come, and never name a court
or a ruling the lint did not.

**Then the count, and then the rest.** `N of M findings: X for code, Y for
counsel` counts the blocks you printed, and the line under it counts every
finding you did not print, by severity, and says where each one goes. Nothing
is dropped: the manifest carries every finding the run returned, and the plan
reads all of them. A run that printed every finding it returned says "That is
all of them." there instead. "For code" and "for counsel" are the law library's
routing, for this first look; the lanes the work goes into are step 5's.

**A law arrives once however many declared jurisdictions reach it.** A child declared
beside its parent mirrors the parent's findings (step 4 says how), so the block
reads each law once, by its instrument key and the slug it was read from, and
the count says so: "4 of 90 instruments (94 findings, 4 of them a parent's law
again)", never a bare total. A split run (step 3) is one run here too: read
every call's file at once, as the command below does for `lint-*.json`.

This prints the blocks' rows from the unwrapped `lint.json`, then the two
count lines, so the run is read in one slice rather than whole. For a split
run, feed it `jq -s '{findings: map(.findings) | add}' lint-*.json` instead of
the file:

```bash
jq -r '
  def counsel: (.settledness.band == "unsettled") or (.lifecycle.band == "blocked");
  def law: [(.id | sub("^[^:]*:"; "")), .jurisdiction];
  def ruling: ((.provisions // []) | join(", ") | if . == "" then "" else . + " " end)
              + ({"enjoins": "blocked", "invalidates": "struck down", "upholds": "upheld"}[.role] // .role)
              + (if .decided then " \(.decided)" else "" end)
              + " by \(.name)" + (if .court then " (\(.court))" else "" end)
              + (if .stage then "; now \(.stage.word // .stage.stage | ascii_downcase)"
                                + (if .stage.date then " \(.stage.date)" else "" end) else "" end);
  def courtlines: [(.court_action.rulings // [])[] | ruling]
                  + (if .court_action.under_challenge then ["under challenge in court"] else [] end);
  def lead: [ .[] | select(.severity == "warn" and .kind == "obligation"
                           and ((.certainty.resultset // "present") == "present")
                           and .in_force.state == "in_force") ]
            | group_by(.resolved_from // .jurisdiction)
            | map(sort_by(.effective_date // "") | reverse | sort_by(.note_url == null) | .[0]);
  (.findings | length) as $total
  | (.findings | group_by(law) | map(sort_by(.resolved_from != null) | .[0])) as $all
  | ([$all | lead[]] + [$all[] | select(counsel)]
     + [$all[] | select(.kind == "coverage" and .severity == "warn")]
     | unique_by(law) | sort_by([(.severity != "warn"), .jurisdiction])) as $shown
  | ($shown[] | [.severity, (.jurisdiction_flag // ""), (.jurisdiction_name // .jurisdiction),
                 (.in_force.words // ""), .summary, (.as_of_date // ""), (.note_url // ""),
                 (if counsel then "counsel" else "code" end)] + courtlines | @tsv),
    ("\($shown | length) of \($all | length) "
     + (if $total > ($all | length)
        then "instruments (\($total) findings, \($total - ($all | length)) of them a parent\u0027s law again)"
        else "findings" end)
     + ": \([$shown[] | select(counsel | not)] | length) for code, \([$shown[] | select(counsel)] | length) for counsel"),
    "not shown: \([$all[] | select(.severity == "warn")] | length - ([$shown[] | select(.severity == "warn")] | length)) warn, \([$all[] | select(.severity == "info")] | length - ([$shown[] | select(.severity == "info")] | length)) info"
' lint.json
```
