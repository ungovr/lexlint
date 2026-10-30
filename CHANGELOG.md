# Changelog

Each release of the LexLint plugin bundle since 1.40.0, newest first. Update
the plugin in your client to get the newest. In Claude Code that is
`claude plugin update lexlint@lexlint`, then restart your session. The bundle
is published at https://github.com/ungovr/lexlint

## 1.64.3 (2026-10-29)

- The bundle's descriptions now name export-control law among the topics the
  lint reads: what software must clear before it is exported or offered abroad,
  namely the classification and authorization an encryption item needs, the end
  users and end uses an export may not reach, and the comprehensively sanctioned
  destinations it may not go to. The law library holds no laws in it yet, so
  every run reports it as not yet researched for each jurisdiction until its
  first laws load. Nothing you declare or call changes.

## 1.64.2 (2026-10-29)

- The bundle's descriptions now name cloud-service law among the topics the lint
  reads: what a provider of a hosted cloud service owes its customers, namely
  switching and exit, limits on switching and egress charges, interoperability,
  and safeguards against foreign governmental access to the data it holds,
  starting with the EU Data Act. Only a run that declares
  `provides_cloud_services` is told a jurisdiction's cloud-service law has not
  been researched; every other run is unchanged. Nothing you declare or call
  changes.

## 1.64.1 (2026-10-29)

- The topics LexLint reads now include digital identity and e-signature law:
  the duties a service takes on when it relies on a digital identity wallet, a
  credential or an attestation, and when an electronic signature or record
  counts. The law library holds no laws in it yet, so every run reports it as
  not yet researched for each jurisdiction until its first laws load.

## 1.64.0 (2026-10-29)

- A new activity, `ships_consumer_interface`: your product has a website, app or
  other screen that members of the public use to buy, book, read or reach a
  service. It is something your software does, so the code can show it: public
  pages, app screens, a storefront, a booking or sign-up flow. A tool only your
  own staff use does not count. Declare it beside `ships_mobile_app` when the
  app is both.
- It is the trigger for digital-accessibility law. No law in the library is
  tagged with it yet, so declaring it today adds a coverage line and no finding;
  findings arrive once the first documents load. No other activity implies it
  and it implies nothing, so every existing declaration is answered as before.

## 1.63.1 (2026-10-28)

- The bundle's descriptions now name digital-accessibility law among the topics
  the lint reads: what a product you sell, or a service you offer to the public,
  must do so that people with disabilities can use it, starting with the
  European Accessibility Act, which has applied since 28 June 2025. Until a
  jurisdiction's accessibility law is researched, a run there says so as a
  coverage warning. Nothing you declare or call changes.

## 1.63.0 (2026-10-28)

- A sixth role, `provides_cloud_services`: the company behind your app offers
  it to customers, under a contract, as a hosted service that stores or runs
  their own data or workloads (infrastructure, platform or software as a
  service). Running your own app on somebody else's cloud is not this role.
  Like the other roles it is your answer, never something read from the code.
- Declaring it today reaches the cybersecurity laws that bind any
  organization, as every role does. The cloud-provider duties in the EU Data
  Act, such as the end of switching charges on 12 January 2027, reach it once
  they are in the law library.

## 1.62.0 (2026-10-28)

- A law's name now arrives whole, as its own `name` field on every instrument
  finding. Some names hold a colon themselves, such as "High-Risk AI:
  Public-Authority Deployer Obligations", and the run's first look used to cut
  the name at its first colon, so half of it opened the sentence beneath. The
  first look now prints `name` whole and the rest of `summary` under it.
- `summary` is unchanged, and so is every finding id. The next merge writes
  each instrument finding's `name` into `lexlint.yml`, one line beside its
  `summary`, and moves nothing else.

## 1.61.0 (2026-10-27)

- `generates_content` has four media kinds under it: `generates_text`,
  `generates_images`, `generates_video` and `generates_audio` (speech, singing,
  music and other sound). Declare each kind of output your software makes, and
  `generates_content` comes with it. A rule written for one medium, such as a
  voice-cloning law, then reaches only software that makes that medium.
- A declaration that names `generates_content` and no kind is answered exactly
  as before, with every kind's rules, and each jurisdiction where a kind would
  narrow them has an `info` line, `<slug>:medium-undeclared`, counting those
  findings. `set_profile` asks which kinds.
- A kind is something your software does, not who you are, so a library or
  framework may declare one in its ACTIVITIES.md.

## 1.60.1 (2026-10-26)

- Step 4's merge script now writes its temporary file under a new name it
  creates for itself, so a link committed in a repository under the old fixed
  name can no longer send the write to a different file. Update if you run
  LexLint in repositories you did not write.
- A finding whose text carries a control character, such as the residue of a
  statute extracted from a PDF, is written so that the next merge can read
  `lexlint.yml` back. Before, one such character could leave the file
  unreadable until it was edited by hand.
- A key inside a finding's nested fields is quoted whenever YAML would read it
  as something else, so no key can add a line of its own to `lexlint.yml`.
- Where the merge script has to be fetched rather than run from the skill,
  step 4 puts it in a new private directory from `mktemp -d` instead of a
  fixed name in `/tmp`, and runs it only when it names this bundle's own
  version. Nothing you declare or call changes.

## 1.60.0 (2026-10-26)

- Three starter prompts in the Codex manifest (`interface.defaultPrompt`), the
  ones a client shows before the first message. The first asks for a lint and
  names no app, so your agent asks which app to lint; the other two look up
  the law and need no account.
- The skill and `AGENTS.md` alike say to lint only an app whose code your
  agent can open: the folder you have open, a public repository, one you
  connected, or code you paste into the chat. When you ask for a lint without
  saying which app, your agent asks, offering the
  open folder first when there is one. When no repository is open, as in a
  chat on a phone or on the web, it also asks where the code is, and it does
  not build a declaration from a description. Where it can open the code but not write
  to it, it shows the confirmed `lexlint.yml` for you to commit.

## 1.59.0 (2026-10-24)

- A new finding kind, `derived`, off by default. Add `derived: true` to the
  `profile` in your `lexlint.yml` and a run adds one finding per record an app
  holds to meet the deadlines the matched laws set: a recorded moment for each
  start an incident-notification deadline counts from (`derived:event_time`),
  and a recorded jurisdiction of residence or location for each affected
  person (`derived:jurisdiction_signal`). Each is always `info`, is about the
  run rather than one jurisdiction, and lists every law it rests on, with
  whether that law states the record or LexLint infers it. It stays off unless
  you ask for it while its wording is under legal review.
- `derived` is a new optional profile key, `true` or `false`, accepted by
  `set_profile`, `run_lint` and `upload_lint_run` and by the schema's
  `profile`. With no key the server default applies, which is off.
- Six fields on a derived finding, all additive. Five are new: `capability`
  (the record, as `key` and `words`), `stated_by` and `inferred_from` (how many
  of the listed laws name the record themselves, and how many LexLint infers it
  from), `derived_from` (each law it rests on, with its bases) and `moments`
  (on `derived:event_time` only, each start a deadline counts from). The sixth
  is `basis`, which posture and customer-duty findings already carry; here it
  says what the listed laws state and what LexLint infers. A derived finding's
  `id` begins `derived:`, and the schema's `kind` enum gains `derived`.
- The skill and `AGENTS.md` alike describe the kind in the severity model.
  The skill tells your agent never to ask about `derived`, to send the key
  through `set_profile`, `run_lint` and the upload exactly as your manifest
  holds it, to triage each derived finding as one code work item titled by its
  `capability.words`, with no `jurisdictions` key when it is the item's only
  finding, and to report its counts rather than its list of laws.
- The merge script carries the new fields into `lexlint.yml`, in the order the
  schema declares them.
- On a split run, where your agent divides one declaration across several
  `run_lint` calls, a derived finding in `lexlint.yml` covers only the
  jurisdictions of the first call carrying the id. The run stored on the
  portal is rebuilt whole and
  covers them all; run the lint unsplit to have the whole-run finding locally.

## 1.58.0 (2026-10-24)

- A new declaration question, `flows`: where your software stores or sends
  personal data across a border. Write it into `lexlint.yml` under
  `profile.flows`, one entry per route, for example `[{"from": "eu", "to":
  "us", "data": "personal", "basis": "contract_clauses"}]`, or `[]` when no
  personal data leaves the jurisdiction it was collected in. `data` is
  `personal` or `sensitive`, and `basis` is the transfer mechanism the route
  relies on: `adequacy`, `contract_clauses`, `binding_rules`,
  `certification`, `authority_approval`, `consent`, `derogation`, or
  `unknown`. Each cross-border transfer finding then names, in `flows`, the
  declared routes that leave its jurisdiction. No finding is dropped or
  downgraded on a flow yet, so a run shows the same findings with or without
  it.
- A jurisdiction with cross-border transfer findings carries one coverage
  line, `<slug>:transfer-flows`, counting them and saying what was declared:
  it asks for `flows` when they were not sent, and for the basis of any route
  declared as `unknown`.

## 1.57.0 (2026-10-22)

- The `lexlint` skill is now a directory: a short `SKILL.md` that your agent
  loads when the skill starts, and a `references/` folder of files it reads
  only when a step needs one, each named in `SKILL.md` with the moment to read
  it. That is the shape the Agent Skills standard asks for, which keeps
  `SKILL.md` under its size budget. A client that reads a long file in slices
  could miss a step of the old single file; now an agent loads the loop and
  its rules up front and the detail of each step as it reaches it. No rule has
  changed, only which file states it, except as listed here: the key, update,
  sign-in and one-run scope steps are now worded for any client, with each
  client's own command in `references/clients.md`, and `SKILL.md` gains a
  short list of the rules to know before a run starts. One step's wording
  changed as well: route 2 of the large-response step, in the skill and in
  `AGENTS.md` alike, now says that no recipe for that call ships and to take
  route 3 otherwise, instead of pointing at a recipe that does not ship.
- The split-run paragraph of the large-response step, in the skill and in
  `AGENTS.md` alike, now lists every activity that can raise an `activity:`
  coverage warning on a split run; it named 9 of the 25 by name.
- The commands each client declares (install, key, update, restart, sign-in
  and one-run scope) appear in the skill only in `references/clients.md`, its
  per-client setup steps, so the same skill reads correctly in every client
  that loads a skill folder. `AGENTS.md` stays one file.
- Each client's entry under Client setup, in `references/clients.md` and in
  `AGENTS.md` alike, now gives that client's restart step, which the key and
  update steps both end on.
- `SKILL.md` declares its license, what it needs to run (network access to
  the LexLint server, and python3 with PyYAML for the merge step) and this
  bundle's version in its frontmatter.
- The merge step's script ships as a file, `skills/lexlint/scripts/merge.py`,
  so your agent runs it where the skill is installed instead of writing a few
  hundred lines to a temporary file on every run. It is the same program
  `AGENTS.md` carries inline, byte for byte, has no execute bit, and makes no
  network call. The skill runs it with `python3` by its installed path, from
  your repository root, or with `uv run` the same way where python3 has no
  PyYAML: its header declares the dependency. If your client loads the
  skill's text without its files, the skill takes the same script from
  `AGENTS.md` instead.
- The merge script has a `--help` with worked examples, a `--dry-run` that
  prints the counts and writes nothing, and a distinct exit code for each way
  it stops (3 for a missing run file or an empty run, 4 for a manifest it
  cannot read or write, 5 for a run file of the wrong shape), with only its
  JSON summary on stdout and every message on stderr. An unreadable
  `--previous` manifest or a manifest that is not YAML now stops with a
  message instead of a Python traceback.
- `lint.tool` in your manifest is the `--tool` value the procedure passes,
  this bundle's own version, and the README's sample manifest shows that
  value instead of a long-stale one.
- The skill's `description`, the text your agent reads to decide whether to
  load the skill, is rewritten and measured. It now tells the agent to load
  the skill first, before touching code, when a change adds or alters what
  the app does with people, their data or other sites (collecting personal
  data, automated email or messages, a chatbot or other generative AI
  feature, training on user data, crawling, voice or face capture, decisions
  about people), even when the request never mentions law, and says what it
  is not for. On 22 labeled requests the old text loaded the skill on none,
  and the new one loaded it on every request it should and on none it should
  not. That was measured on the bundle without its commands, which is the
  shape this release ships (the next entry): until now, in Claude Code the
  `/lexlint` command shared the skill's name and its description was the one
  the agent read.
- If you decline a key, the sign-in or the lint itself, the skill now says in
  one line that the lint was offered and declined, and goes back to the
  request that brought it in. The lint is advisory and never blocks the work.
  `AGENTS.md` says the same.
- The plugin's four commands are skills now, and their names changed. In
  Claude Code lists them as `/lexlint:lexlint` (the lint),
  `/lexlint:lexlint-key`, `/lexlint:lexlint-upload` and
  `/lexlint:lexlint-feedback`, and asking in your own words loads the same
  skills. After `claude plugin update lexlint@lexlint` and a restart,
  `/lexlint`, `/lexlint-key`, `/lexlint-upload` and `/lexlint-feedback` are no
  longer commands. A typed short name can still reach its skill, as
  `/lexlint-key` did in a measured run, but the listed names are the ones to
  use.
  The reason is reach: a command was a Claude Code convention, while every
  client that reads a skill folder, Codex among them, now gets all four, and
  in Claude Code the old `/lexlint` command loaded in place of the skill it
  shared a name with.
- The key, upload and feedback skills are written from the same source as
  the lint, so their rules cannot drift from it. The key skill looks for a
  saved key before it offers a route, checks a key against the server before
  saving it, and sends your agent to your client's own entry in
  `references/clients.md` for where the key goes and how to restart.
- Passing a path with the request is now step 1 of the lint, for every
  client: a path ending in `.yml` or `.yaml` is the manifest, any other path
  is the scope for that run, both at once is the manifest first, a path that
  does not exist stops the run, and a scope from the request is never written
  to the manifest. In Claude Code that is `/lexlint:lexlint <path>`.
- The upload's consent preview, in the skill and in `AGENTS.md` alike, now
  lists the declared activities and, when the run carries them, the
  public-sector and regulated-sector answers, since the call sends them. The
  feedback step shows its payload in a block before it sends. `AGENTS.md` no
  longer names a Claude Code command in its upload section.

## 1.56.0 (2026-10-21)

- A sixth license class under `provides_financial_services`:
  `is_crypto_asset_provider`, for a crypto-asset or virtual-asset service
  provider (an exchange, custodian, broker, transfer service or token issuer),
  or software supplied to one. Declare it and the role comes with it, so every
  rule that binds any financial firm still reaches you; a rule written for
  crypto businesses alone now reaches only this class.
- `is_payment_provider` no longer covers crypto-asset service providers: it is a
  payment or e-money institution or a money transmitter. A crypto business that
  declared only `is_payment_provider` should add `is_crypto_asset_provider`:
  MiCA's rule on recording client communications now reaches the new class
  alone, so that finding stops appearing until you do. Rules that name both
  kinds of firm, such as Cyprus's DORA designation and Palestine's payments
  decree, reach either declaration. A business that also transmits money
  declares both classes.

## 1.55.0 (2026-10-20)

- The procedure now covers an install that signs in instead of using a key.
  When `check_access` reports `credential: "none"`, your agent skips the key
  steps and never mints a trial, reads the law straight away up to the free
  lookups `free_lookups` reports, and, when a tool asks for sign-in, tells you
  how for your client: `/mcp` in Claude Code, or the Connect prompt in the
  Claude apps. Signing in from Codex is not open yet, so Codex keeps using a
  key. An install that uses a key changes nothing.

## 1.54.1 (2026-10-17)

- A LexLint report now ends with the link to the stored run, on a line of its
  own, so it is the last thing you read instead of sitting above the findings.
- `/lexlint-key`'s check of a key now sets its own time limit, so it runs as
  written on a Mac. Nothing you declare or call changes.

## 1.54.0 (2026-10-17)

- A new declaration question, `roles`: which role the maker of your software
  holds under the EU AI Act (provider, deployer, importer, distributor,
  product manufacturer or authorised representative) and under the GDPR
  (controller or processor). Write it into `lexlint.yml` under
  `profile.roles`, for example `{"ai_system": ["provider"], "personal_data":
  ["processor"]}`. A duty line that binds a role you do not hold now sits in
  `requires_elsewhere` instead of `requires`, and the finding names the roles
  it was judged under in `role`. A run without it says how many findings an
  answer would move, in a coverage line per regime. Only the European Union's
  own rows are tagged by role so far.
- Each instrument finding carries `reading`: whose reading its lines are
  (LexLint's), the day research read the source, and the guidance and court
  rulings that also read the law, each with the day it was issued or the day
  LexLint recorded it.

## 1.53.2 (2026-10-15)

- `/lexlint` and `/lexlint-key` now say that the Claude desktop app never reads
  a shell profile, not even after a full quit and reopen. A key saved only in
  `~/.zshrc` or another profile is diagnosed as such, and the fix offered is
  `/lexlint-key`, which saves the key where every start of Claude Code reads
  it. The README's "Get a key" says the same. Nothing you declare or call
  changes.

## 1.53.1 (2026-10-15)

- LexLint's server now keeps a record of each request: what it was, which
  coding tool sent it, what kind of credential it carried, whether it
  succeeded, and the country and region of the connection. It holds no IP
  address, key or account, and nothing from what you linted. The README sets
  it out in full, under Feedback. Nothing you declare or call changes.

## 1.53.0 (2026-10-15)

- `high_risk_decisions` has eight decision domains under it:
  `employment_decisions`, `credit_decisions`, `insurance_decisions`,
  `housing_decisions`, `education_decisions`, `health_care_decisions`,
  `public_services_decisions` and `justice_decisions`. Declare each kind of
  decision your software makes or scores about people, and `high_risk_decisions`
  comes with it. A rule written for one kind of decision, such as a hiring law,
  then reaches only software that makes that kind.
- A declaration that names `high_risk_decisions` and no domain is answered
  exactly as before, with every domain's rules, and each jurisdiction where a
  domain would narrow them has an `info` line, `<slug>:decision-domain-undeclared`,
  counting those findings. `set_profile` asks for the domains.
- A domain is something your software does, not who you are, so a library or
  framework may declare one in its ACTIVITIES.md.

## 1.52.0 (2026-10-15)

- `provides_financial_services` has five license classes under it: `is_bank`,
  `is_lender`, `is_insurer`, `is_securities_firm` and `is_payment_provider`.
  Declare the class or classes your software's financial law comes from (a
  bank that lends declares two), and the role comes with it. A rule that binds
  one class of firm then reaches only that class, so a lender is not told a
  broker-dealer's rules.
- A declaration that names the role and no class is answered exactly as
  before, with every class's rules, and each jurisdiction where a class would
  narrow them has an `info` line, `<slug>:financial-class-undeclared`, counting
  those findings. The skill now asks for the class together with
  `regulated_sector`.
- The role's definition says what it always meant: a license held, or software
  supplied to a firm that holds one. Moving money alone is not it.

## 1.51.0 (2026-10-15)

- The bundle ships `schema/activities.schema.json`, the schema for
  `ACTIVITIES.md`: a file at a repository's root that declares which legal
  activities each package it ships performs or enables, which it rules out, and
  which counterparties it necessarily talks to. The activities are the 24 the
  lint already accepts, each with a page in the registry at
  https://lexlint.io/activities
- The bundle carries its own `ACTIVITIES.md`: a library that performs none of
  the activities and talks to mcp.lexlint.io for every run.
- Four activity definitions the lint shows are spelled in US English. Their
  meaning is unchanged. Nothing you declare or call changes.

## 1.50.2 (2026-10-12)

- The bundle's descriptions now name product-liability law among the topics the
  lint reads: who answers in damages for harm a product, software or an AI
  system causes, starting with the EU Product Liability Directive, which makes
  software a product from 9 December 2026. Until a jurisdiction's liability law
  is researched, a run there says so as a coverage warning. Nothing you declare
  or call changes.

## 1.50.1 (2026-10-11)

- The README links UnGovr's privacy policy, which applies to LexLint, under
  "More". Nothing about how a run behaves changes.

## 1.50.0 (2026-10-10)

- Recording a call and recording a text chat are now two activities, because
  the law treats them differently. `records_conversations` is replaced by
  `records_calls` (people talking to each other: a phone or video call, or a
  meeting held in person or online, including a notetaker that joins one; a
  voice assistant a caller talks to is `processes_voice`) and `records_text_chat`
  (keeping what users type in a chat, or having a vendor receive it as it is
  typed, with a person or an assistant answering: live chat, a chat widget,
  stored transcripts, session replay of typing). Declare the one that matches,
  or both. A statute that
  covers only the telephone, such as a telephone-only recording law, now
  reaches a call recorder and not a chat widget. The old name is retired, not
  deleted: runs and declarations that already name it still read, marked
  "(retired)", but a new run that names it is refused, with the two
  replacements and their definitions. Ask the developer which one applies,
  because a call and a typed chat differ in law, then update the manifest or
  saved declaration. Nothing else you declare or call changes.

## 1.49.3 (2026-10-10)

- The procedure now names the legal unit a jurisdiction everywhere, never a
  place: the lead block for each declared jurisdiction, the jurisdiction at
  the head of each block, and the ISO 3166 code read as the jurisdiction it
  names. Nothing you declare or call changes, and no field is added, renamed
  or removed.

## 1.49.2 (2026-10-10)

- The README shows the LexLint wordmark at the top instead of the LL icon. The
  icon is now used for the favicon alone. Nothing about how a run behaves
  changes.

## 1.49.1 (2026-10-05)

- When you have not said whether a public body runs or buys the software, or
  whether a bank or its supplier does, the run's note about it now counts every
  finding your answer would change, not only the ones it would move off you
  whole. A finding that is partly a public body's and partly yours stays at
  warn whatever you answer, so it was never counted, yet your answer still
  moves its other duties, and a supplier's answer adds a `customer_duty`
  finding for it. Those findings are now counted in
  `<slug>:public-sector-undeclared` and `<slug>:regulated-sector-undeclared`,
  and the lines say the findings "carry duties that bind only" those parties,
  which is true of a finding that is only partly theirs. Nothing you declare or
  call changes. A run that did not send the answer can now carry one of those
  notes in a jurisdiction that did not carry it before, when the only law there
  that touches it is partly a public body's or a bank's; no other finding is
  added or removed. A run that sent the answer reads as it did before.

## 1.49.0 (2026-10-05)

- A profile can now say whose duty the financial-services law is,
  `profile.regulated_sector`, keyed by sector: `{"financial": "supplier"}`.
  The values are `body` (a bank, insurer or payment institution runs the
  software), `supplier` (it is supplied to such entities) and `none`. A vendor
  whose customers are banks no longer reads its customers' duties as its own:
  the incident notices and reporting duties a bank owes arrive as
  `customer_duty` findings, a provider's contract terms stay yours, and a law
  that binds anyone is unchanged. It moves duties and never adds a match, so a
  vendor still declares `provides_financial_services`. A finding the answer
  cannot move, a law that binds only public bodies among them, carries no
  `owed` and is read as it is without the answer.
- `set_profile` asks the question in its `next` step when
  `provides_financial_services` is declared and the answer was not sent. A run
  without it says so: each jurisdiction where financial-law duties would move
  carries one info line counting them, `<slug>:regulated-sector-undeclared`.
  Nothing changes for a profile that does not declare the role.
- `run_lint`, `set_profile` and `upload_lint_run` take `regulated_sector`, and
  the run echoes it. Send it to `upload_lint_run` whenever the run had it.

## 1.48.1 (2026-10-04)

- The command in the procedure that prints the run after `run_lint` could not
  be pasted into a shell: a single apostrophe in its text ended the quoted
  program early, and the shell stopped with a syntax error. It now runs as
  written, and prints the same words as before. Nothing you declare or call
  changes.

## 1.48.0 (2026-10-03)

- A run that does not say whether a public body runs or buys the software now
  says so itself. Each jurisdiction where a law binding only public bodies
  matched carries one info line counting them, and `set_profile` asks the
  question in its `next` step when the answer was not sent. The same law no
  longer appears at two severities in two sessions without a reason given.
- A strategy, a charter or a regulator's guidance that matched your
  declaration is no longer reported as a duty. These records bind nobody on
  their own, so one info line per jurisdiction names them as context instead.
- `generates_content` now means output that reaches the app's users or the
  public. A tool whose AI output only its own team reads does not declare it.
- `run_lint` takes `brief: true`, for a client with no LexLint procedure that
  shows findings to a person. Each finding comes back as one line: its summary
  and first duty clipped to 160 characters, with the citation, link, when the
  law binds and whose duty it is. On a customer's 61-finding run that is about
  3,700 words where the full run is about 25,000. The plugin never sends it:
  the procedure needs the full findings to write `lexlint.yml`.
- Every `run_lint` result carries `replay`, a short reference to quote when
  you tell us about a run. It names the bundle, the law library build, the
  moment the run was judged and a digest of the declaration, so we can rebuild
  exactly that run. Nothing about the run is stored to make this work; the
  feedback step now puts it in the summary for you.

## 1.47.0 (2026-10-03)

- When a court has blocked a law, struck it or part of it down, or upheld it
  after a block, the finding now says which ruling did it. A new field,
  `court_action`, carries each ruling's name, its court, the day it was
  decided, what it did, the parts of the law it reached when it reached only
  some, where it stands now (an appeal filed, affirmed, reversed) and its
  case page on LexLint, plus a flag when a suit against the law is pending.
  It is absent when no court has acted, which is most laws.
- The run printed after `run_lint` adds a line under any law a court acted
  on, for example "blocked 2025-08-29 by Kohls v. Bonta (United States
  District Court for the Eastern District of California)", and "under
  challenge in court" when a suit is pending. The brief for counsel names the
  ruling the same way, linked to its page.
- `lexlint.yml` keeps `court_action` on each finding, and the bundle's schema
  declares it. Nothing you declare or call changes.

## 1.46.2 (2026-10-01)

- LexLint's body of law is now called the law library wherever you and your
  agent read it: the tool and schema descriptions, the text the server
  returns, the written procedure, the plugin's commands and README. It used
  to be called the corpus. Only the word changes. No key, field name, value
  or step is different, and `corpus_built_at` keeps its name, so a client
  that reads it is not affected. The run block the procedure prints labels
  its third line `law library`, where it read `corpus`.

## 1.46.1 (2026-09-30)

- The bundle's descriptions now name content-moderation law among the topics the lint
  reads: the liability of a service for what its users post,
  notice-and-takedown, and moderation transparency. A profile that declares
  `operates_social_platform` meets it. Nothing you declare or call changes.

## 1.46.0 (2026-09-30)

- A run now opens in the shape https://lexlint.io and
  https://developer.lexlint.io show a run in, printed straight after
  `run_lint` and before anything is merged:
  what was declared, where the app operates, by flag and name, and the date
  of the corpus; then a block for the lead finding in each declared place and
  for every finding for counsel, each with its place, the law, when it binds,
  the duty in full, the date it was read against its source and the address
  of its law page; then a count of what the block shows and of the rest.

## 1.45.1 (2026-09-29)

- The bundle now carries this changelog, CHANGELOG.md, with one entry per
  release, newest first. Read it in the bundle or at
  https://developer.lexlint.io/changelog on the developer site.
- The procedure's pointer to LexLint's law pages, which had been a bare domain
  name, is now the full address https://lexlint.io/law

## 1.45.0 (2026-09-29)

- A profile can now declare a public-sector role, `profile.public_sector`:
  `body` for software a public body runs, `supplier` for software sold to or
  run for public bodies, both, or `none`. `set_profile`, `run_lint` and
  `upload_lint_run` all accept it.
- With the role declared, each requirement is routed by who owes it. Every
  instrument finding carries `owed`. A duty that binds you stays in the
  finding's `requires`. A duty that binds only bodies you are not is reported
  as information, with its lines kept in `requires_elsewhere`.
- A duty that your public-sector customer owes and meets through your software
  arrives as its own `customer_duty` finding, placed right after the
  instrument finding it was split from.
- A caller that does not declare a role gets exactly the output it got before.

## 1.44.0 (2026-09-29)

- A state or other sub-national place now reads with its country code first, as
  "US-California", where it used to read "California (US)". The code, a hyphen
  and the name take about as much room as a flag emoji and its space, so a
  Place column lines up in both command-line clients. No field is added or
  renamed.
- The procedure's flag rule and its examples use the new form, and the plugin
  schema's description names both.

## 1.43.1 (2026-09-29)

- The copyright line in the bundle's LICENSE file now names the holder as
  UnGovr, with no company-type suffix. No tool, schema or procedure behaviour
  changes.

## 1.43.0 (2026-09-28)

- Every `run_lint` finding and every `set_profile` coverage row for a country,
  the European Union or the United Nations now also carries `jurisdiction_flag`,
  the flag emoji for that place. A state or a city carries none and never
  borrows its country's. The field is declared in the plugin's schema, and a
  merged manifest keeps it.
- The procedure prints the flag, then a space, before the place name in every
  table and list, and the keyless first-run preview table prints it too.

## 1.42.0 (2026-09-26)

- Every `run_lint` instrument finding, and every instrument `get_law` returns,
  now carries `in_force`, which says when the law binds. It is declared in the
  plugin's schema, a merged manifest keeps it, and `lifecycle` stays for
  existing clients.
- The procedure prints each finding's in-force words, `in_force.words`,
  wherever it says when a law binds.

## 1.41.1 (2026-09-26)

- The aggregation topic is labelled "Reuse law", not "News aggregation law".

## 1.41.0 (2026-09-24)

- The procedure names the communications topic and the three facts it adds.
- The `automated_outreach` activity no longer borrows `deploys_chatbot`'s
  categories. It now reaches the communications topic's rows, so a profile that
  declares it gets those rows in place of chatbot-disclosure rows, and its
  findings change.

## 1.40.3 (2026-09-23)

- `/lexlint-key` checks a key with `check_access`.
- LexLint no longer says your key is forwarded to a separate data service.
  The LexLint server checks it itself. Where `get_law` holds no data for a
  jurisdiction, its note now points at https://lexlint.io/law for coverage.

## 1.40.2 (2026-09-21)

- Step 1 no longer leaves a row marked ask when the evidence in hand settles
  it, and it asks an open ask row again before it sets the profile, so a
  one-word yes can no longer silently drop that row.
- Step 1 resolves the app's domains before it shows the declaration table.

## 1.40.1 (2026-09-21)

- Step 1 proposes the declaration from the code, and you confirm it, on every
  client.

## 1.40.0 (2026-09-21)

- A compact upload's `app_scope` reaches the portal as the scope object its
  schema requires.
