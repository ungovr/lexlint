---
description: Upload this session's completed lint run to the LexLint portal, after showing you exactly what leaves the repository
---

Store the run this session already produced on the LexLint portal, and show
you its URL once it lands.

**This is the closing step of a lint run that produced findings, and the
approval you give to the call is the yes.** A run closes by uploading itself,
and that is the only place it is raised unprompted: what will be sent is shown
first, exactly what leaves the repository, and a declined approval means
nothing was sent. Never volunteer it anywhere else, and never run it in a
headless or CI session, where with nobody there to approve it there is
nothing to upload.

**It is one tool call, and nothing else.** `upload_lint_run` takes the
declaration `run_lint` ran on and two values from its reply, and the server
rebuilds the findings itself from that declaration, judged at that same
instant, so what is stored is what you were shown. No shell, no file outside
the tree, no findings array passing through the agent's output: the call is a
few hundred bytes plus whatever triage you have written.

## 1. Check the preconditions

The `run_lint` response from a completed `/lexlint` run in this session, which
is the run being uploaded. A `lexlint.yml` on disk carrying `app` and
`profile` supplies the name and the declaration when it exists. On a first run
with no manifest yet, the name is the repository's own (its package manifest's
name, else its directory), and the declaration is the one the run was made
with, `activities` and `jurisdictions` exactly as sent.

Missing the `run_lint` response, say so, run `/lexlint`, and stop: it lints
again against today's corpus and closes by uploading. That includes a session
opened after a first run whose upload was refused. The first-run procedure at
https://lexlint.org/first-run sends the declaration and not the findings and
writes no record of its own, so there is no file waiting for a later session
to send, and nothing on this machine to look for.

A manifest with **no `lint:` block is not a missing precondition**. The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by the loop's merge and triage steps, and triage waits on an approval
that may not have come yet. Upload the run and say the work items are empty.

## 2. Build the arguments

Take each from whatever owns it rather than all from one file:

- `record.app`, which the server builds from `app_name`, `app_repo` and
  `app_scope`: the manifest's `app.name`, or the first-run name above; its
  `app.repo` when it has one; and `app_scope` set to what this run actually
  read, whenever that was not the whole repository: one directory as a
  string, or the manifest's `scope` object, `{include: [...], exclude:
  [...]}`, when it read several. The server stores the object either way, and
  refuses any other shape by name. A `/lexlint <path>` scope is deliberately
  never written to the manifest, so copying `app` wholesale uploads a run over
  one directory carrying no scope at all, and the portal captions it `whole
  repository`. Leave `app_scope` out only when the run read the whole
  repository.
- `activities` and `jurisdictions`: the two lists `run_lint` was called with,
  exactly as sent, and never the manifest's where the two differ. The server
  rebuilds from what you send, so a declaration the run did not use stores a
  run that never happened.
- `corpus_built_at` and `run_at`: both from that same `run_lint` response,
  verbatim. The server refuses the call when its corpus has moved since, or
  when `run_at` is more than an hour old, because either way the findings it
  would store are not the ones the developer approved. Both refusals name the
  same remedy: lint again, show the new result, and upload that.
- `work_items` and `vanished`: the manifest's, verbatim, when its `lint:`
  block is from this run. Otherwise leave both out. Triage held only in this
  conversation never uploads.
- `findings_state`: the developer's per-finding triage, keyed by finding id.
  Where the manifest's merged block covers this same run, take `state`,
  `where`, `note` and `handled_by` from every finding that carries any of
  them: they are the developer's, and the run has no opinion about them.
  Leave the argument out when no finding carries one. An id the run does not
  carry is refused, and that is right: the triage is another run's.
- `client_version`: the bundle version from the skill you are running. The
  bundle's own server entry sends it on every call as well, so the server has
  it either way.

**Never pair one run's triage with another run's reply.** A committed
manifest normally holds the previous run's `lint:` block. Compare its
`lint.run_at` and its finding ids against the response in hand, and on any
disagreement take nothing from the block but the four overlay fields, for the
ids both carry, and leave `work_items` out.

Nothing else goes in the call, and nothing else could: the tool takes no
credential, no source file, no prompt or transcript and no git identity.

## 3. Show the exact arguments and wait

Show them in the conversation, never as a file: write nothing into the
repository but the manifest, and a preview saved under `docs/` is a file the
next `git add` commits.

Print what is about to leave the repository, in full, before calling
anything:

```
LexLint will upload exactly this:

  findings:       <count>, rebuilt by the server from the declaration below
  jurisdictions:  <three slugs, plus a count if there are more>
  work items:     <count, or "0, the manifest holds no merged run yet">
  triage carried: <count of findings with a state, place, note or owner>
  destination:    the account of key ung_live_<prefix>...
```

Then send it. If your client asks before it runs the tool call, that prompt
is the developer's approval and there is no second question to ask. If it will not
ask (a pre-approved session, a skip-permissions or full-auto session, any
client that runs calls without a prompt), ask the developer yourself, in one
line, and wait: "Send this run to the LexLint portal?" A no means nothing
leaves the repository. Either way, what was shown is what was approved; do not
change it after the yes.

## 4. Send it, and read the reply as a reply

Call `upload_lint_run` with the arguments from section 2. Nothing is written
to disk on the way, and nothing has to be deleted afterwards.

**A refusal is a reply, not a failed call.** The server answers a refusal as
JSON-RPC, HTTP 200 with an `error` member in place of a `result`, and your
client hands it to you as the tool's result. A reply carrying `error` stored
nothing and has no `run_url`; `error.message` says what to fix, and for a
moved corpus or a stale `run_at` that is to lint again and upload the new
result. Report the refusal; never read a result out of it.

**A blocked route is never a reason to forge an identity.** Do not set a
`User-Agent` to look like a browser or like some other tool, here or anywhere
else: it circumvents an access control the operator chose.

Say what became of the upload, in one line: the link the reply carried; that
the developer said no; or that it was asked and did not land, refused, failed
or state unknown, with the reason. On success, report the returned
`run_url` and say the run is stored, and
report `share_url` too when it came back: a trial key's account has no email
to sign in with, so that link is its way back into the run, and it works for
30 days. If `duplicate` came back true, say the run was already stored under
that URL rather than uploaded again.

If the call fails outright, say plainly that **nothing was stored**, give the
reason, and offer to try again. If the connection drops after the request was
sent, the state is unknown rather than failed: say that too, and offer to
retry rather than assuming either outcome. The upload is idempotent per
payload hash, so a retry never creates a duplicate. For a trial key the retry
replaces the share link, so read the newest reply's `share_url`.

## Nothing is written back to the repo

No run URL, run code, or receipt goes into `lexlint.yml` or anywhere else in
the working tree. The portal resolves which project a run belongs to from
`app.name` alone, so there is nothing local to track.
