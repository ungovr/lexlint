---
description: Upload this session's completed lint run to the LexLint portal, after showing you exactly what leaves the repository
---

Store the run this session already produced on the LexLint portal, and show
you its URL once it lands.

**This is the closing step of a lint run that produced findings, and the
approval you give to the call is the yes.** A run closes by uploading itself,
and that is the only place it is raised unprompted: the payload is shown first,
exactly what leaves the repository, and a declined approval means nothing was
sent. Never volunteer it anywhere else, and never run it in a headless or CI
session, where with nobody there to approve the payload there is nothing to
upload.

## 1. Check the preconditions

The `run_lint` response from a completed `/lexlint` run in this session, which
is the run being uploaded. A `lexlint.yml` on disk carrying `app` and `profile`
supplies `record.app` and `record.profile` when it exists. On a first run with
no manifest yet, `record.app` is `{"name": ...}` with the repository's own name
(its package manifest's name, else its directory), and `record.profile` is the
declaration the run was made with, `activities` and `jurisdictions` exactly as
sent.

**A first run that could not upload itself leaves its record on disk, and
that record is the other thing this command uploads.** The first-run
procedure at https://lexlint.org/first-run writes the run it made to
`/tmp/lexlint-first-run/record.json`, and when the client refused the upload's
shell commands it leaves that file in place and hands the upload to the next
session. So with no `run_lint` response in this session, look there first,
and take it only when its `app.name` is this repository's own name (its
package manifest's name, else its directory, the rule the first run filled it
by): the path is shared by every repository on the machine, and a record
naming another one is somebody else's run, so say so and leave it. That file
is already the `record` object, `app`, `profile`, `lint.findings`
and `envelope` exactly as the run made them: read it with your file tool, wrap
it in the `ungovr.lexlint-upload/1` payload of section 2, show it as section 3
says, and send it as a tool call, `upload_lint_run(payload)`, never as the
`curl` in section 4. Leave `client_version` out of that payload: the
field means the bundle version that ran the lint, and this lint was run by
the first-run procedure, not by this bundle. A shell command is what that session could not run, and
the tool call needs none; the payload passes through your own output, which is
the cost and the point. Remove the directory only once the reply confirms the
run is stored, `run_url` present or `duplicate` true:
`rm -rf /tmp/lexlint-first-run`. A refusal, an error or a dropped connection
keeps the record where it is, for the retry the failure rule below describes.

Missing both, the `run_lint` response and a saved record, say so, run
`/lexlint` first, and stop rather than building a partial payload.

A manifest with **no `lint:` block is not a missing precondition**. The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by the loop's merge and triage steps, and triage waits on an approval
that may not have come yet. Upload the run and say the work items are empty.

## 2. Build the payload

Assemble the `ungovr.lexlint-upload/1` object, taking each part from whatever
owns it rather than all from one file:

- `record.app` and `record.profile`: the manifest's, verbatim, or the first-run
  name and declaration above when there is no manifest, with one exception:
  `app.scope` is what this run actually read. A `/lexlint <path>` scope is
  deliberately never written to the manifest, so copying `app` wholesale
  uploads a run over one directory carrying no scope, and the portal captions
  it `whole repository` on the run page, in the run list and on the counsel
  cover. Leave `scope` off only when the run read the whole repository.
- `record.lint.findings`: this session's `run_lint` response, which is the run
  being uploaded. Where the manifest's merged block covers this same run, carry
  `state`, `where`, `note` and `handled_by` across per finding id. The set of
  findings is always the run's.
- `record.lint.work_items` and `record.lint.vanished`: the manifest's, verbatim,
  when its `lint:` block is from this run, and otherwise empty. Triage held only
  in this conversation never uploads.
- `record.lint.declaration_sensitivity`: that same `run_lint` response's
  `declaration_sensitivity`, verbatim, when the response carried one (every
  response has since 2026-09-19). The run page's "By declared value" reads it
  and shows nothing without it. Never build it by hand from the findings: the
  server's rule counts findings that carry no `matched_by`.
- `record.envelope`: the run's own metadata, at minimum `corpus_built_at` from
  that same `run_lint` response.

**Never pair one run's findings with another run's envelope.** A committed
manifest normally holds the previous run's `lint:` block, and copying it
wholesale under today's `corpus_built_at` files a run that never happened. The
hash is computed over whatever you assembled, so nothing downstream catches it.

Never include the API key or any other credential, source files, prompts or
transcripts, or git usernames, emails, or remote URLs.

Leave `payload_hash` out. The server derives it from `record` and stores the
filled-in object, so nothing you run produces it. A payload that carries one
must match the server's exactly (the sha256 hex digest of the canonical JSON
encoding of `record`: keys sorted, `,` and `:` with no space after either,
non-ASCII left as raw UTF-8) and is refused otherwise, so sending it is a
check you can add, never a step you need. The skill's "Uploading a run"
section carries the on-disk recipe and its caveats for a client that sends it
anyway.

**On mentioning a tool you do not have:** the same restraint as the skill.
Say it once, in this session, and only if its absence actually cost something
here (the payload went through your own output because there was no `curl`).
Never because a tool is merely missing, never twice, never before the result,
and not at all in a headless or CI session or on a client with no shell,
where nobody can act on it and installing the tool would change nothing.

Without `curl`, call `upload_lint_run(payload)` as a tool and accept that the
payload passes through your own output. That works; the cost is the bytes.

## 3. Show the exact payload and wait

Print what is about to leave the repository, in full, before calling
anything:

```
LexLint will upload exactly this:

  findings:      <count>
  jurisdictions: <three slugs, plus a count if there are more>
  work items:    <count, or "0, the manifest holds no merged run yet">
  size:          <payload size>
  destination:   the account of key ung_live_<prefix>...
```

Then send it. If your client asks before it runs the command or the tool
call, that prompt is the developer's yes and there is no second question to
ask. If it will not ask (a pre-approved shell, a skip-permissions or full-auto
session, any client that runs commands without a prompt), ask the developer
yourself, in one line, and wait: "Send this run to the LexLint portal?" A no
means nothing leaves the repository. Either way, the payload above is what was
approved; do not change it after the yes.

## 4. Upload, from disk

The approval rule in section 3 applies to this command exactly as it would to
the tool call.

A real payload is around 100 KB of legal text, and passing it as a tool
argument means reproducing every byte of it in your own output, where the
server's hash check turns the smallest slip into a refused upload. Send the
file instead. Write the JSON-RPC request out with the payload nested inside
it, `{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name":
"upload_lint_run", "arguments": {"payload": <the object>}}}`, then post it:

```bash
curl -sS --fail-with-body https://mcp.lexlint.org/mcp \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $UNGOVR_API_KEY" \
  --data-binary @upload-request.json
```

**Check the reply for an error before reading anything else out of it.** Two
ways it can carry one and neither is a failed command: `curl -sS` alone exits 0
on a 500 and prints the edge's error page as though it were the answer, which
is what `--fail-with-body` stops, and a call the server read and refused comes
back HTTP 200 with an `error` member instead of a `result`, which no exit code
will ever report. A reply carrying `error` stored nothing and has no
`run_url`; `error.message` says what to fix.

No `initialize` first and no session to carry: the server is stateless and
answers a plain JSON POST with plain JSON. Write both files, the request and
the `record.json` it wraps, outside the repository, and delete
both once the reply is read: each holds the complete findings and the
developer's triage, and a file left in the tree gets committed by the next
`git add .`

**`curl` works and Python's `urllib` does not**: the same request from
`urllib.request` returns `403` with Cloudflare error `1010`, "browser signature
banned". That is our edge, not your machine. **Never forge a `User-Agent` to
get past a block** anywhere, ours included: it circumvents an access control
the operator chose. If no ordinary HTTP client is available, call
`upload_lint_run(payload)` as a tool and accept the relay.

On success, report the returned `run_url`
and say the run is stored, and report `share_url` too when it came back: a
trial key's account has no email to sign in with, so that link is its way back
into the run, and it works for 30 days. If `duplicate` came back true, say the
run was already stored under that URL rather than uploaded again.

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
