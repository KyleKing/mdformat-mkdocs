# Development & Debugging Best Practices

A collection of systematic approaches to software development and debugging.

## Overview

This document compiles insights on writing better code, debugging methodologies, and becoming a more effective developer.

---

## How to Fix a Bug: A Systematic Approach

**Source:** [How to fix a bug](https://sobolevn.me/2019/01/how-to-fix-a-bug)

The article outlines five key phases for addressing software defects:

### 1. Spotting the Bug
Detection requires awareness of factors like user impact scale, execution environment, and reproducibility difficulty. Tools such as Sentry, Prometheus, and NewRelic help automate discovery.

### 2. Reporting the Bug
Quality bug submissions should establish "why this is problematic, what should occur instead, why it matters, and reproduction steps." The author emphasizes that "screenshots and gifs rock for systems with UI" while noting that stack traces shouldn't be image-captured.

### 3. Reproducing the Bug
Engineers must write failing regression tests to confirm the issue programmatically rather than manually. Debuggers and static analysis tools assist in capturing elusive problems.

### 4. Fixing the Bug
The actual code modification follows once reproduction succeeds and CI builds pass.

### 5. Documenting via Postmortem
Final documentation captures the non-technical narrative, including what caused the issue, resolution steps, user impact, and timeline—creating institutional knowledge for future teams.

The author emphasizes that "bugs happen all the time" and advocates for systematic, blameless processes that prevent recurrence through thorough documentation and testing practices.

---

## Functions vs. Classes: Design Principles

**Source:** [Mediocre Developer](https://sobolevn.me/2018/03/mediocre-developer)

The author recommends a clear hierarchy: "Prefer pure functions over regular functions" and "Prefer regular functions over classes," only using classes "in a strong need." This approach prioritizes simplicity and cognitive efficiency.

### What Makes a Good Developer

According to this piece, excellence isn't about innate genius. Instead, strong developers:

- **Embrace continuous learning** without expecting magical shortcuts
- **Prioritize simplicity** using the "WTFs/Minute" principle—code should be understandable at first glance
- **Implement safeguards** through testing, static typing, code reviews, and automated checks
- **Automate deployment** with Docker and CI/CD tools to catch environment-specific failures
- **Monitor production** using error tracking and logging services
- **Remain humble**, recognizing that "all software has bugs" and distrusting their own work enough to implement multiple verification layers

The core message: quality development isn't reserved for the exceptionally talented—it's achievable through disciplined practices, automation, and acknowledging human limitations.

---

## Python Debugging Techniques

**Source:** [Debugging Python Scripts](https://geo-python.github.io/2017/lessons/L6/debugging-scripts.html)

Key debugging approaches for Python development:

### 1. Test with Known Outputs
Create simplified test cases with predictable results. As the material explains, "we need to know the 'answer' the code should produce" to verify correctness. Using small data subsets allows you to manually calculate expected outcomes before running your full program.

### 2. Ensure Consistent Behavior
"It is a good thing when your code crashes the same way every time you run it." Reproducible errors are easier to isolate and fix than intermittent problems. If your code works sometimes and fails other times, debugging becomes significantly harder.

### 3. Reduce Execution Time
When dealing with large datasets that cause crashes, test your program on smaller data portions first. This dramatically speeds up the debugging cycle—waiting 30 minutes for a crash makes testing inefficient.

### 4. Make Small, Tracked Changes
Use version control (like GitHub) to document modifications incrementally. The documentation emphasizes: "change one thing at a time, test the code, and make more changes if needed." This approach isolates which specific alteration caused a problem, rather than making multiple simultaneous changes that obscure the source of errors.

These strategies collectively reduce debugging time by creating reproducible conditions and enabling systematic problem identification.

---

## Debugging Series: Welcome to the Jungle

**Source:** [Debugging Series 2021](https://thoughtbot.com/blog/debugging-series-2021-welcome-to-the-jungle)

This introductory article launches a multi-part debugging series. While it doesn't detail specific approaches, it previews upcoming topics:

### Planned Coverage
The series will explore "assumptions, charting a course, reading errors, leveraging Git, root causes, classical philosophy, giving up gracefully. And ducks."

### Key Philosophy
Rather than prescribing solutions, this introduction establishes that debugging is a learnable skill deserving formal instruction—something many developers never receive formally during their education.

As stated: "a novice can always learn something from the most arcane subject, and a master can always hone their skills by practicing their fundamentals."

The series positions debugging as a structured discipline worthy of intentional study rather than trial-and-error learning.

---

## Regex Visualization

**Source:** [Regexper](https://regexper.com/#%28a*%29%2B)

*Note: This is a tool rather than an article. Regexper provides visual diagrams of regular expressions, making complex patterns easier to understand and debug.*

Key benefits:
- Visual representation of regex logic flow
- Easier identification of potential issues (e.g., catastrophic backtracking)
- Educational tool for learning regex syntax
- Debugging aid for complex patterns

---

## Summary: Key Debugging Principles

1. **Systematic Approach**: Follow a structured process from spotting to fixing to documenting
2. **Reproducibility**: Ensure bugs can be consistently reproduced before attempting fixes
3. **Incremental Changes**: Make small, tracked changes to isolate problem sources
4. **Automation**: Use tools and tests to catch issues early
5. **Documentation**: Record findings to build institutional knowledge
6. **Simplicity First**: Prefer simple, understandable code over clever complexity
7. **Testing**: Write regression tests to prevent bugs from returning
8. **Version Control**: Track all changes systematically

## Related Tools

- **Error Tracking**: Sentry, Rollbar, Bugsnag
- **Monitoring**: Prometheus, NewRelic, Datadog
- **Debugging**: pdb (Python debugger), IDE debuggers
- **Static Analysis**: mypy, pylint, flake8
- **Visualization**: Regexper for regex, profilers for performance
