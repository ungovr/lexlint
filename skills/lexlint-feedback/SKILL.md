---
name: lexlint-feedback
description: Use when the developer wants to send feedback about LexLint, a finding, or the law it cites, from this session.
license: MIT
compatibility: Needs the LexLint MCP server at https://mcp.lexlint.io and nothing else
metadata:
  version: "1.67.0"
  publisher: UnGovr
  homepage: https://lexlint.io
---

<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# LexLint feedback

Collect the developer's feedback on LexLint and submit it.

**Run this only on the developer's explicit yes.** A lint run whose upload
approval was declined closes by inviting feedback once, and that is the only
place it may be raised unprompted. Never volunteer it anywhere else, and never
run it in a headless or CI session, where with nobody there to approve the
payload there is nothing to send.

### Sending feedback

`submit_feedback` sends the developer's feedback on LexLint to the people who
build it, recorded against their UnGovr account so we can write back.

**Never read the session transcript to build the summary**: a key pasted into
a session is recorded there, and a summary built from one would carry the
developer's own key to us.

The shape:

1. Draft a short usage summary from what you actually did this session. If no
   lint ran, omit it rather than inventing one. When one did, put each run's
   `replay` value in it, verbatim: it lets us rebuild exactly the run the
   feedback is about, and it carries nothing the developer did not send.
   Cover only what you can answer, and drop any line you cannot: whether
   `lexlint.yml` already existed or was written this session, the activities
   and jurisdictions declared, how many findings came back by severity, how
   many work items by lane, which lanes were actually worked, and anything
   that got stuck, and where. Work from what you did, never from what was
   said, and never paste a log.
2. Ask what they want to say: one open question, what was useful, what was
   not, what is missing. Say that a person reads it.
3. Print the exact payload, in full, and wait for an explicit yes. Say that
   this is all of it:

   ```
   LexLint will send exactly this:

     usage:    <the drafted summary, or "none: no lint ran this session">
     comments: <their words>
     client:   <the client you are running in, such as claude-code or codex>
     version:  1.67.0
   ```

   Editing is expected, not exceptional, and the payload shown last is the one
   they approve. If they say no, say that nothing was sent, and stop.
4. Call `submit_feedback(comments, usage_summary?)` and report the receipt.
   Send exactly what you displayed, `client` and `plugin_version` as the
   payload shows them: not a superset, not a re-rendered version.

If the call fails, say plainly that nothing was sent. Never report a submission
you did not get a receipt for. One submission per session: if they think of
something afterwards, it belongs in the same submission rather than a second
one.

If the server refuses the payload because something in it is shaped like an
API key or a token, do not strip it silently and retry. Say what was caught,
and let the developer decide what to do about it.

Two other things are recorded automatically, and they are the whole of the
rest of the list.

Which plugin version is running. It rides the `check_access` preflight LexLint
already makes, and is stored on its own, in a place that holds nothing but
version numbers. It is how we tell whether anyone is still on a bundle old
enough that retiring an old tool name would break them. A version string and
nothing else: not the key, not an IP address, and no record of what was linted.

A record of each request to the LexLint server: what the request was (which
tool, or a step of connecting), which coding tool sent it (never the model),
what kind of credential it carried and whether it succeeded, plus the country
and region Cloudflare reports for the connection. That location is the
connection's, which for a VPN or a cloud-hosted agent is a data center, and it
plays no part in which laws a lint applies; those come only from the
jurisdictions the developer declares. The record holds no IP address, key or
account, and nothing from what was linted. Each record is kept three months,
then only as daily totals.

Nothing else about a session is collected automatically by LexLint. The key is
an UnGovr Open Data key, and that API keeps a request log of its own, set out
at https://www.ungovr.org/open-data/api-keys and holding which collection was
asked for and a one-way hash of the key, never which jurisdiction was looked
up.
