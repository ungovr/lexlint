<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

## Cache what you fetched

A jurisdiction payload is roughly 10 KB and costs one upstream request every
time it is read, plus one more for each parent the resolution walk passes
through on the way. A triage pass that re-reads the same six jurisdictions
while working the lanes spends most of a day's free tier re-downloading law
that did not change.

So persist what `get_law` returns, into the repo you
are working in:

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

Each file holds the payload plus the two fields that make it checkable:

```json
{
  "slug": "us/ca",
  "as_of_date": "2026-08-12",
  "cached_at": "2026-08-25T20:31:00Z",
  "payload": { }
}
```

`as_of_date` is the payload's own `provenance.as_of_date`, lifted to the top
level so the check below can run without parsing the whole file.

**Key on the resolved slug, never the requested one.** `get_law("us/ca/sf")`
walks up and answers from `us/ca`. The resolved slug is the payload's own
`jurisdiction.slug`, and that is the key. `resolved_from` is the other one: it
holds the slug you asked for, and it is present only when a parent answered.
Filed under what was asked for, one row of the law library lands in the cache repeatedly
under slugs `check_access` has never heard of, and not one of those entries can
be revalidated.

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

Re-fetch a jurisdiction when any of these holds:

- `set_profile` reports an `as_of_date` the cached copy does not carry.
- The cached entry is more than 24 hours old. `as_of_date` is a review date
  rather than a build stamp, so a correction that does not move it is invisible
  to the comparison above, and the 24-hour bound is what limits how long such
  an edit can be served from disk.
- The file does not parse, or its envelope disagrees with the payload inside.
  Delete it and fetch. An entry LexLint cannot read is not a cache hit.

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
lexlint 1.65.0 · key: set · server: reachable · quota: 47 of 50 remaining, resets 17:00 PT
cache: 5 jurisdictions held, 1 refreshed
```

Someone reading a citation is owed the knowledge of whether it was read from
the law library this minute or from a copy taken yesterday.

Domain resolutions need none of this. `profile.domains` in `lexlint.yml`
already records them, so a domain sitting there is not resolved a second time.
