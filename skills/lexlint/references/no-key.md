<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### When the preflight says there is no key

**If the same response reports `credential: "none"`, this section is not
yours.** That install signs in instead of using a key: go to "When this
install signs in instead of using a key", below (`references/signed-in.md`).

If `key_present` is false, stop. **And do not offer a route to a key yet.**
The server cannot tell a key that does not exist from a key that is saved on
this machine and went out as an empty header, so it answers
`key_present: false` to both. Read as "no key", the second one ends with a
fresh key minted over a working one, by a developer who followed every
instruction they were given.

**So look first, whenever you have a shell, with one command that prints file
names and nothing else.**

Which files are worth opening differs by client, so the command is in your
client's entry under "Client setup" below (`references/clients.md`), as "Saved-key check", beside what
each result means there. It has this shape:

```
grep -l UNGOVR_API_KEY <the files your client's entry names> 2>/dev/null
```

`grep -l` prints the NAME of every file the variable's name appears in.
**Never `cat` one of these files, never print the matching line, and never
read the value into the conversation.** That rules out `grep` without `-l`,
and `printenv`, and an `echo` of the variable: the question is where a key is
saved, and a file's name answers it. No output means none of them names the
variable. The exit status says nothing, because a file that does not exist
sets it as well. Where there is no `grep` at all (Windows PowerShell), the
rule is the same for whatever you use in its place: file names only.

**If your client declines the command, you have not looked.** That is "your
own client declining to make a call" in the next section (`references/unreachable.md`), and it is not an
empty result: say that you could not look, and go on to the setup flow without
guessing what it would have found. The rule against a second mint in Setup (in `SKILL.md`)
still holds there, because it never depended on this command.

**Tell the developer what you found in those words.** "A key is saved in
`<file>` but did not reach the server", then the one cause that file points
at and the one thing to do about it. Never "no key", and never an offer to
mint: told there is no key, a developer takes another one, and the first is
still sitting in the file.

**There really is no key only on the last line of that list**, where nothing
that could hold one names the variable. Then run the setup flow above, and ask
before starting either route (in `SKILL.md`).

The key flow itself is the `lexlint-key` skill, named in `SKILL.md`.
