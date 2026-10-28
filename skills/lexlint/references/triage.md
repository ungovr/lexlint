<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# Step 5 in detail: triage

**`applies_to` says whom the instrument binds**, as the law library records it, and
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
kind of body the caller is, which the profile collects only as `public_sector`
and, for a regulated financial entity, `regulated_sector` (read `owed` below
when either was declared) and no other tool here asks for. So
the field comes to you and the reading lives here, which is the reason it is
written down: a session that does not think to look reports duties binding
state agencies to a private studio as work to do.

**When a finding carries `owed`, read `owed` instead.** The lint has already
done the reading this section asks of you: `owed: yours` binds this app;
`owed: elsewhere` does not, arrives at `info`, and keeps its lines in
`requires_elsewhere`; and `owed: customer` means the duty is your customer's, a
public body or a financial institution, with the lines your software has to
support split into a `customer_duty` finding placed directly after it.
`applies_to` stays on both as the law library recorded it. `owed` is the answer
for this declaration. With `public_sector` declared every instrument finding
carries it. With only `regulated_sector` declared, only the findings that answer
moves do, and a government-only finding carries none: it keeps the `applies_to`
reading below, which that answer says nothing about. With `roles` declared, a
finding whose lines a role answer moved carries `owed` and `role`, the declared
roles each regime's lines were judged under; a line tagged for a role the
developer does not hold sits in `requires_elsewhere`. With `flows` declared, a
cross-border transfer finding carries `flows`, the declared routes that leave
its jurisdiction (`[]` when none does), and nothing else about it changes.

An instrument can be partly yours and partly your customer's. It then keeps its
own lines, carries `customer_duty_id`, and its `customer_duty` finding follows
it.

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

For a finding that carries `owed`, the first count comes from `owed` instead of
`applies_to`: it is the findings whose `owed` is `elsewhere`, and the threshold
count is unchanged.

6 findings are owed by someone other than this app, and 5 bind providers of
generative AI above thresholds this app is nowhere near. Both sets stay in
`lexlint.yml` with their citations, and neither is a work item.

An instrument finding whose `owed` is `customer` or `elsewhere` is not a work
item of its own. For `customer`, its `customer_duty` sibling is the work.
For a finding with no `owed`, the `applies_to` reading above stands.

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

Each work item takes one of exactly four lanes:

- `code`: a change to this repository. Ship a diff.
- `doc`: an artifact this repository should carry: a usage statement, a crawl
  policy, a procedure note. Draft it into the repo.
- `counsel`: not yours to act on alone. This lane is for findings that turn
  on legal judgment rather than work: whether the declared activity is
  permitted at all, whether a duty reaches this product, anything a
  restrictive or unsettled posture leaves as a question a diff cannot answer.
  Record it and route it. This is a real bucket, not a paywall, and nothing
  here is dressed as one.
- `product`: a capability your public-sector or financial-sector customers need
  to discharge a duty of their own. Every `customer_duty` finding goes here, and nothing else does.
  It usually ships as a diff, like `code`, and it is a separate lane because the
  duty is not yours: missing it is your customer's breach, and your exposure
  runs through the contract, not the statute.

**A finding whose `settledness.band` is `unsettled` goes to the counsel lane.
This is not a judgment you make: the law library made it, and the fields
beside the band say why.** The band is derived in the law library from whether a
regulator or a court has construed the duty, whether the instrument is under
challenge, and what questions the research left open. Route it even when the
finding also looks answerable with a diff, and say so in the plan: a
mitigation you can ship does not settle whether the duty reaches this
product. The one exception is a `customer_duty` finding, which always goes to
`product`: the duty is your customer's, so how settled it is is their counsel's
question, and you note the unsettled state in the work item.

- `developing` is a signal to weigh, not a rule. Someone with authority has
  read the duty and questions remain.
- `settled` routes nothing on its own. Your own reading still can, and should.
- **Absent is not `settled`.** Most instruments carry no band yet. There the
  lane is your judgment, exactly as it was before this field existed.

`settledness.open_questions` is what the brief for counsel opens with. Show
those questions verbatim wherever you show the finding, and never rewrite one
into a recommendation: the question is the research's, and the answer is the
lawyer's.

**Each `derived` finding is a `code` work item of its own.** Make one per
derived finding, titled with its `capability.words`, citing the derived
finding's `id` in the item's `findings`, and set the finding's `handled_by` to
it. The record it names is a change to this repository, a field or a
timestamp kept per incident or per person, which is why it is code. Never
write a `jurisdictions` key on an item whose only finding is derived: the
finding has no jurisdiction of its own, the portal reads the item's
jurisdictions from the laws in `derived_from`, and the upload warns on an
item whose `jurisdictions` differ from those of the findings it cites.
In the plan table, the Jurisdictions cell of an item whose only finding is
derived shows the distinct `jurisdiction` values of its `derived_from`, each
by its `jurisdiction_name` where the entry carries one and as the slug where
it does not, the same way the portal derives them; that is display only, and
the item still writes no `jurisdictions` key.

Write the plan to `lint.work_items` and point each finding at its item with
`handled_by`, except the `topic:` tool-coverage notices, which answer to no
work item. Then show the developer:

31 findings across 22 jurisdictions, and 5 things to do.

| Lane | What to do | Jurisdictions |
|---|---|---|
| CODE | Honor machine-readable TDM reservations before fetch | 🇪🇺 European Union, 🇩🇪 Germany, 🇫🇷 France +17 more |
| CODE | Label synthetic content on generated output | 🇪🇺 European Union, 🇰🇷 South Korea, US-California |
| DOC | AI-usage statement in the product README | 🇪🇺 European Union, 🇰🇷 South Korea |

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

# Step 6 in detail: work the lanes

**Code lane.** Find the file the work item implicates, ship the diff, and
record the location in `where` with a short `note` on every finding the item
answers.

**`product`** is worked like `code`: ship the change that lets the customer
discharge the duty, and set `handled_by` on the `customer_duty` finding it
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
   `jurisdiction_name`, `in_force.words`, as-of date, then the citation
   last, linked where `note_url` exists and plain where it does not. Under
   the table, one line per finding, so the table keeps its four columns:
   first the finding's
   `why`, in the lint's words, so counsel reads the reason before the law;
   then the finding's `summary` exactly as the lint gave it (the instrument's
   name and one sentence), the name, which is the finding's `name`, linked to
   the LexLint page where `note_url` exists,
   then **where in the code** the question arises: the `where` the developer
   recorded on the finding (a path and line, an issue, a document), as a
   link into the repository when the manifest declares one and plain
   otherwise. A lawyer who can see where the question comes from reads it
   differently from one handed a statute. A
   `posture` or `coverage` finding routed here is not an instrument and
   arrives with `citation: null` and no `in_force`: its row carries the kind
   in that column and its `basis` (the field and value the lint read,
   `crawl_policy = unsettled`) in the citation column. Never supply a
   citation for a row the lint gave none; a lawyer handed an invented
   reference has been handed something worse than a blank. Last on the line,
   where the finding carries `settledness`: its band, then the guidance link
   and the case citation the law library recorded. A lawyer reading "unsettled"
   wants to know what has already been said about the duty, and a band with
   no evidence under it is the same non-answer a bare citation is. Where the
   finding carries `court_action`, its court lines follow, as the run block
   prints them, each ruling's name linked to its `url`: a lawyer asked whether
   a blocked law binds starts from the order that blocked it.
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

### Link every citation that has a page

A finding whose instrument has a LexLint page carries `note_url`. Everywhere
you show that finding, show its citation as a link to that page: in the triage
list, in the work item, in the counsel list, in the brief for counsel, in
`lexlint.yml`. A citation alone
is a string to go and search for. The page behind it holds the summary, when
the law binds, what the instrument asks of an app, and the source
the research was read from.

| Lane | What to do | Where | Citation |
|---|---|---|---|
| COUNSEL | Confirm whether the labeling duty reaches this product | 🇪🇺 European Union | [AI Act Art. 50](https://lexlint.io/l/eu-2024-1689-50) |

**Never construct that URL.** `note_url` is a short code stored with the
record, not something derivable from the citation, and an instrument the
research engine has not reached carries none. No `note_url`, no link: show the
citation plain. A guessed link 404s underneath a statute the developer is about
to act on, which is worse than the citation on its own.

Carry `note_url` into the manifest beside `citation`, so the committed file
stays readable in six months.
