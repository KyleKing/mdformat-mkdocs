# Maintaining the security guard

`test_security.py` guards the render layer against ReDoS (catastrophic regex
backtracking) and XSS (unescaped interpolation in default render rules). The open
question is how to keep its payloads correct and complete as the plugin grows,
without hand-maintaining a payload per regex.

## The problem with hand-authored payloads

A fixed list of adversarial strings rots: someone adds a regex or a render sink,
the payload list doesn't grow with it, and the guard reports green while covering
nothing. We want coverage to track the plugin automatically, and to *know* when it
doesn't.

## Three layers, chosen by cost

The guard uses a layered approach rather than one mechanism, because each catches a
different failure mode.

1. **Behavioral guard, fixture-derived (default, always on).** `test_security.py`
   reads the plugin's own render fixtures and amplifies a homogeneous character run
   inside each one. Every fixture is a known-valid activation, so the amplified
   variant reaches the real regexes without naming them. Adding a fixture grows the
   fuzz corpus for free. This is the primary regression guard: fast, deterministic,
   no flakiness. XSS stays an explicit `_INJECTION_CASES` list, because a probe only
   tests a sink if it actually lands in that sink, which fixtures can't guarantee.

2. **AST reachability check (default, always on, `test_regex_reachability.py`).**
   The gap in layer 1 is silent: if a new regex is anchored past a lead-in that no
   fixture produces (e.g. `` ^```math ``), the fuzz corpus never reaches it and the
   miss is invisible. This test statically extracts every regex literal from the
   plugin package, reconstructs each pattern's literal prefix, and asserts at least
   one fixture-derived payload contains that prefix. It answers "are we fuzzing every
   regex?" objectively, and names the ones we aren't. It runs as part of the normal
   `pytest` suite, so it rides the existing CI job; when it fails, add a fixture that
   exercises that syntax (which also improves render coverage). This is the only
   layer that measures completeness instead of assuming it.

3. **Hypothesis deep-fuzz (optional, opt-in profile).** Layers 1–2 only vary the
   *amplification* of known-shaped inputs. To explore unknown-shaped inputs, add a
   Hypothesis strategy that composes the plugin's grammar from its fixtures (reuse
   the fixture inputs as `st.sampled_from` building blocks, interleave homogeneous
   runs and HTML metacharacters) and renders under the same time budget and XSS
   assertion. Because property-based runs are slower and can be flaky under a hard
   timeout, gate it behind `HYPOTHESIS_PROFILE` (see `tests/test_hypothesis.py`) and
   run it nightly, not on every push. It finds the next class of bug; it should not
   block a PR.

## Recommendation

Keep layers 1 and 2 always on — both are cheap, deterministic, and ride the existing
`pytest` job. Reach for layer 3 only once the plugin's grammar is non-trivial and you
want continuous exploration beyond the fixture set. The through-line is that fixtures
are the single source of truth: they drive rendering tests, the ReDoS corpus, the
reachability check, and the Hypothesis building blocks, so investing in fixture
coverage improves every layer at once.
