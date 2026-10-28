---
name: lexlint-key
description: Use when the developer needs an UnGovr Open Data key put in place for LexLint, has pasted one, or the preflight found no key and no saved key.
license: MIT
compatibility: Needs network access to https://mcp.lexlint.io to check the key, and a browser for the sign-in at https://ungovr.org when the developer takes an account key
metadata:
  version: "1.61.0"
  publisher: UnGovr
  homepage: https://lexlint.io
---

<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

# LexLint key

Get an UnGovr Open Data key into place so the LexLint tools can run. A key the
developer pasted with the request is the key: go to step 3. Anything else,
including no key at all, starts at step 1.

This is the key flow the `lexlint` skill's Setup hands off to
(`../lexlint/SKILL.md`), and that skill's rules about keys hold here too.

**The lint is advisory and never blocks the work.** If the developer declines
the key, say in one line that it was offered and declined, then go back to the
request that brought you here and do it.

## 1. Look before you offer a route

**"No key" is two different states, and getting a key fixes only one of
them.** A key that is saved on this machine and did not reach the server reads
`key_present: false` exactly as a missing one does. So unless the saved-key
look already ran in this session, run it first: one command that prints file
names and never a value, set out in `../lexlint/references/no-key.md`, with
your client's own command in its entry in `../lexlint/references/clients.md`.
If it finds a saved key, say where and why it did not arrive, and do not mint
another. Only when it finds nothing, go on to step 2.

## 2. Offer both routes and let the developer pick

**There are two routes to a key and the developer picks, so ask BEFORE you
start either one.** Neither is a fallback for the other. One needs an account,
which is free; the other needs none: `claim_trial_key`, called from this
session, mints a 30-day key good for 50 requests over its whole life and
returns it in the result. Say that an account key is the one without an expiry
or a lifetime total, and say that a trial key will be recorded in this
session's transcript. Then run only the route they chose. Never run
`claim_trial_key` because no key was found, and never run it twice.

**Twice includes a key you cannot see from here.** Do not run
`claim_trial_key` when the saved-key look found a key on disk, when a key was
minted earlier in this conversation, or when your own memory or notes for this
machine record one. The one exception is a developer who, told that a first
key exists, asks for a new key in so many words. A needless mint is not free
to them: it spends one of the limited trial mints their address gets each
day, and it leaves the earlier key stranded, still valid and saved somewhere
nothing reads.

When the preflight ran, `setup.steps` in its response names the routes this
deployment actually offers. Offer only those: a deployment that cannot mint a
trial names only the account route, and offering the other one there sends
the developer to a dead end.

Say it in these words, or close to them:

> LexLint runs on your own UnGovr Open Data key. There are two ways to get
> one: sign in and create an account key, which is free and never expires, or
> take a 30-day trial with no account at all.
>
> For an account key, sign in here, select "Create a key", copy it, and paste
> it back to me:
>
> https://ungovr.org/cli-login?client=lexlint
>
> For a trial key, just say so and I will mint one for you here, no sign-in
> needed.

Then stop and wait for the developer's choice. Do not open a browser, do not
run a login command, and do not offer to generate an account key yourself:
minting one happens on that page, under the account holder's own sign-in, and
nowhere else. If they choose the trial, call `claim_trial_key` then, and only
then.

One thing to say alongside the account-key link, because a developer cannot
work it out from the page alone:

- A key pasted into a session is recorded in that session's transcript. It is
  worth saying before they paste it, not after.

Creating a key no longer revokes the account's other keys, so there is nothing
to warn about there and nothing to talk them out of: if they cannot find the key
they had, the answer is to make another one.

## 3. Check the shape before spending a request on it

A key pasted back, or a key that arrived in `claim_trial_key`'s result, looks
the same from here: `ung_live_` followed by a long random string. If what came
back ends in `...`, it is a display stub from the settings list rather than a
key: the full value appears once, in the box on the page above. Name that
rather than sending them back to look again.

## 4. Verify it against the live API

One request, so a wrong key fails here rather than four steps later. It asks
LexLint's own `check_access`, the preflight every lint starts with, and spends
one request of the key's daily allowance. One line, and no backslash
continuation: `\` continues a line in bash and zsh and does not in PowerShell,
where this same command otherwise breaks apart.

```
curl -sS --fail-with-body --max-time 120 -X POST https://mcp.lexlint.io/rpc -H "X-API-Key: <the-key>" -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_access","arguments":{}}}'
```

On Windows PowerShell, `curl` is usually an alias for `Invoke-WebRequest`,
which does not take these flags at all. Use its own form there:

```
(Invoke-RestMethod -Method Post -TimeoutSec 120 -Uri https://mcp.lexlint.io/rpc -Headers @{'X-API-Key'='<the-key>'} -ContentType 'application/json' -Body '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_access","arguments":{}}}').result.structuredContent | Format-List key_valid, notice
```

Read `key_valid` and `notice` from the answer:

- `key_valid: true`: the key works. Go to step 5. If `notice` says the free
  allowance is spent, or that paid access is needed, pass that sentence on;
  the key is still worth persisting.
- `key_valid: false`: the key was refused. Ask them to check they copied the
  whole value, and offer the link again.
- `key_valid: null`, an error, or no answer: LexLint could not check. That says
  nothing about the key, so persist it anyway and say the check was
  inconclusive.

## 5. Persist it where the next session will read it

The key belongs in `UNGOVR_API_KEY`, saved where your client reads it when it
starts. Where that is, and the command that writes it when your client has
one, differ by client: your client's **Key** entry in
`../lexlint/references/clients.md` gives both, and no command from another
client's entry is worth offering.

Never write the key into a file that is committed. In a repository that means
never a project's own settings file (on Claude Code, `.claude/settings.json`
and `.claude/settings.local.json`) and never `.env`; check `git check-ignore`
if you are unsure whether a candidate file is tracked.

**When the file is JSON, check that it still parses, without printing it**:

```
python3 -m json.tool <the file> >/dev/null && echo ok
```

`ok` means it does. Anything else is the line and column of the first error,
and it matters more than it looks: an unparseable settings file is ignored
whole, so a stray comma loses the key and every other setting in the file with
it. Fix it before going on.

If the developer would rather have the key in their environment for other tools
too, the shell profile is the alternative, and it is theirs to run. It reaches
only a client started from a terminal opened after the line is in, and some
never read one at all: the Claude desktop app never reads a shell profile, not
even after a full quit and reopen (measured 2026-10-15), so a developer who
uses it keeps the key in the file above.

**Read the profile off their actual shell, never off a guess.** A line appended
to `~/.zshrc` for someone running bash is sourced by nothing, so the restart
leaves the variable unset and lands them back where they started, holding a key
they were told was saved. `echo $SHELL`, or `$env:SHELL` on PowerShell, is the
question worth one command:

| Shell | File | Line |
|---|---|---|
| zsh | `~/.zshrc` | `export UNGOVR_API_KEY=<the-key>` |
| bash | `~/.bashrc`, or `~/.bash_profile` on macOS | `export UNGOVR_API_KEY=<the-key>` |
| fish | `~/.config/fish/config.fish` | `set -gx UNGOVR_API_KEY <the-key>` |
| PowerShell | the path in `$PROFILE` | `$env:UNGOVR_API_KEY = '<the-key>'` |

For anything not on that list, ask which file their shell reads at startup
rather than picking the closest-looking one.

## 6. Say what happens next

The value is read at process start, so the session it was pasted into cannot
see it. Tell them plainly:

> Saved. Restart your session as a new process (a reset inside the running
> one will not do it), then ask for the lint again. The first thing it does
> is a preflight that reports whether the key arrived.

How a restart is done differs by client, and your client's **Restart** entry in
`../lexlint/references/clients.md` gives it.

Do not run the lint yourself in this session, and do not claim the key is
working. Nothing in this session can see it yet, and the preflight after the
restart is what actually answers that.

**If the preflight after the restart still reads `key: not set`, do not mint
again, and do not run this skill again either.** The key you saved is still
where you put it. The `lexlint` skill looks for it by file name, never by
value, and says where the saved key is and why it did not arrive: a session
that was not really restarted, a settings file that stopped parsing, the wrong
scope, or a surface that does not pass a plugin's header variable on. A second
key fixes none of those, and it strands the first.
