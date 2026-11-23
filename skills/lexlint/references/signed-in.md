<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### When this install signs in instead of using a key

Some installs carry no key at all. The copy of LexLint listed in a client's
directory connects with no key header, and the person signs in to a LexLint
account when a tool asks them to. `check_access` reports that as
`credential: "none"`.

**When it does, skip the key routes above (in `SKILL.md`) and never call `claim_trial_key`.**
There is no saved key to look for and no trial to mint from this install, and
`key_present: false` is the expected answer here, not a problem to report. The
tools that need sign-in are the ones in `sign_in.needed_for`.

**Law lookups work straight away.** `get_law` and
`resolve_domain_jurisdiction` answer with no account, up to the limit
`free_lookups` reports: `free_lookups.remaining` of `free_lookups.limit` are
left, and the count resets at `free_lookups.resets`. A null `remaining` means
the server could not count, never that none are left. Show it on the preflight
line where the key would go:

```
lexlint 1.86.0 · signs in when asked · free law lookups: 18 of 25 left, reset at UTC midnight
```

Do not ask anyone to sign in before a tool asks for it: a person who only came
to read a law never needs to.

**Where your client's entry in `references/clients.md` says signing in is not
open from it, do not call a tool in `sign_in.needed_for` at all, nor a lookup
once `free_lookups.remaining` is 0.** Both answer by asking for a sign-in, some
clients start that sign-in themselves the moment they are asked, and from a
client it is not open to, it can only fail. Stop before the call, keep to the
law lookups while they last, say when they reset once they are spent, and give
the route that entry names for a lint.

**When a tool answers that sign-in is needed, stop and say how to sign in.** A
tool in `sign_in.needed_for` answers that way every time on this install, and
a lookup does once the free ones are used up. Give the person the step for the
client they are in:

- In a coding client, open its list of connected servers, choose lexlint, and
  sign in. Your client's entry in `references/clients.md` gives the exact step
  where it has one.
- In the Claude apps, approve the Connect prompt.

Once they have signed in, run the same step again.

**A sign-in that fails is a stop, the same as a server that did not
answer** (`references/unreachable.md`).
A registration error, a refused consent, any error from the sign-in itself:
name the step that needed it, quote the error you got, report no findings, and
give the route that does work, from your client's entry in Client
setup (`references/clients.md`). Do not start the sign-in again unasked. What is
left of the request after that is the law lookups, as Setup
says (in `SKILL.md`), and nothing from memory in the lint's place.

Signing in to LexLint from Codex is not open yet, so a Codex user keeps the
key route above (in `SKILL.md`): their key in an `X-API-Key` header.
