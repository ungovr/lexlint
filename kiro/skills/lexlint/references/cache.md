<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

## Cache what you fetched

Every `get_law` call is one lookup, and it costs one upstream request, plus
one more for each parent the resolution walk passes through on the way. A
triage pass that re-reads the same instruments of the same six jurisdictions
while working the lanes spends most of a day's free tier re-downloading law
that did not change.

### Read the index, then the instruments

A bare `get_law` returns the jurisdiction's index, and says so in
`detail: "index"` and in its `note`: one short row per instrument, with its
`record_id`, `name`, `status`, `topics` and `in_force`, and none of what the
instrument requires. To read that, call again with the same `jurisdiction`
argument the index call used and up to 5 `record_id` values in `instrument`.
The answer has `detail: "instrument"`, those instruments in full, and in
`not_found` any id this jurisdiction does not hold, which usually means the id
came from another jurisdiction's index. `topic` narrows the index to one topic
by its slug. `detail: "full"` returns every instrument in full in one call,
which for the largest jurisdictions runs to millions of characters: ask for it
only when the developer wants the whole file, and expect your client to save
it to a file rather than show it.

So persist what you read, into the repo you are working in:

```
.lexlint/
  jurisdictions/
    us.json
    us/ca.json
    eu.json
```

Add `.lexlint/` to `.gitignore` unless the developer asks for it committed.
Committing it deliberately is a reasonable choice and often a good one: it
turns "the law changed underneath us" into a diff a reviewer can read.
Committing it by accident is neither, so ask rather than assume.

Each file is one jurisdiction. It holds the instruments you read in full,
keyed by `record_id`, the index you found them in, kept apart, and the fields
that make it checkable:

```json
{
  "slug": "us/ca",
  "as_of_date": "2026-08-12",
  "index": { "cached_at": "2026-08-25T20:31:00Z", "rows": [ ] },
  "instruments": {
    "us/ca:1a2b3c4d5e6f": { "cached_at": "2026-08-25T20:33:00Z", "row": { } }
  }
}
```

`as_of_date` is the response's own `provenance.as_of_date`, lifted to the top
level so the check below can run without parsing the whole file. Each part
carries its own `cached_at`, because instruments join the file as you read
them. Keep an index under `index` only when it was asked for without `topic`:
a `topic` call answers with part of the index, and cached there it would later
read as every instrument the jurisdiction holds.

**Never cache an index as the law.** An index row names an instrument and
carries none of its duties. It never goes under `instruments`, and nothing is
quoted, cited as a requirement or counted as covered from `index`. An
instrument is under `instruments` only when an `instrument` call, or a
`detail: "full"` call, returned it in full.

**Key on the resolved slug, never the requested one.**
`get_law("us/ca/santa-barbara")` answers from `us/ca`, the jurisdiction whose
law reaches the city. The resolved slug is the response's own
`jurisdiction.slug`, and that is the key. `resolved_from` is the other one: it
holds the slug you asked for, and it is present only when another
jurisdiction's law answered.
Every `record_id` starts with the resolved slug (`us/ca:1a2b3c4d5e6f`), so an
instrument whose id names another slug does not belong in the file. Filed
under what was asked for, one row of the law library lands in the cache
repeatedly under slugs `check_access` has never heard of, and not one of those
entries can be revalidated.

### Revalidating is free, so do it every run

`set_profile` is already a call of every run, and it reports `as_of_date` for
each declared slug in that one request. That is the whole freshness check:
compare each cached `as_of_date` against what `set_profile` just reported, and
re-fetch only what moved. A cache of any size revalidates inside a call you were
making anyway, so there is no size at which checking costs more than not
checking.

Do **not** pass `jurisdictions` to `check_access` to get these dates. It answers
the same question `set_profile` already answers, off a request `check_access`
spends either way: asking both costs nothing extra, it just gives you the same
dates twice. Read them from `set_profile`, so there is one place to look, not two.

Start a jurisdiction's file over, and fetch what you need again, when any of
these holds:

- `set_profile` reports an `as_of_date` the cached copy does not carry, or a
  response you just fetched for it carries another `as_of_date`.
- The file does not parse, its `slug` is not the response's
  `jurisdiction.slug`, or an instrument in it has an id that names another
  slug. Delete it and fetch. An entry LexLint cannot read is not a cache hit.
- A file with a top-level `payload` is in the shape earlier bundles wrote,
  before `get_law` answered with an index, and that payload may be an index
  saved as if it were the law. Delete it and fetch, whatever its `as_of_date`
  says.

Re-fetch one part of the file, the index or one instrument, when its
`cached_at` is more than 24 hours old. `as_of_date` is a review date rather
than a build stamp, so a correction that does not move it is invisible to the
comparison above, and the 24-hour bound is what limits how long such an edit
can be served from disk.

### What the cache must never do

**It must never create coverage.** If `check_access` reports `held: false` for
a slug, a copy cached while it was held does not make it held. Report the
coverage warning exactly as a run with no cache would. Coverage is what the
law library holds now, and a local file answering otherwise is the reassuring wrong
answer with a cache in front of it.

**It must never feed the lint.** `run_lint` reads the law library
server-side and verifies it against the published manifest, by row count, byte
count and digest, on every run. Nothing hands it a cached copy, and that is
deliberate: the verification is what stops a half-published law library from linting
clean, so a cache able to reach it would be a way to skip it. Findings are not
cached either, for the same reason `lint.vanished` exists.

**It must never be quiet about itself.** Extend the status line the run already
prints:

```
lexlint 1.86.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
cache: 5 jurisdictions held, 1 refreshed
```

Someone reading a citation is owed the knowledge of whether it was read from
the law library this minute or from a copy taken yesterday.

Domain resolutions need none of this. `profile.domains` in `lexlint.yml`
already records them, so a domain sitting there is not resolved a second time.
