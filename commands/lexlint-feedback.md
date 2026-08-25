---
description: Send feedback on LexLint to the people who build it, from this session
---

Collect the developer's feedback on LexLint and submit it.

**Run this only when the developer asks for it.** Never offer it, never suggest
it as a next step after a lint, and never run it in a headless or CI session:
with nobody there to approve the payload, there is nothing to send.

## 1. Draft the usage summary yourself

Write a short summary of how LexLint was actually used in this session, from
what you did. Cover only what you can answer, and drop any line you cannot:

- whether `lexlint.yml` already existed or was written during this session
- the activities and jurisdictions declared
- how many findings came back, by severity
- how many work items, by lane (code, doc, counsel)
- which lanes were actually worked
- anything that got stuck, and where

**Never read the session transcript to build this, and never paste a log.** A
key pasted into a session is recorded in that transcript, and a summary built
from one would carry the developer's own key to us. Work from what you did, not
from what was said.

If no lint ran this session, say so and skip the summary. Do not invent one.

## 2. Ask what they want to say

One open question: what was useful, what was not, what is missing. Say that a
person reads it.

## 3. Show the exact payload and wait

Print what you are about to send, in full, and say that this is all of it:

```
LexLint will send exactly this:

  usage:    <the drafted summary, or "none: no lint ran this session">
  comments: <their words>
  client:   claude-code
  version:  <from .claude-plugin/plugin.json>
```

Then stop. Editing is expected, not exceptional. Only on an explicit yes do you
call the tool. If they say no, say that nothing was sent, and stop.

## 4. Submit

Call `submit_feedback` with `comments`, and with `usage_summary` if there is
one. Send exactly what you displayed: not a superset, not a re-rendered
version.

Then report the receipt:

> Sent. Your receipt is `fb_xxxxxxxxxx`, if you ever need to refer to it.

If the call fails, say plainly that **nothing was sent**, give the reason, and
offer to try again. Never report a submission you did not get a receipt for.

If the endpoint refuses the payload because something in it is shaped like an
API key or a token, do not strip it silently and retry. Say what was caught,
and let the developer decide what to do about it.

## Once per session

One submission per session. If they think of something afterwards, it belongs
in the same submission rather than a second one.
