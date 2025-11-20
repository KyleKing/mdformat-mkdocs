# Code Review & Pull Request Best Practices

A collection of best practices for code reviews and pull request management.

## Overview

This document compiles insights on conducting effective code reviews, submitting quality pull requests, and maintaining high code quality through peer review processes.

---

## Good PRs Are Minimal

**Source:** [PR Guidelines](https://gist.github.com/mherrmann/5ce21814789152c17abd91c0b3eaadca)

### Core Principle
"Every PR should have one, and only one, unique goal." Contributors should make the absolute minimum changes necessary to achieve that single objective.

### Specific Guidelines

**What to Avoid:**
- Unnecessary whitespace modifications (tabs/spaces conversions create excessive line changes)
- Running linters across the entire codebase as a side effect
- Introducing new tools or dependencies unless absolutely essential
- Deviating from the project's established code style

**What to Follow:**
- Match existing conventions for tabs/spaces, line length limits, and quote styles
- Keep changes focused and reviewable
- Submit multiple improvements as separate PRs rather than combining them

### The Rationale

The maintainer emphasizes that reviewers must examine every change you make. A minimal, focused PR is easier to understand, review, and approve. This approach respects the reviewer's limited time and demonstrates consideration for the maintenance burden your contribution creates.

**Key Takeaway:** Quality PRs prioritize clarity and minimalism over comprehensiveness in a single submission.

---

## Code Review Best Practices

**Source:** [Code Review Best Practices - Kevin London](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html)

*Note: This article was not accessible during summarization. Common code review best practices include:*

### For Reviewers
- **Be Kind and Constructive**: Frame feedback positively
- **Ask Questions**: "What do you think about...?" vs "This is wrong"
- **Provide Context**: Explain why something matters
- **Praise Good Code**: Acknowledge clever solutions or improvements
- **Review Thoroughly**: Don't rubber-stamp; actually read the code
- **Use Checklists**: Ensure consistent review quality

### For Authors
- **Keep PRs Small**: Easier to review, faster to merge
- **Provide Context**: Explain the why, not just the what
- **Self-Review First**: Catch obvious issues before requesting review
- **Respond Promptly**: Keep the review cycle moving
- **Be Open to Feedback**: Remember reviews improve code quality

### Review Focus Areas
1. **Functionality**: Does the code do what it's supposed to?
2. **Tests**: Are there sufficient tests? Do they test the right things?
3. **Design**: Is the approach sound? Are there better alternatives?
4. **Complexity**: Is the code as simple as it can be?
5. **Naming**: Are variables, functions, and classes well-named?
6. **Documentation**: Are complex parts explained?
7. **Security**: Are there potential vulnerabilities?
8. **Performance**: Are there obvious performance issues?

---

## Code Review Comments (Go Wiki, Generally Applicable)

**Source:** [Go Wiki - Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)

*Note: This article was not accessible during summarization. While Go-specific, many principles apply universally:*

### General Principles
- **Consistency**: Follow established patterns in the codebase
- **Clarity**: Prefer obvious code over clever code
- **Error Handling**: Handle errors explicitly and appropriately
- **Context**: Pass context through call chains when needed
- **Naming**: Use clear, descriptive names; avoid abbreviations

### Common Review Points
- Variable shadowing issues
- Error return conventions
- Interface design principles
- Package organization
- Comment formatting and content
- Import grouping and ordering

---

## Out of Control Review Processes

**Source:** [Talk on out of control review processes](https://apenwarr.ca/log/20171213)

*Note: This article was not accessible during summarization. Common themes in this type of discussion:*

### When Review Processes Fail
- Too many required reviewers creates bottlenecks
- Perfectionism prevents shipping
- Trivial changes receive disproportionate scrutiny
- Review becomes gatekeeping rather than collaboration
- Inconsistent standards across reviewers

### Fixing Broken Processes
- **Time-box Reviews**: Set reasonable review time limits
- **Trust and Autonomy**: Empower developers to make decisions
- **Tiered Review**: Match review rigor to change importance
- **Clear Guidelines**: Document what matters in reviews
- **Measure Impact**: Track review time vs. bug rates
- **Culture Change**: Foster collaboration, not gatekeeping

---

## Software Quality Metrics

**Source:** [Software Quality Metrics](https://hub.codebeat.co/docs/software-quality-metrics)

*Note: This article was not accessible during summarization. Common quality metrics include:*

### Code Quality Metrics
- **Complexity**: Cyclomatic complexity, cognitive complexity
- **Duplication**: Code clone detection
- **Coverage**: Test coverage percentages
- **Debt**: Technical debt indicators
- **Churn**: Frequency of changes to files (instability indicator)

### Using Metrics in Reviews
- Identify high-complexity functions needing refactoring
- Track coverage trends
- Flag excessive duplication
- Prioritize review attention on high-churn, high-complexity areas

### Metrics Limitations
- Metrics are indicators, not absolute measures
- Context matters more than raw numbers
- 100% coverage doesn't mean bug-free code
- Low complexity can still be poorly designed

---

## Team Collaboration & Pull Request Culture

**Source:** [One of the Team - Python Hyper](https://python-hyper.org/en/latest/one-of-the-team.html)

The Hyper project establishes a community-focused approach to open source development with tiered contribution levels:

### Contributor Guidelines

Any developer who commits to a Hyper sub-project automatically joins the contributors team, gaining authority to merge pull requests and manage issues. However, the project emphasizes collaborative responsibility through three key expectations:

1. **Peer Review Requirements**: Contributors must refrain from merging their own work, as "code review is important, and skipping it is bad."

2. **Maintainer Approval**: Changes should only be merged after a maintainer or administrator approves them, ensuring alignment with project vision.

3. **Conduct Standards**: All contributors must follow the project's code of conduct outlined in their contributing policy.

### Maintainer Role

Those demonstrating sustained valuable contributions may advance to sub-project maintainer status, gaining direct master branch access and permission management authority. These individuals serve dual roles as "stewards of culture, as much as they are of code," responsible for enforcing policies and fostering an inclusive contributor environment.

The framework balances distributed decision-making with strategic oversight, acknowledging that "the maintainers are responsible for the 'spirit' of the project" while encouraging widespread participation in the ecosystem.

---

## Best Practices Summary

### For Submitting PRs
1. **Single Purpose**: One goal per PR
2. **Small Changes**: Easier to review and merge
3. **Self-Review**: Catch issues before requesting review
4. **Good Descriptions**: Explain what, why, and how
5. **Tests Included**: Demonstrate functionality and prevent regressions
6. **Follow Conventions**: Match existing code style
7. **Respond Promptly**: Keep review cycles moving

### For Reviewing PRs
1. **Be Respectful**: Kind, constructive feedback
2. **Be Thorough**: Actually read and understand the code
3. **Ask Questions**: Seek to understand before criticizing
4. **Acknowledge Good Work**: Positive reinforcement matters
5. **Explain Context**: Help the author learn
6. **Focus on Important Issues**: Don't bikeshed minor style points
7. **Approve or Request Changes**: Don't leave PRs in limbo

### For Process Management
1. **Set Expectations**: Clear guidelines on what gets reviewed
2. **Time-box Reviews**: Don't let PRs stagnate
3. **Automate Checks**: Use CI for style, tests, linting
4. **Trust the Team**: Enable autonomy within guidelines
5. **Measure and Improve**: Track metrics, adjust process
6. **Foster Collaboration**: Review is learning, not gatekeeping

### Red Flags in Reviews
- **Rubber Stamping**: Approving without actually reviewing
- **Bikeshedding**: Endless debate over trivial issues
- **Gatekeeping**: Using review as power play
- **Inconsistency**: Different standards for different people
- **Ghosting**: Requesting changes then disappearing
- **Perfectionism**: Blocking over minor improvements

## Tools and Automation

### Review Automation
- **Linters**: Automated style checking (flake8, pylint, black)
- **Type Checkers**: Static analysis (mypy, pyright)
- **Security Scanners**: Vulnerability detection (bandit, safety)
- **Coverage Tools**: Test coverage reporting
- **CI/CD**: Automated test running and validation

### Review Platforms
- **GitHub**: Pull requests, review comments, suggestions
- **GitLab**: Merge requests, inline discussions
- **Gerrit**: Change-based code review
- **Phabricator**: Differential code review

### Communication
- **Code Comments**: Inline explanations in PRs
- **Conventional Comments**: Standardized comment prefixes (nit, question, suggestion)
- **Review Apps**: Deploy preview environments
- **Status Checks**: Required CI passes before merge

## Further Reading

- [Google Engineering Practices - Code Review](https://google.github.io/eng-practices/review/)
- [Effective Code Reviews Without the Pain](https://www.developer.com/tech/article.php/3579756)
- [How to Do Code Reviews Like a Human](https://mtlynch.io/human-code-reviews-1/)
- [The Art of Humanizing Pull Requests](https://blog.dnsimple.com/2016/10/the-art-of-humanizing-pull-requests/)
