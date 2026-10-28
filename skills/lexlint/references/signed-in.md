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
lexlint 1.61.0 · signs in when asked · free law lookups: 18 of 25 left, reset at UTC midnight
```

Do not ask anyone to sign in before a tool asks for it: a person who only came
to read a law never needs to.

**When a tool answers that sign-in is needed, stop and say how to sign in.** A
tool in `sign_in.needed_for` answers that way every time on this install, and
a lookup does once the free ones are used up. Give the person the step for the
client they are in:

- In a coding client, open its list of connected servers, choose lexlint, and
  sign in. Your client's entry in `references/clients.md` gives the exact step
  where it has one.
- In the Claude apps, approve the Connect prompt.

Once they have signed in, run the same step again.

Signing in to LexLint from Codex is not open yet, so a Codex user keeps the
key route above (in `SKILL.md`): their key in an `X-API-Key` header.
