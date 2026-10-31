---
name: lexlint-upload
description: Use when the developer asks to upload a finished LexLint run to the portal, after showing exactly what leaves the repository.
license: MIT
compatibility: Needs the LexLint MCP server at https://mcp.lexlint.io and nothing else
metadata:
  version: "1.67.1"
  publisher: UnGovr
  homepage: https://lexlint.io
---

<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# LexLint upload

Store the run this session already produced on the LexLint portal, and show
the developer its URL once it lands. It is the close of step 7 of the
`lexlint` skill's loop (`../lexlint/SKILL.md`): a run that produced findings
ends here, after the developer has seen exactly what leaves the repository.

## Sending feedback and uploading runs

Two tools write rather than read. `submit_feedback` sends the developer's own
words about LexLint to the people who build it. `upload_lint_run` stores one
completed run on the LexLint portal, against the account the key belongs to.
Both are gated on the developer, this session: the upload is the closing step
of every run that produced findings, and the approval asked for before that
call is the yes; feedback is invited once, when that approval is declined.
Neither runs in a headless or CI session, where there is nobody to approve
anything.

**Step 7 is the one place either tool is raised unprompted**, and it is
written out in full there: the upload as the run's closing step, and one
invitation to send feedback if the upload is declined. Everywhere else, never
volunteer either one. The payload preview still stands between building the
upload and sending it: what leaves is shown before it goes.

A run reaches the portal only at the close of the run that produced it, shown
first, and from then on it is kept against their UnGovr account. A trial key's
account cannot be signed in to, so its upload also returns `share_url`, a link
that opens the run with no sign-in for 30 days; report it. Source, schema,
data, prompts and git history never leave the repository; what goes is the
lint's own output, the declaration the developer made (the two lists, and
`public_sector`, `regulated_sector`, `roles`, `flows` and `derived` when they gave them) and the repository's name.

The developer can delete a run or delete a project at any time from the
portal. Deleting a run removes it immediately and its stored payload is
purged within 30 days; deleting a project removes it, and everything under
it, right away. The developer can also export a project's own runs as
JSON. A run can be shared by an unguessable, expiring link that works
without signing in, and revoking it deletes the link immediately, not
merely marks it inactive. A trial key's account has no sign-in. To keep its
runs, the developer signs in at https://ungovr.org/cli-login?client=lexlint (an
account is free) and pastes the trial key at https://my.lexlint.io/claim and
the runs, their project and the key move to the account, where the portal's
delete button is theirs. To have a trial's run deleted without an account, the
developer writes to hello@ungovr.org quoting the share link and we delete the
run, or the link alone, within one working day.

### Uploading a run

`upload_lint_run` stores one complete lint run on the LexLint portal, against
the account the key belongs to, and hands back the portal URL and, for a trial
key, a share URL that needs no sign-in. It is the only way a run ever leaves
the repository: nothing else in this procedure sends findings, work items, or
the manifest anywhere. It runs at the close of the run that produced it, after
the developer has seen what will be sent and approved the call, at your
client's prompt or, where it asks nothing, at yours.

**It is one tool call, and nothing else.** The call sends the declaration
`run_lint` ran on and two values from its reply, and the server rebuilds the
findings itself from that same declaration, judged at that same instant, so
what is stored is what the developer was shown. No shell, no file outside the
tree, no key read out of anything, and no findings array passing through your
output: the whole call is a few hundred bytes plus whatever triage the
developer has written. That is the route, and the only one this procedure
gives.

**Preconditions.** The `run_lint` response from a completed LexLint run in
this session, which is the run being uploaded. A `lexlint.yml` on disk carrying
`app` and `profile` supplies the name and the declaration when it exists. On a
first run with no manifest yet, the name is the repository's own (its package
manifest's name, else its directory), and the declaration is the one the run
was made with, `activities`, `jurisdictions` and, when the run sent them,
`public_sector`, `regulated_sector`, `roles`, `flows` and `derived`, exactly as sent.

Missing the `run_lint` response, say so, run the `lexlint` skill again, and
stop: it lints again against today's law library and closes by uploading. That includes a session
opened after a first run whose upload was refused. The first-run procedure at
https://lexlint.io/first-run sends the declaration and not the findings and
writes no record of its own, so there is no file waiting for a later session
to send, and nothing on this machine to look for.

**A manifest with no `lint:` block is not a missing precondition.** The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by step 4 and step 5, and step 5 waits on an approval that may not have
come yet. Upload the run and say the work items are empty. Stopping here
instead strands a completed run behind an unrelated approval gate, which is the
defect this paragraph exists to close.

**Build the arguments.** Take each from whatever owns it, which is not all one
file:

- `record.app`, which the server builds from `app_name`, `app_repo` and
  `app_scope`: the manifest's `app.name`, or the first-run name above; its
  `app.repo` when it has one; and `app_scope` set to what this run actually
  read, whenever that was not the whole repository: one directory as a
  string, or the manifest's `scope` object, `{include: [...], exclude:
  [...]}`, when it read several. The server stores the object either way, and
  refuses any other shape by name. A one-run scope, named when the developer
  asked for the lint, is deliberately never written to the manifest, so
  copying `app` wholesale uploads a run over one directory carrying no scope
  at all, and the portal captions it `whole repository`. Leave `app_scope` out
  only when the run read the whole repository.
- `activities`, `jurisdictions` and `public_sector`: the lists `run_lint` was
  called with, exactly as sent, and never the manifest's where they differ. The
  server rebuilds from what you send, so a declaration the run did not use
  stores a run that never happened. **Send `public_sector` whenever the run
  being uploaded was declared with one.** A compact upload that leaves it out is
  rebuilt without it and stores an unrouted run: every line of every instrument
  as the app's own, no `owed`, no `customer_duty` findings, which is not what
  the developer was shown. Leave it out only when the run itself was made
  without it. **Send `regulated_sector` whenever the run being uploaded was
  declared with it**, for the same reason, exactly as `run_lint` took it, and
  **`roles`, `flows` and `derived` likewise**: a run rebuilt without `derived`
  carries no derived finding, so `findings_state` keyed on one is refused.
- `corpus_built_at` and `run_at`: both from that same `run_lint` response,
  verbatim. The server refuses the call when the law library has moved since, or
  when `run_at` is more than an hour old, because either way the findings it
  would store are not the ones the developer approved. Both refusals name the
  same remedy: lint again, show the developer the new result, and upload that.
- `work_items` and `vanished`: the manifest's, verbatim, when its `lint:`
  block is from this run. Otherwise leave both out. **Triage that lives only
  in this conversation never uploads**: a plan the developer has not approved
  and the repo does not hold is not part of the record, and sending it files
  their name to work items they never agreed to.
- `findings_state`: the developer's per-finding triage, keyed by finding id.
  Where the manifest's merged block covers this same run, take `state`,
  `where`, `note` and `handled_by` from every finding that carries any of
  them, the same four fields step 4 carries across: they are the developer's,
  and the run has no opinion about them. Leave the argument out when no
  finding carries one. An id the run does not carry is refused, and that is
  right: the triage is another run's.
- `client_version`: `1.67.1`, the bundle that ran the lint. The
  bundle's own server entry sends it on every call as well, so the server
  has it either way.

**Never pair one run's triage with another run's reply.** A committed manifest
normally holds the *previous* run's `lint:` block. Compare its `lint.run_at`
and its finding ids against the response in hand, and on any disagreement
take nothing from the block but the four overlay fields, for the ids both
carry, and leave `work_items` out. The server keeps the other half of this
rule: an id it did not rebuild is refused rather than stored.

Nothing else goes in the call, and nothing else could: the tool takes no
credential, no source file, no prompt or transcript and no git identity, and
what the server stores is the app name, the declaration, the findings it
rebuilt, the triage you sent and the law library's date.

**Show the consent preview, then wait for the approval.** Before calling the
tool, print exactly what is about to leave the repository, in the conversation
and never as a file: write nothing into the repository but the manifest, and a
preview saved under `docs/` is a file the next `git add` commits.

| Field | Value |
|---|---|
| Findings | 31, rebuilt by the server from the declaration below |
| Activities | the declared activities, exactly as sent |
| Jurisdictions | `us` `us/ca` `eu` +3 more |
| Public sector | the declared answer; leave this row out when the run has none |
| Regulated sector | the declared answer; leave this row out when the run has none |
| Work items | 5 |
| Triage carried | 12 findings with a state, place, note or owner |
| Destination | the account of key `ung_live_<prefix>...` |

Give the jurisdictions cell the same three-and-a-count treatment as
everywhere else in this procedure, and name the full list in a line under the
table when there are more than three. **When the work items are empty because
the manifest holds no merged block, say so in that cell** ("0, the manifest
holds no merged run yet") rather than printing a bare zero: the developer is
approving what leaves, and an unexplained zero next to 31 findings reads as a
bug in the preview. For the destination, read the key from
wherever it persists for this client, the place your client's Key entry in
`../lexlint/references/clients.md`
names, and show only its first sixteen characters (`ung_live_` plus
seven more) followed by `...`, the same truncation the settings page itself
uses. Never show more of the key than that, and if you cannot find where it
persists, say the destination is unknown rather than guessing at it.

Then ask for an explicit yes. **No yes, no call.** Not because the plugin is
installed, not because a previous session said yes, and never in a headless
or CI session, where there is nobody to give one. Where your client asks
before it runs the tool call, that prompt is the developer's yes and there is
no second question to ask; where it will not ask, ask once yourself, in one
line, and wait. Either way, what was shown is what was approved: do not change
it after the yes.

**A refusal is a reply, not a failed call.** The server answers a refusal as
JSON-RPC, HTTP 200 with an `error` member in place of a `result`, and your
client hands it to you as the tool's result. A reply carrying `error` stored
nothing and has no `run_url`; `error.message` says what to fix, and for a
moved law library or a stale `run_at` that is to lint again and upload the new
result. Report the refusal; never read a result out of it.

**A blocked route is never a reason to forge an identity.** Do not set a
`User-Agent` to look like a browser or like some other tool, here or anywhere
else: it circumvents an access control the operator chose, and the operator
being us changes nothing about that.

**Report what came back.** On success, print the returned `run_url` and say
the run is stored. Print `share_url` too when it came back: that is a trial
key's own way in, since its account has no email to sign in with, and the
link works for 30 days. Either link goes last in what you say, on a line of
its own with nothing after it, for the reason the report section gives. If `duplicate` came back true, say the run was
already stored under that URL rather than uploaded again: the portal keys on
the account and the payload hash together, so re-sending the same run is
always safe and never files a second copy.

If the call fails outright, say plainly that nothing was stored, give the
reason, and offer to try again. If the connection drops after the request was
sent, the state is unknown rather than failed: say that plainly too, and offer
to retry rather than assuming either outcome, because the upload is
idempotent per payload hash and a retry never creates a duplicate. For a trial
key the retry replaces the share link, so read the newest reply's `share_url`.

Say what became of the upload, in one line, and last: the link the reply
carried; that the developer said no; or that it was asked and did not land,
refused, failed or state unknown, with the reason.

**Record nothing about the upload in the repo.** No run URL, run code, or
receipt goes into `lexlint.yml` or anywhere else in the working tree. The
portal resolves which project a run belongs to from `app.name` alone, on its
own side, so there is no local identifier to track and nothing here for
`.lexlint/` or any other cache to hold.
