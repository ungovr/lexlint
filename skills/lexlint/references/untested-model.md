<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### When you are not running a model LexLint is tested against

Every `check_access` response also says which models LexLint's procedure is
exercised against. `tested_model_families` holds lowercase tokens, a model
family or, where a client never tells its model the family, the product, and
`model_notice` is the sentence to show. The policy comes down; nothing about
your model goes up. LexLint is never told which model you are, and
`check_access` has no argument that could carry it, because the only thing that
knows which model is reading this file is you.

**You know which model you are. Do not go looking for it.** A model id read out
of a config file, an environment variable or a settings dump names whatever that
file says, which is not necessarily the model reading this line.

**What you were told is your model id, all of it, the product name included.**
Some clients give a model its exact id. Others tell it only the product it
runs in and a model generation, "X, an agent based on GPT-6", and never the
tier, so there the product name is the only word that can match, and leaving it
out stops the run on a notice that names the very model running it.

Lowercase that, split it into words on every character that is not a letter,
and test whether any one of those words is exactly a token in
`tested_model_families`. **Whole words, never substrings.** `solar-pro` is not
`sol` and `octopus-v2` is not `opus`, and a substring rule clears both: it
fails by staying silent about a model nobody has tested, which is the one
failure this section exists to prevent.

If one of your words is a token, say nothing. A developer told their setup is
fine learns to skim the preflight, and this is a footnote to their lint either
way.

If it does not, name the model you are and print `model_notice` verbatim, then
ask:

```
LexLint on claude-sonnet-5.

  <model_notice, printed verbatim, wrapped to your output width>

  Continue on this model, or switch and re-run?
```

The notice is **not reproduced here on purpose.** It is server-owned so that
which models are tested can change without every frozen install having to be
updated, and a copy of its wording in this file would be a second source of
truth that goes stale the first time the tested set moves. It did: this block
quoted a two-model sentence for as long as the set had two models in it. Print
what the response hands you.

Then do what they say. **Continuing is a real answer**, and the lint that
follows is the normal one: this is an advisory rather than a gate, nothing here
can verify a model it was told about, and refusing to work would trade a
possible weakness for a certain failure.

**If there is nobody to ask, print it and lint anyway.** A CI job, a cron run
and a dispatched subagent have no developer in them, and silence must never
resolve to a refusal. The warning belongs in the transcript regardless, where
whoever reads the findings later can see what produced them.

If the fields are absent, say nothing about models at all. An older server does
not answer this, and absent is not the same as unsuitable.

`run_lint` returns the same two fields, for the run that never called the
preflight at all. **Say it once per session**, in the opening lines, exactly as
with a stale version: a warning repeated on every result is one an agent learns
to skip past. If you already showed it at the preflight, the copy on the lint is
the same policy arriving twice, not a second thing to report.
