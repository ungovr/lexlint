<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### When the response says a newer LexLint exists

An installed plugin is frozen at the version it was installed at. Nothing
updates it on its own, and a developer running a stale one gets today's data
through last month's instructions: the server can hand back a field that the
installed skill has never heard of, and the run quietly does nothing with it.
That has already happened once, which is why `check_access` answers the
question at all.

`update_available` is three-valued, and only `true` is an instruction:

- **`true`**: say so once, plainly, in the run's opening lines, and give the
  update step from your own client's entry in `references/clients.md`. Do not
  make it the whole report and do not repeat it: it is a footnote to their
  lint, not the reason they came.

  ```
  lexlint 1.4.0 · a newer LexLint (1.63.0) is available
  ```

  Where that entry says updating is not available, give its reason instead.
  When they ask why an update did not take: it only loads at session start,
  and the entry names any trap of its own.

- **`false`**: nothing to say. Print the version on the status line and move
  on.
- **`null`**: LexLint learned nothing about your version, which is not the
  same as being current. Say nothing about updates at all: a guess here either
  sends a current developer to run a pointless command or reassures a stale one.

The lint is what they asked for. Run it either way: a stale plugin still lints,
and refusing to work until someone updates would be a worse failure than the
one this exists to catch.

Once the repo has a cache, that same line carries its state: see "Cache what
you fetched" (`references/cache.md`).
