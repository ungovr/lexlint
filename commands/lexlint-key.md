---
description: Set up the UnGovr Open Data key LexLint runs on, by pasting one in
---

Get an UnGovr Open Data key into place so the LexLint tools can run.

`$ARGUMENTS` is the key, if the developer already pasted one. Treat anything
that is not a key as an empty argument and start at step 1.

## 1. If no key was pasted, hand over the link

Say this, with the URL on its own line so it stays clickable:

> LexLint runs on your own UnGovr Open Data key. Sign in here, select
> "Create a key", copy it, and paste it back to me.
>
> https://ungovr.org/cli-login?client=lexlint

Then stop and wait. Do not open a browser, do not run a login command, and do
not offer to generate a key: minting happens on that page, under the account
holder's own sign-in, and nowhere else.

One thing to say alongside the link, because a developer cannot work it out
from the page alone:

- A key pasted into a session is recorded in that session's transcript. It is
  worth saying before they paste it, not after.

Creating a key no longer revokes the account's other keys, so there is nothing
to warn about there and nothing to talk them out of: if they cannot find the key
they had, the answer is to make another one.

## 2. Check the shape before spending a request on it

A key looks like `ung_live_` followed by a long random string. If what came
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

- Claude Code: `~/.claude/settings.json`, as `{"env": {"UNGOVR_API_KEY": "..."}}`.
  Merge into the existing JSON rather than overwriting it, keep every other
  key, and `chmod 600` the file afterwards.
- Any other client: name the file it reads and write it there, or fall back to
  the shell profile below.

Never write the key into a file that is committed. In a repository that means
never `.claude/settings.json` and never `.env`; check `git check-ignore` if you
are unsure whether a candidate file is tracked.

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
