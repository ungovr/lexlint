<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# Step 7 in detail: report only what the lint can claim

**Write nothing into the repository but the manifest.** The run's JSON, the
upload preview, a report of your own: each goes under `/tmp` or your client's
scratch space and is gone when the session ends. The report is for the
session, the stored run is what the developer keeps, and a file of yours in
their tree is one the next `git add` commits. Step 6's doc lane and counsel
lane are the exceptions, and each writes only the artifact the developer
chose, where they chose it.

**Say what became of the upload**, in one line: the `run_url` or `share_url`
the reply carried; that the developer said no; or that it was asked and did
not land, refused, failed or state unknown, with the reason the upload
section's failure rule asks for. A report with none of these has skipped the
close, and a headless or CI session, where nothing is asked and nothing is
sent, says that instead.

That line is the close in place as well as in name: it ends the report, below
the findings, the sections that follow here and anything else you say about
the run. The link is what the developer opens once they have read to the end,
and one printed above a long table has scrolled away by then. Put the URL on a
line of its own, in full, with nothing after it, since a terminal takes a
trailing full stop or bracket into the link. A question still to ask comes
after the report, not inside it.

**After the findings, say which findings rest on exactly one declared
activity.** The `run_lint` response groups them for you in
`declaration_sensitivity`, keyed by activity with the finding ids, so the
developer can see what a value they doubt is carrying: strike that value and
those are the findings that go with it. An activity nothing rests on alone is
absent from it, and `{}` means no finding rests on a single value. If you
marked a value as unsure in step 3 and nobody was there to answer, this is
where the report names it, beside its group. On a split run (step 3) take the
union of the calls' groups, and drop any id the merged run no longer holds.
When the run went out without `public_sector`, name that as an open question
here too, beside the `<slug>:public-sector-undeclared` line that counts the
findings carrying a duty that binds only public bodies: some have `applies_to`
`government`, others are `both` with a public body's duty among their lines, and
the answer is what would route those duties. The same goes for a run with
`provides_financial_services` or a class declared and no `regulated_sector`:
name it beside the `<slug>:regulated-sector-undeclared` line, which counts the
findings carrying a duty that binds only a regulated financial entity or its
suppliers. And for a run with the role and no class: name the class as the
open question beside the `<slug>:financial-class-undeclared` line. And for a
run with a `roles` axis unanswered: name the role question beside the
`<slug>:ai-role-undeclared` or `<slug>:data-role-undeclared` line.

**Policy and guidance are context, never findings.** A `<slug>:soft-law` line
names the records that matched the declaration but are a strategy, a charter or
a regulator's guidance rather than law. They bind nobody on their own, so they
are not findings and not work items. Report the line as it reads, and never
promote a record it names into the findings table.

**Say what this run did not reach, every run, as its own section.** "Unlinted
is not clean" is the rule above (in `SKILL.md`); this is the part that makes it operational,
and it is the one thing in the report nobody can reconstruct afterwards. It is
a fixed section, it appears whether or not the run found anything, and it is
never empty, because its last line is always there:

**What this run did not reach**

- **Jurisdictions declared that LexLint holds nothing for**, by name, or that
  there were none. This is the coverage warning above (in `SKILL.md`), restated where a reader
  looking for gaps will find it.
- **Activities this app does that were not declared**, or that you found none.
  You read the code in step 1 to inform the questions; this is where that
  reading earns its keep, and an activity you noticed and did not declare is a
  gap you already know about.
- **Topics outside the six LexLint covers.** Name the ones a reader of this
  particular app would expect to see and LexLint does not hold. A studio that
  records identifiable people gets no right-of-publicity law out of a lint
  whose law library does not cover it, and a report that does not say so reads as
  though the question was asked and answered.
- **The standing line.** LexLint covers AI, scraping, privacy, cybersecurity,
  communications, content-moderation, product-liability, age-gating and reuse law, in the jurisdictions declared, for the
  activities declared. Everything else is unlinted, and unlinted is not clean.

Name the instrument where you can ("California's right of publicity, Cal. Civ.
Code section 3344") and say plainly that it did not come back under the
declared activities. Then stop: do not research it, do not summarize it, and
do not advise on it. Naming the gap is the whole job, and it is the most
useful thing a lint can say about law it does not hold.

**Then close the run by uploading it.** A terminal summary is the short version
of what just happened: it collapses findings to fit, and it is gone when the
session is. A run that produced findings therefore ends with the upload, as a
step and not as a pitch: build the payload ("Uploading a run", in the `lexlint-upload` skill named in `SKILL.md`), show the
developer exactly what leaves the repository, and run `upload_lint_run`. The
approval your client asks for before that call is the developer's yes, and
where your client will not ask (a pre-approved shell, a skip-permissions or
full-auto session) you ask once yourself, in one line, and wait; a declined
approval is a no: say plainly that nothing left the repository, ask
once for feedback instead, and take that answer as final whatever it is:

> Understood, nothing leaves the repository. If you have a minute, anything you
> would change about this run is worth more to the people who build LexLint
> than the run itself.

Then stop. One upload, one fallback, no third ask. Skip the sequence entirely
when the run found nothing, and in any headless or CI session, where there is
nobody to approve the payload and an unanswered prompt reads as a yes.
