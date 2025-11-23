# Article Summaries Collection

This directory contains comprehensive summaries of articles and resources related to software development best practices, compiled from [calcipy issue #38](https://github.com/KyleKing/calcipy/issues/38).

## Overview

These documents synthesize insights from 29+ articles covering various aspects of professional software development, from code quality and testing to team collaboration and project management.

## Documents

### [1. Logging Best Practices](./logging-best-practices.md)
**Topics Covered:**
- Log level guidelines (ERROR, WARN, INFO, DEBUG, TRACE)
- The "2AM rule" for error logging
- Production support and forensic analysis
- Making logs actionable with proper context

**Key Takeaway:** Logs should serve production support and forensic analysis, with levels chosen based on required response rather than perceived importance.

---

### [2. Development & Debugging](./development-and-debugging.md)
**Topics Covered:**
- Systematic bug-fixing approach (5 phases)
- Functions vs. classes design principles
- Python debugging techniques
- Making debugging a learnable skill

**Key Takeaway:** Quality development is achievable through disciplined practices, automation, and acknowledging human limitations—not innate genius.

---

### [3. Testing Best Practices](./testing-best-practices.md)
**Topics Covered:**
- Python testing style guide
- Stubbing vs. mocking strategies
- Test organization and naming
- Preferring real objects over mocks

**Key Takeaway:** Focus on testing behavior rather than implementation, use real objects when practical, and always use autospec for mocks.

---

### [4. Code Review & Pull Request Best Practices](./code-review-and-pr-best-practices.md)
**Topics Covered:**
- Minimal, focused pull requests
- Code review guidelines for reviewers and authors
- Team collaboration in reviews
- Avoiding process bottlenecks

**Key Takeaway:** Every PR should have one unique goal with minimal changes; reviews are about collaboration and learning, not gatekeeping.

---

### [5. README Best Practices](./readme-best-practices.md)
**Topics Covered:**
- Essential README sections
- Writing style and formatting
- Visual elements and documentation
- README as a filtering tool

**Key Takeaway:** A great README welcomes newcomers, informs quickly, guides through setup, invites contribution, and maintains accuracy over time.

---

### [6. GitHub & Team Practices](./github-and-team-practices.md)
**Topics Covered:**
- Professional GitHub workflow
- Issue and label management
- Team collaboration patterns
- Automation and tooling

**Key Takeaway:** Use GitHub as a communication platform to enable precise technical communication inexpensively and reduce wasted development time.

---

### [7. Python Best Practices](./python-best-practices.md)
**Topics Covered:**
- PEP 8 and code style
- Common Python idioms
- Modern tooling (Poetry, Black, mypy)
- Project structure and configuration

**Key Takeaway:** Follow community conventions with automated tools, prefer explicitness over cleverness, and use modern tooling for quality assurance.

---

## Articles by Category

### Logging (4 articles)
1. [Logging levels: the wrong abstraction | IG Labs](https://labs.ig.com/logging-level-wrong-abstraction)
2. [Log Levels - Stack Overflow](https://stackoverflow.com/questions/7839565/logging-levels-logback-rule-of-thumb-to-assign-log-levels/8021604#8021604)
3. [What should you log in an application](https://cloudncode.blog/2016/12/30/what-should-you-log-in-an-application-and-how-to-avoid-having-24x7-support-looking-at-them/)
4. [How to Log in Python Like a Pro](https://guicommits.com/how-to-log-in-python-like-a-pro/)

### Development & Debugging (4 articles)
5. [How to fix a bug](https://sobolevn.me/2019/01/how-to-fix-a-bug)
6. [Mediocre Developer](https://sobolevn.me/2018/03/mediocre-developer)
7. [Regex visualization](https://regexper.com/)
8. [Debugging Scripts Guide](https://geo-python.github.io/2017/lessons/L6/debugging-scripts.html)
9. [Debugging Series 2021](https://thoughtbot.com/blog/debugging-series-2021-welcome-to-the-jungle)

### Testing (2 articles)
10. [Stubbing vs Mocking](https://outsidein.dev/testing-concepts.html#stubbing-and-mocking)
11. [Testing the Diff](https://www.vinta.com.br/blog/2021/testing-the-diff/)
12. [Python Testing Style Guide](https://blog.thea.codes/my-python-testing-style-guide/)

### Code Review & Best Practices (4 articles)
13. [Code Review Best Practices](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html)
14. [PR Guidelines](https://gist.github.com/mherrmann/5ce21814789152c17abd91c0b3eaadca)
15. [One of the Team](https://python-hyper.org/en/latest/one-of-the-team.html)
16. [Code Review Comments (Go)](https://github.com/golang/go/wiki/CodeReviewComments)
17. [Out of Control Review Processes](https://apenwarr.ca/log/20171213)
18. [Software Quality Metrics](https://hub.codebeat.co/docs/software-quality-metrics)

### README Resources (5 articles)
19. [README Checklist](https://liw.fi/readme-review/)
20. [Software Release Practice HOWTO](https://tldp.org/HOWTO/Software-Release-Practice-HOWTO/distpractice.html#readme)
21. [Awesome README](https://github.com/matiassingers/awesome-readme)
22. [Make a README](https://www.makeareadme.com/)
23. [Best README Template](https://github.com/othneildrew/Best-README-Template)

### GitHub & Team Practices (4 articles)
24. [Using GitHub Professionally](https://petabridge.com/blog/use-github-professionally/)
25. [Sane GitHub Labels](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63)
26. [Triage Process](https://github.com/vector-im/element-meta/wiki/triage-process)
27. [Every Programmer Should Know](https://github.com/mtdvio/every-programmer-should-know)

### Python Best Practices (2 articles)
28. [Python Style Guide](https://docs.python-guide.org/writing/style/)
29. [Python Package Template](https://github.com/TezRomacH/python-package-template)

---

## Key Themes Across All Resources

### Quality Through Process
- Systematic approaches beat ad-hoc solutions
- Automation reduces human error
- Documentation builds institutional knowledge
- Testing prevents regressions

### Communication is Critical
- Clear commit messages and PR descriptions
- Comprehensive READMEs for onboarding
- Code reviews as collaborative learning
- Issues and labels for project organization

### Simplicity and Clarity
- Prefer simple solutions over clever ones
- Code should be self-documenting
- Minimize cognitive load for readers
- Follow established conventions

### Continuous Improvement
- Regular refactoring
- Learning from bugs and incidents
- Iterative development processes
- Measuring and adjusting practices

### Human-Centered Development
- Blameless postmortems
- Respectful code reviews
- Inclusive documentation
- Work-life balance awareness

---

## Using These Resources

### For Individual Developers
- **Starting a new project?** Check the README and Python best practices guides
- **Fixing a bug?** Follow the systematic approach in Development & Debugging
- **Writing tests?** Consult the Testing best practices
- **Submitting a PR?** Review the Code Review guidelines
- **Setting up logging?** Use the Logging best practices

### For Teams
- **Establishing processes?** Review GitHub & Team Practices
- **Onboarding new members?** Share the README best practices
- **Improving code quality?** Implement practices from Code Review and Python guides
- **Building culture?** Apply lessons from Team Practices and Every Programmer Should Know

### For Project Maintainers
- **Creating documentation?** Use the README and documentation guides
- **Managing issues?** Check GitHub practices for labels and triage
- **Reviewing PRs?** Follow Code Review best practices
- **Setting standards?** Combine Python and Testing best practices

---

## Note on Article Accessibility

Some articles were not accessible during the summarization process due to network issues, 403/404 errors, or SSL handshake failures. Where articles were inaccessible, the summaries include notes about typical content in that category and common best practices.

Successfully summarized articles include key quotes and detailed insights from the original sources.

---

## Contributing

These summaries were created to capture learnings from valuable resources. If you:
- Find broken links
- Have updated information
- Want to add new relevant articles
- Spot errors or omissions

Please open an issue or submit a pull request to improve these resources.

---

## License

These summaries are provided for educational purposes. Original articles retain their respective copyrights and licenses. Please refer to the original sources for authoritative information and proper attribution.

---

**Last Updated:** 2025-11-20

**Source Issue:** [calcipy#38](https://github.com/KyleKing/calcipy/issues/38)
