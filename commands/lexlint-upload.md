---
description: Upload this session's completed lint run to the LexLint portal, with your explicit approval of exactly what leaves the repository
---

Store the run this session already produced on the LexLint portal, and show
you its URL once it lands.

**Run this only on the developer's explicit yes.** A lint run that produced
findings closes by offering it once, and that is the only place it may be
raised unprompted: an offer is not a yes, and nothing is built or sent until
they give one. Never volunteer it anywhere else, and never run it in a
headless or CI session, where with nobody there to approve the payload there
is nothing to upload. A `/lexlint` run never uploads on its own.

## 1. Check the preconditions

Two things, and they are the two the payload is built out of: a completed
`/lexlint` run in this session, with the `run_lint` response it produced, and
a `lexlint.yml` on disk carrying `app` and `profile`. If either is missing,
say so, run `/lexlint` first, and stop here rather than building a partial
payload.

A manifest with **no `lint:` block is not a missing precondition**. The run
being uploaded is the `run_lint` response, which you have; the `lint:` block is
written by the loop's merge and triage steps, and triage waits on an approval
that may not have come yet. Upload the run and say the work items are empty.

## 2. Build the payload and its hash

Assemble the `ungovr.lexlint-upload/1` object, taking each part from whatever
owns it rather than all from one file:

- `record.app` and `record.profile`: the manifest's, verbatim.
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

## 3. Show the exact preview and wait

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

Then stop. Only on an explicit yes do you call the tool. If they say no, say
that nothing was sent, and stop.

## 4. Upload, from disk

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
answers a plain JSON POST with plain JSON. Delete the request file afterwards,
because it holds the whole record.

**`curl` works and Python's `urllib` does not**: the same request from
`urllib.request` returns `403` with Cloudflare error `1010`, "browser signature
banned". That is our edge, not your machine. **Never forge a `User-Agent` to
get past a block** anywhere, ours included: it circumvents an access control
the operator chose. If no ordinary HTTP client is available, call
`upload_lint_run(payload)` as a tool and accept the relay.

On success, report the returned `run_url`
and say the run is stored. If `duplicate` came back true, say the run was
already stored under that URL rather than uploaded again.

If the call fails outright, say plainly that **nothing was stored**, give the
reason, and offer to try again. If the connection drops after the request was
sent, the state is unknown rather than failed: say that too, and offer to
retry rather than assuming either outcome. The upload is idempotent per
payload hash, so a retry never creates a duplicate.

## Nothing is written back to the repo

No run URL, run code, or receipt goes into `lexlint.yml` or anywhere else in
the working tree. The portal resolves which project a run belongs to from
`app.name` alone, so there is nothing local to track.
