<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# Step 1 in detail: read or create `lexlint.yml`

Show each candidate as a table of three columns: the value, your evidence (a
file and line, a store listing, a README sentence, or `none found`), and your
call, `include`, `leave out` or `ask`. Then one question: confirm, or strike
and add. An open question with no candidate is what the developer gets when
you skip the table, and it is the worse question: they cannot say yes to it,
and they have to know this vocabulary to answer it at all. Run 21 of the
funnel stopped on exactly that.

**Make the call the definition makes.** `ask` is for what the code cannot
show: a regulated role, a market, a person or property the app acts on. It is
not for a value whose definition already decides it on the evidence in your
hand. A game that teenagers may play is `include` for `serves_minors`, because
the definition below reaches a service merely likely to be accessed by them;
an app that fetches and shows another operator's records is `include` for
`aggregates_content`. Run 22 marked both `ask`, the developer answered "yes
go", and the lint that followed matched nothing.

**An `ask` row is not answered by a yes.** A one-word yes confirms the rows
you marked `include` and answers nothing else. When an `ask` row is still open
after the developer's answer, ask it again, once, in one line, and do not call
`set_profile` with one open: a declaration with a question left in it is a
lint that under-reports by design.

**Resolve the domains first.** When there is no manifest, do step 2 before you
show the table, so every operator the app talks to is a jurisdiction row with
its evidence rather than something you learn after the developer has already
said yes. Run 22 found California for two operators after the confirmation,
and it went into a comment instead of the declaration.

**What does this app do?** One or more of: `crawls_web`, `trains_models`,
`generates_content`, `deploys_chatbot`, `processes_personal_data`,
`processes_voice`, `processes_biometrics`, `automated_outreach`,
`high_risk_decisions`,
`publishes_adult_content`, `operates_social_platform`, `serves_minors`,
`operates_app_store`, `ships_mobile_app`, `ships_consumer_interface`,
`relies_on_digital_identity`, `collects_e_signatures`, `ships_encryption`,
`serves_sanctioned_destination`, `aggregates_content`, `distributes_software_product`,
`statutory_requests`,
`records_calls`, `records_text_chat`, `tracks_devices`, and the decision
domains and media kinds below.

**An activity LexLint has retired** (today `records_conversations`, replaced by
`records_calls` and `records_text_chat`) cannot start a new run. `set_profile`,
`run_lint` and `upload_lint_run` refuse it by name, ahead of any quota spend,
and the refusal names what replaced it and defines each replacement. When you
meet that refusal, or a `lexlint.yml` that still names a retired activity, ask
the developer which replacement applies, and never pick one yourself: a call and
a typed chat differ in law, so the choice is the clarification. Then declare the
one they name, rewrite `lexlint.yml`, and run again. Old runs that name the
retired activity still read.

**Who runs it?** Six more values are roles rather than activities, and a
sector-gated statute reaches the app through them and through nothing else:
`handles_health_records` (a HIPAA covered entity or business associate, or a
health-sector entity under a national regime), `provides_financial_services`
(holds a financial-services license, or supplies software to a firm that
does), `operates_essential_service` (an essential or important
entity under NIS2 or a transposition, or a designated critical-infrastructure
operator), `is_listed_company` (a public company filing with a securities
regulator), `provides_telecom_services` and `provides_cloud_services` (offers
customers, under a contract, a hosted service that stores or runs their own
data or workloads; running on somebody else's cloud is not it). These rows are
always `ask`, and they are the rows `ask` is for; never mark a role `include`
from the code. A health app is not a covered entity because it stores health
data, a fintech is not a bank because it moves money, and a web app is not a
cloud provider because it is hosted.

**Which license class?** `provides_financial_services` has six children, one
per license class whose rulebook does not cross into the others: `is_bank` (a
deposit-taker), `is_lender` (anyone who regularly extends or arranges credit as
a business, licensed or not), `is_insurer` (an insurer, reinsurer or insurance
producer, or a utilization-review organization acting for a health insurer),
`is_securities_firm` (a broker-dealer, investment firm or adviser, or fund
manager), `is_payment_provider` (a payment or e-money institution or a money
transmitter) and `is_crypto_asset_provider` (a crypto-asset or virtual-asset
service provider: an exchange, custodian, broker, transfer service or token
issuer). A class implies the role, so
declare the class and the role comes with it; a bank that lends declares
`is_bank` and `is_lender`, and a vendor whose customers are banks and insurers
declares both of those classes. Ask it as one row with the role: which class or
classes the software's financial law comes from, the developer's answer and
never the code's. A row that binds one class reaches only that class, so a
lender is not told a broker-dealer's rules. A profile that declares the role
and no class is answered with every class's rules, and each jurisdiction where
a class would narrow them has an `info` coverage line,
`<slug>:financial-class-undeclared`, counting those findings.

**Which decisions?** `high_risk_decisions` has eight children, one per domain
of decision about a person: `employment_decisions` (hiring, promotion, pay,
termination, task allocation, or monitoring and rating workers),
`credit_decisions` (credit, a loan or another financial service offered to
the person), `insurance_decisions`, `housing_decisions` (a tenancy, a rental
application, tenant screening), `education_decisions` (admission, grading,
proctoring), `health_care_decisions` (coverage, prior authorization,
utilization review, triage), `public_services_decisions` (public assistance
and benefits, emergency dispatch) and `justice_decisions` (law enforcement,
migration, asylum and border control, the courts, legal services). They are
activities, not roles, so the code can settle one: a model that scores job
applicants is `include` for `employment_decisions` with that file as its
evidence, while a "risk score" whose use the code does not state is `ask`. A
domain implies `high_risk_decisions`, so declare the domain and the parent
comes with it, and declare every domain the software decides in. A row written
for one kind of decision reaches only that kind, so a hiring tool is not told a
border-control rule. A profile that declares `high_risk_decisions` and no
domain is answered with every domain's rules, and each jurisdiction where a
domain would narrow them has an `info` coverage line,
`<slug>:decision-domain-undeclared`, counting those findings.

**What does it generate?** `generates_content` has four children, one per kind
of output: `generates_text` (articles, messages, summaries, code),
`generates_images` (pictures, artwork, edits of them), `generates_video` (clips,
animation, edits and swaps of real footage) and `generates_audio` (speech,
singing, music and other sound). They are activities, not roles, so the code can
settle one: a call to a text-to-speech or voice-cloning API, or a music model,
is `include` for `generates_audio` with that file as its evidence, while output
whose medium the code does not state is `ask`. A kind implies
`generates_content`, so declare the kind and the parent comes with it, and
declare every kind the software makes. A row written for one medium reaches only
that medium, so an image app is not told a voice-cloning rule. A profile that
declares `generates_content` and no kind is answered with every kind's rules,
and each jurisdiction where a kind would narrow them has an `info` coverage
line, `<slug>:medium-undeclared`, counting those findings.

**Does the public use a screen of it?** `ships_consumer_interface` is a
public-facing web or app frontend: pages, screens, a storefront, a booking or
sign-up flow. It is an activity, so the code can settle it: pages or app screens
anyone can reach are `include`, with that frontend as the evidence. An admin
console or a tool only the company's own staff use is not this, and neither is
an API with no screen of its own. It is the trigger for digital-accessibility
law, and it is separate from `ships_mobile_app`, which is about distributing an
app through a store: declare both for a mobile app the public uses.

**Does it check a digital identity, or take signatures?**
`relies_on_digital_identity` is code that accepts a digital identity wallet, a
verifiable credential or attestation, or an identity-verification service's
result, to check who a person is, their age or another attribute: an OpenID4VP
or ISO mdoc verifier, an SD-JWT VC library, an identity-verification SDK. A
password, or a social sign-in that only links an account, is not this.
`collects_e_signatures` is code that asks a person to sign an agreement or a
record electronically, in its own flow or through an e-signature service; a
checkbox accepting terms is not this. Both are activities, so the code settles
them, and they are the triggers for digital-identity law.

**Does it ship encryption?** `ships_encryption` is code that implements
cryptography, or bundles or vendors a library that does, beyond calling the
operating system's or platform's own TLS or cryptography APIs: a cryptography library
in the dependency tree or in vendored source, a custom cipher, a bundled TLS
stack or end-to-end encryption of its own. Calling HTTPS through the platform's
stock client is not this. It is an activity, so the code settles it, and it is a
trigger for export-control law.

**A sanctioned destination is set by the lint.** `serves_sanctioned_destination` is
never asked and never read from the code. The lint sets it itself when the
declaration lists `cu`, `ir` or `kp` as a jurisdiction, and says so in an `info`
coverage line, `<slug>:sanctioned-destination`, for each one. Declare it
yourself only when the app is offered to people in one of those countries and you
have not listed it as a jurisdiction. It is the trigger for sanctions law on
exports and services.

**Is it government software?** One more question, never answered from the
code: is this software run by a public body, sold to or run for public bodies,
both, or neither? Put it as the table's last row with the four answers spelled
out, and send the answer as `public_sector`: `["body"]`, `["supplier"]`,
`["body", "supplier"]` or `["none"]`. A police department's own records system
is `body`; a company selling that system to police departments, or running it
for them, is `supplier`; almost everything else is `none`. Some laws bind only
public bodies and some bind whoever supplies them, and this answer is the only
way the lint can tell a duty that is yours from one that is your customer's. Do
not call `set_profile` with it open, exactly as for the roles above.

**When to ask is one rule.** Ask it whenever the profile is declared or
re-declared. A manifest whose `profile` has no `public_sector` means the
question was never asked, so ask it once on the next interactive run, and write
the answer into the manifest's `profile`. The one case where it stays open is
an answer that cannot be had, a headless or CI run or a developer who has not
answered: leave `public_sector` out of every call entirely, and never send
`["none"]` on the developer's behalf. `["none"]` is the answer "neither
applies", and it moves every duty that binds only public bodies to
`owed: elsewhere`. A run sent without it says so itself: each jurisdiction
that matched a finding carrying a duty that binds only public bodies, a whole
finding or one line of it, has an `info` coverage line,
`<slug>:public-sector-undeclared`, counting those findings. Their duties stay
shown as yours, at the severity they would have as yours. A run that asked in
one session and not the next would otherwise show the same law at two
severities.

**Whose duty is the financial law?** A second answer, asked only when
`provides_financial_services` or one of its classes is a declared activity. A bank and a vendor whose
customers are banks both declare that role, and the lint cannot tell them
apart. Ask whether this software is run by a bank, insurer or other regulated
financial entity (`body`), supplied to such entities (`supplier`), or neither
(`none`), and send the answer as `regulated_sector`, keyed by sector:
`{"financial": "supplier"}`. A fraud-prevention vendor is `supplier`, a bank's
own system is `body`. It moves duties and never matches them, so a supplier
still declares the classes of its customers to be linted against financial
law. The same rule governs when to ask: whenever the profile is declared or
re-declared, once on the next interactive run when a manifest's `profile`
declares the role or a class and has no `regulated_sector`, never
`{"financial": "none"}` on the developer's behalf, and left out of every call
when it cannot be had. A run sent without it says so: each jurisdiction where
the answer would move a matched financial-law duty off the caller, a whole
finding or one line of it, has an `info` coverage line,
`<slug>:regulated-sector-undeclared`, counting those findings.

**Which role does the maker hold under each regime?** Asked of every
declaration, like `public_sector`, and never answered from the code. One firm
can be a provider under the EU AI Act and a processor under the GDPR, and some
duties bind only one role. Ask two things: under the EU AI Act, does the
developer's company build the AI system and put it out under its own name
(`provider`), use one under its own authority (`deployer`), or act as
`importer`, `distributor`, `product_manufacturer` or
`authorised_representative`, or none of these (`none`)? Under the GDPR, does it
decide why and how personal data is processed (`controller`), process it on a
client's documented instructions (`processor`), or neither (`none`)? A role can
be both (`["provider", "deployer"]`), and `none` is only ever alone. Send the
answers as `roles`, keyed by regime: `{"ai_system": ["provider"],
"personal_data": ["processor"]}`. A duty line tagged for a role the developer
does not hold moves to `requires_elsewhere`. The same rule governs when to ask:
whenever the profile is declared or re-declared, once on the next interactive
run when a manifest's `profile` has no `roles`, never `["none"]` on the
developer's behalf, and an axis left out of `roles` when its answer cannot be
had. A run sent without an axis says so: each jurisdiction where the answer
would move a matched duty off the caller has an `info` coverage line,
`<slug>:ai-role-undeclared` or `<slug>:data-role-undeclared`, counting those
findings. Only the European Union's own rows are tagged by role so far; a
jurisdiction where no matched line is tagged by role has an `info`
line, `<slug>:role-not-applied`, saying its duties are shown as yours.

**Where does personal data go?** Asked of every declaration, like `roles`, and
never answered from the code: a region in a deploy file can prompt the
question, never settle it. Ask whether the app stores or sends personal data
outside the jurisdiction it collects it in, and for each route where it starts
(`from`), where it goes (`to`), whether it is `personal` or `sensitive` data,
and the transfer mechanism it relies on (`basis`): `adequacy`,
`contract_clauses`, `binding_rules`, `certification`, `authority_approval`,
`consent`, `derogation`, or `unknown` when the developer does not know. Send
the answers as `flows`, one entry per route, `[{"from": "eu", "to": "us",
"data": "personal", "basis": "contract_clauses"}]`, or `[]` when none leaves.
`from` and `to` are jurisdiction slugs, and `eu` covers its member states. Each
cross-border transfer finding then names, in `flows`, the declared routes that
leave its jurisdiction. Nothing is dropped or downgraded on a flow: a
jurisdiction with such findings has an `info` line, `<slug>:transfer-flows`,
counting them and saying what was declared, which asks for `flows` when it was
not sent and for the basis of a route declared `unknown`. Ask when you would
ask for `roles`, and leave `flows` out when the answer cannot be had.

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

Read the code to build the candidate and its evidence, never to declare on
the developer's behalf: the table is a proposal until they confirm it.
Declaring `trains_models` because you saw a model import, when the app only
calls an API, produces findings for obligations that do not apply, and the
evidence column is there so the developer can catch exactly that.

**Four facts carry communications law, and each has a near neighbor.**
`automated_outreach` is software that sends people messages or places calls:
marketing email, SMS alerts, notifications, an agent that texts. It returns the
consent, sender-identification, opt-out and calling-hour rules (CAN-SPAM, the
TCPA, PECR, CASL), and nothing else: where a model writes or speaks the
messages (an AI voice agent, generated email copy), declare `generates_content`
or `deploys_chatbot` beside it, because the AI-disclosure rules attach there
and not to the sending. A request filed with a public body under a records or
freedom-of-information law is `statutory_requests` instead, and it exists so
that a records-request sender does not collect marketing law it does not owe.
`records_calls` is recording, transcribing or monitoring people talking to each
other: a phone or video call, or a meeting held in person or online, including
a notetaker that joins one; it returns the one-party and all-party consent
rules for recording speech, which `processes_voice` alone does not. A voice
assistant a caller talks to is `processes_voice`, not this: `records_calls` is
for people talking to each other.
`records_text_chat` is keeping what users type in a chat, or letting a vendor
receive it as it is typed, whether a person or an assistant answers (live chat,
a chat widget, stored transcripts, a session-replay script that captures
typing); it returns the interception rules for electronic communications,
which `deploys_chatbot` alone does not. An assistant that answers the chat is
`deploys_chatbot` beside it, and one that keeps no transcript and passes
nothing to a vendor is `deploys_chatbot` alone. They are separate because a
telephone-only statute reaches a call and not a chat, and because a chat widget
whose vendor reads the transcript has no voice in it. A form the app merely
saves is neither. `tracks_devices` is any cookie, pixel, SDK identifier or
fingerprint the service does not strictly need to deliver what the user asked
for, which is almost every site running analytics or advertising; it returns
the cookie-consent rule.

**Ask about voices and faces even when nothing here is AI.** `processes_voice`
and `processes_biometrics` reach privacy law rather than AI law, so they attach
to a support line that keeps call recordings or a kiosk that matches a face,
with no model anywhere in the product. Developers routinely leave both
undeclared for that reason. Declared, they return biometric statutes with their
own consent, retention and destruction duties, and in Illinois a private right
of action the person whose voiceprint you took can bring directly.

**Does it process personal data?** `processes_personal_data` is information
about a person who can be identified: accounts and sign-in, a contact or
sign-up form, analytics that follow visitors, an order or support history.
Most software does, so read the code for it: a users table, an auth provider,
an analytics SDK or a form that stores an email address is `include`, with that
file as its evidence. It is what privacy law turns on; a crawler, a model
trainer or a chatbot reaches a privacy law only where that law names the
conduct, so declare this beside them. When the software holds nothing about
anyone, record that answer: `activities_left_out: [processes_personal_data]` in
the profile. A declaration that says neither, and declares any activity the
code settles, is answered as if it processes personal data, and run_lint says
so in an `info` coverage line, `<slug>:personal-data-undeclared`, wherever a
finding rests on that alone, until the profile answers.

**Where will it operate?** This question has four plausible readings and
developers pick the wrong one. It is not where the users are, and it is not
where the servers are. **Server location is noise. What matters is the
jurisdiction of each operator whose content or systems the app touches, plus
every jurisdiction the app itself is offered in.** For a crawler, that means
the jurisdiction of each site it fetches, which step 2 resolves.

List every one of them. A jurisdiction left off is not passed, it is unlinted,
and unlinted is not clean. Propose here too: the markets a store listing or a
README names, and the operators step 2 will resolve, go in the table with
their evidence, and the four readings below are asked on top of it. A
jurisdiction you did not propose is one the developer has to think of alone.

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

A slug is the jurisdiction's UnGovr Atlas path: California is
https://ungovr.org/us/ca and its Atlas ID is `urn:ungovr:us/ca`.
The server also reads an ISO 3166 code as the jurisdiction it names, so a region
copied from a cloud or edge config works as written: `US-CA` is `us/ca`,
`GB-ENG` is England, a country code such as `FR` is that country, and a
territory the law library holds under its sovereign is reachable from its own
code (`PR` is `us/pr`). The
profile it writes always holds the slug. A city or county has no ISO code: name
it by path, as above.
A deeper or unresearched path resolves to the nearest jurisdiction with law,
and the jurisdictions whose law is researched are listed at https://lexlint.io/law
for the developer to check. The server resolves whatever you send and names
what it resolved to in the coverage preview, so there is nothing to look up
anywhere else, and a slug taken from a web search is the one that quietly
lints the wrong jurisdiction.

**Quote every slug.** YAML reads a bare `no` as boolean false and Norway
disappears from the declaration without a trace.

`set_profile` in step 3 checks the slugs and returns the coverage preview.
Show it to the developer before spending the lint, as a table:

You declared 6 jurisdictions. LexLint holds data for all 6.

| Jurisdiction | Instruments | Reviewed |
|---|---:|---|
| 🇺🇸 United States (federal) | 19 | 2026-08-12 |
| US-California | 14 | 2026-08-12 |
| 🇪🇺 European Union | 12 | 2026-08-12 |
| 🇩🇪 Germany | 8 | 2026-08-12 |
| 🇬🇧 United Kingdom | 6 | 2026-08-12 |
| 🇰🇷 South Korea | 3 | 2026-08-12 |

Depth varies. A low count is coverage LexLint has, not coverage the
jurisdiction lacks.

A slug with `held: false` returns a coverage warning, never a pass. Say so
here, not after the run, and give it a row of its own rather than dropping it
from the table: a jurisdiction missing from the preview reads as one nobody
declared.

**`derived` is a profile key you never ask about.** `derived: true` in the
`profile` of `lexlint.yml` adds `derived` findings to the run: the records an
app holds to meet the deadlines the matched laws set, each traced to the laws
it rests on. The severity model (`references/severity.md`) says what one is. It is off by
default while its wording is under legal review, so do not ask the developer
about it, do not put it in the table, and do not write it into `lexlint.yml`
yourself. A developer who wants these findings adds `derived: true` to the
manifest's `profile`, or asks you to; `derived: false`, or no key at all,
leaves them out.

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
