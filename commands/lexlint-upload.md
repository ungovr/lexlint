---
description: Upload this session's completed lint run to the LexLint portal, with your explicit approval of exactly what leaves the repository
---

Store the run this session already produced on the LexLint portal, and show
you its URL once it lands.

**Run this only when the developer asks for it.** Never offer it, never
suggest it as a next step after a lint, and never run it in a headless or CI
session: with nobody there to approve the payload, there is nothing to
upload. A plain `/lexlint` run never does this on its own.

## 1. Check the preconditions

There has to be a completed `/lexlint` run already in this session, with the
`run_lint` response it produced, and `lexlint.yml` has to exist on disk. If
either is missing, say so, run `/lexlint` first, and stop here rather than
building a partial payload.

## 2. Build the payload and its hash

Assemble the `ungovr.lexlint-upload/1` object from the manifest:
`record.app`, `record.profile`, and `record.lint` (`findings`, `work_items`,
`vanished`) copied verbatim from `lexlint.yml`, plus `record.envelope`
carrying the run's own metadata, at minimum `corpus_built_at` from the
`run_lint` response. Never include the API key or any other credential,
source files, prompts or transcripts, or git usernames, emails, or remote
URLs.

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
  work items:    <count>
  size:          <payload size>
  destination:   the account of key ung_live_<prefix>...
  payload hash:  <the sha256 hex digest just computed>
```

Then stop. Only on an explicit yes do you call the tool. If they say no, say
that nothing was sent, and stop.

## 4. Upload

Call `upload_lint_run(payload)`. On success, report the returned `run_url`
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
