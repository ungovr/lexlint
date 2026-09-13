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
sent. Missing the `run_lint` response, say so, run `/lexlint` first, and stop
here rather than building a partial payload.

A manifest with **no `lint:` block is not a missing precondition**. The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by the loop's merge and triage steps, and triage waits on an approval
that may not have come yet. Upload the run and say the work items are empty.

## 2. Build the payload and its hash

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
- `record.envelope`: the run's own metadata, at minimum `corpus_built_at` from
  that same `run_lint` response.

**Never pair one run's findings with another run's envelope.** A committed
manifest normally holds the previous run's `lint:` block, and copying it
wholesale under today's `corpus_built_at` files a run that never happened. The
hash is computed over whatever you assembled, so nothing downstream catches it.

Never include the API key or any other credential, source files, prompts or
transcripts, or git usernames, emails, or remote URLs.

Compute `payload_hash` as the sha256 hex digest of the canonical JSON
encoding of `record`: keys sorted, `,` and `:` separators with no space after
either, and non-ASCII characters left as raw UTF-8 rather than
backslash-escaped. The server recomputes this same digest from the `record`
you send and refuses the upload on any mismatch, so "close" does not pass.

**With `jq` and a hash tool, do it on disk and the bytes never reach you.**
Write `record` to a file, then:

```bash
jq -cS . record.json | tr -d '\n' | sha256sum | cut -d' ' -f1
```

`-S` sorts keys at every level, `-c` gives the two tight separators, and jq
emits raw UTF-8, so this is byte-identical to the definition above. `tr` drops
the newline jq adds, which is not part of the digest; on macOS use `shasum -a
256`.

Numbers are the one place the two can part, so check rather than assume.
Nothing in the upload schema declares a numeric field and a `run_lint` response
carries none, but `app` and `profile` are copied out of the developer's
`lexlint.yml` verbatim and are open to extra fields. So run two counts first,
both of which should answer `0`:

```bash
jq '[.. | numbers] | length' record.json
jq -r '.. | strings' record.json | grep -c $'\x7f'
```

The second is for DEL, U+007F, the only non-number character the two encoders
disagree about: the definition writes it raw and jq writes `\u007f`, so the
number count alone would pass a record that hashes two ways. Either count
non-zero, hash with the definition above instead.

The rule behind it: jq passes the literal through as written while the
definition re-renders whatever it parsed, so they differ for any literal that
is not already what the definition would print. `1e3` against `1E+3`,
`0.1234567890123456789` against `0.12345678901234568`, `1.79e309` against
`Infinity` which is not JSON, `-0` against `0`. Illustrations, not a checklist.

**On mentioning a tool you do not have:** the same restraint as the skill.
Say it once, in this session, and only if its absence actually cost something
here (the payload went through your own output because there was no `curl`).
Never because a tool is merely missing, never twice, never before the result,
and not at all in a headless or CI session or on a client with no shell,
where nobody can act on it and installing the tool would change nothing.

Without those tools, use the definition above in whatever language you have.
That works, and the only cost is that the payload passes through your own
output.

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
  payload hash:  <the sha256 hex digest just computed>
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
curl -sS https://mcp.lexlint.org/mcp \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $UNGOVR_API_KEY" \
  --data-binary @upload-request.json
```

No `initialize` first and no session to carry: the server is stateless and
answers a plain JSON POST with plain JSON. Write both files, the request and
the `record.json` the hash counts read, outside the repository, and delete
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
