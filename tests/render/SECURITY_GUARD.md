# Maintaining the security guard

`test_security.py` guards against ReDoS (catastrophic regex backtracking) and XSS
(unescaped interpolation in default render rules). The question is how payloads
stay complete as the plugin grows without hand-maintaining one per regex.

## Plugins of every shape

An mdformat plugin may ship markdown-it syntax, renderers, postprocessors, or any
combination. A guard written against a markdown-it plugin symbol only fits the
first kind, so this one goes through `update_mdit` and the plugin's mdformat
extension name instead, both of which every plugin has.

The consequence worth knowing: the ReDoS timing path calls `mdformat.text`, not
`MarkdownIt.render`, because a postprocessor-only plugin contributes nothing to an
HTML render and its regexes would never run. The XSS path does render HTML, since
that is where an escaping bug shows up, and a plugin with no render rules has no
such sink and keeps `_INJECTION_CASES` empty.

## The problem with hand-authored payloads

A fixed list of adversarial strings rots: someone adds a regex or a render sink,
the payload list doesn't grow with it, and the guard reports green while covering
nothing. Coverage should track the plugin automatically and report when it doesn't.

## Three layers, chosen by cost

Each layer catches a different failure mode.

1. **Behavioral guard, fixture-derived (default, always on).** `test_security.py`
   reads the plugin's own render and format fixtures and amplifies a homogeneous
   character run inside each one. Every fixture is a known-valid activation, so the amplified
   variant reaches the real regexes without naming them. Adding a fixture grows the
   fuzz corpus for free. This is the primary regression guard: fast, deterministic,
   no flakiness. XSS stays an explicit `_INJECTION_CASES` list, because a probe only
   tests a sink if it lands in that sink, which fixtures can't guarantee.

2. **AST reachability check (default, always on, `test_regex_reachability.py`).**
   Layer 1 fails silently: a regex anchored past a lead-in no fixture produces
   (e.g. `` ^```math ``) never sees the fuzz corpus, and nothing reports the miss.
   This test extracts every regex literal from the package, reconstructs each
   pattern's literal prefix, and asserts some fixture-derived payload contains it.
   It names any regex we aren't fuzzing and runs in the normal `pytest` suite. When
   it fails, add a fixture for that syntax (which also improves render coverage).
   This is the only layer that measures completeness instead of assuming it.

3. **Hypothesis deep-fuzz (optional, opt-in profile).** Layers 1 and 2 only vary the
   *amplification* of known-shaped inputs. To explore unknown-shaped inputs, add a
   Hypothesis strategy that composes the plugin's grammar from its fixtures (reuse
   the fixture inputs as `st.sampled_from` building blocks, interleave homogeneous
   runs and HTML metacharacters) and renders under the same time budget and XSS
   assertion. Because property-based runs are slower and can be flaky under a hard
   timeout, gate it behind `HYPOTHESIS_PROFILE` (see `tests/test_hypothesis.py`) and
   run it nightly, not on every push. It finds the next class of bug and should not
   block a PR.

## Recommendation

Keep layers 1 and 2 always on: cheap, deterministic, already in the `pytest` job.
Add layer 3 once the grammar is non-trivial and you want exploration beyond the
fixture set. Fixtures drive the rendering tests, the ReDoS corpus, the reachability
check, and the Hypothesis building blocks, so adding one improves every layer at
once.
