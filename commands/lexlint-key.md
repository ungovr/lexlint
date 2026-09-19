---
description: Set up the UnGovr Open Data key LexLint runs on, by pasting one in
---

Get an UnGovr Open Data key into place so the LexLint tools can run.

`$ARGUMENTS` is the key, if the developer already pasted one. Treat anything
that is not a key as an empty argument and start at step 1.

## 1. If no key was pasted, offer both routes and let the developer pick

There are two ways to a key, and neither is the fallback for the other:

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
nowhere else. If they choose the trial instead, call `claim_trial_key` only
after they choose it: never run it because no key was found, and never run it
twice. Say before running it that the key it returns will be recorded in this
session's transcript, the same as a pasted key.

**Twice includes a key you cannot see from here.** Do not run
`claim_trial_key` when a key is already saved on this machine, when one was
minted earlier in this conversation, or when your own memory or notes for this
machine record one. The one exception is a developer who, told that a first
key exists, asks for a new key in so many words. A needless mint is not free
to them: it spends one of the limited trial mints their address gets each
day, and it leaves the earlier key stranded, still valid and saved somewhere
nothing reads. If the preflight said `key: not set` on a machine where a key
was saved before, that is a key that did not arrive and not a missing one:
`/lexlint` looks for it by file name and says where it is.

One thing to say alongside the account-key link, because a developer cannot
work it out from the page alone:

- A key pasted into a session is recorded in that session's transcript. It is
  worth saying before they paste it, not after.

Creating a key no longer revokes the account's other keys, so there is nothing
to warn about there and nothing to talk them out of: if they cannot find the key
they had, the answer is to make another one. An account key has no expiry and
no lifetime total, which the trial does not: say that if they ask which to
pick.

## 2. Check the shape before spending a request on it

A key pasted back, or a key that arrived in `claim_trial_key`'s result, looks
the same from here: `ung_live_` followed by a long random string. If what came
back ends in `...`, it is a display stub from the settings list rather than a
key: the full value appears once, in the box on the page above. Name that
rather than sending them back to look again.

## 3. Verify it against the live API

One request, so a wrong key fails here rather than four steps later. One
line, and no backslash continuation: `\` continues a line in bash and zsh and
does not in PowerShell, where this same command otherwise breaks apart.

```
curl -sS -o /dev/null -w '%{http_code}' -H "X-API-Key: <the-key>" https://data.ungovr.org/v1/ai-laws/index.json
```

On Windows PowerShell, `curl` is usually an alias for `Invoke-WebRequest`,
which does not take these flags at all. Use its own form there:

```
(Invoke-WebRequest -Uri https://data.ungovr.org/v1/ai-laws/index.json -Headers @{'X-API-Key'='<the-key>'} -SkipHttpErrorCheck).StatusCode
```

- `200`: the key works. Go to step 4.
- `401` or `403`: the key was refused. Ask them to check they copied the whole
  value, and offer the link again.
- `402`: the key works and today's free allowance is already spent. Still worth
  persisting; say when it resets (00:00 UTC).
- Anything else, or no answer: the API is having a problem. That says nothing
  about the key, so persist it anyway and say the check was inconclusive.

## 4. Persist it where the next session will read it

The key belongs in `UNGOVR_API_KEY`. Write it into the `env` block of the
developer's user settings file, creating the file if it is not there:

- Claude Code: the **user** settings file, as a top-level
  `{"env": {"UNGOVR_API_KEY": "..."}}`. That file is
  `$CLAUDE_CONFIG_DIR/settings.json` when `CLAUDE_CONFIG_DIR` is set, and
  `~/.claude/settings.json` only when it is not, so ask before choosing:
  `echo "${CLAUDE_CONFIG_DIR:+set}"` prints `set` or an empty line. With the
  variable set, a key written to `~/.claude/settings.json` is saved in a file
  this client never reads. Merge into the existing JSON rather than
  overwriting it, keep every other key, and `chmod 600` the file afterwards.
- Any other client: name the user-level file it reads and write it there, or
  fall back to the shell profile below.

Never write the key into a file that is committed. In a repository that means
never `.claude/settings.json`, never `.claude/settings.local.json` and never
`.env`; check `git check-ignore` if you are unsure whether a candidate file is
tracked.

**The user file and no other scope, and the reason is not only git.**
`.claude/settings.local.json` is gitignored, so it passes that test, and it is
still the wrong place. Claude Code opens two connections to each server, and an
`env` value from the project or the local settings file reaches the server on
one of them and arrives empty on the other (measured on Claude Code 2.1.278).
A key saved there works for some calls and reads as `key: not set` for others.

**Then check that the file still parses, without printing it**:

```
python3 -m json.tool "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json" >/dev/null && echo ok
```

`ok` means it does. Anything else is the line and column of the first error,
and it matters more than it looks: an unparseable settings file is ignored
whole, so a stray comma loses the key and every other setting in the file with
it. Fix it before going on.

If the developer would rather have the key in their environment for other tools
too, the shell profile is the alternative, and it is theirs to run.

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

## 5. Say what happens next

The value is read at process start, so the session it was pasted into cannot
see it. Tell them plainly:

> Saved. Restart your session (a `/clear` will not do it), then run `/lexlint`.
> The first thing it does is a preflight that reports whether the key arrived.

Do not run the lint yourself in this session, and do not claim the key is
working. Nothing in this session can see it yet, and the preflight after the
restart is what actually answers that.

**If the preflight after the restart still reads `key: not set`, do not mint
again, and do not run this command again either.** The key you saved is still
where you put it. `/lexlint` now looks for it by file name, never by value, and
says where the saved key is and why it did not arrive: a session that was not
really restarted, a settings file that stopped parsing, the wrong scope, or a
surface that does not pass a plugin's header variable on. A second key fixes
none of those, and it strands the first.
