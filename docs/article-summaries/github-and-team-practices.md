# GitHub & Team Practices

Best practices for using GitHub professionally and managing software projects effectively.

## Overview

This document compiles insights on professional GitHub usage, issue management, team collaboration, and project organization.

---

## Using GitHub Professionally

**Source:** [Using GitHub Professionally](https://petabridge.com/blog/use-github-professionally/)

### Key Workflow Recommendations

#### Before Coding: Create Issues First
- File issues to prevent "false starts" and "blind alleys" through early team discussion
- Use issue templates to standardize information collection
- Apply labels sparingly for meaningful organization
- Group related work into milestones to communicate project priorities

#### During Development: Submit Pull Requests Early
The guide emphasizes: "Don't 'Hold' a Pull Request Until the Job is 'Done'" — submit proposals promptly rather than waiting for completion.

### Collaboration Techniques

**Code Discussion:**
- Use GitHub permalinks to reference specific code sections with full context
- Cross-link related issues across pull requests and projects
- Reference issue numbers in commit messages for automatic tracking

**Pull Request Management:**
- Keep PRs small and focused; break large tasks into independent requests
- Always work on feature branches, never submit from main development branches
- Self-review your own changes first to guide external reviewers

**Technical Safeguards:**
- Require continuous integration to pass before merging
- Keep branches updated before integrating changes
- Use branch protection rules to maintain code quality

### Core Philosophy

The underlying principle centers on leveraging GitHub as a communication platform. As noted, the goal is enabling "precise technical communication inexpensively" to reduce wasted development time and improve team coordination.

---

## Sane GitHub Labels

**Source:** [Sane GitHub Labels](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63)

*Note: This article was not accessible during summarization. Common approaches to GitHub label systems:*

### Label Categories

**By Type:**
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `refactor` - Code restructuring
- `test` - Test additions or fixes

**By Priority:**
- `priority: critical` - Must be fixed immediately
- `priority: high` - Important, fix soon
- `priority: medium` - Normal priority
- `priority: low` - Nice to have

**By Status:**
- `status: blocked` - Waiting on something else
- `status: needs discussion` - Requires team input
- `status: in progress` - Currently being worked on
- `status: ready for review` - Awaiting code review

**By Area:**
- `area: frontend` - UI/UX changes
- `area: backend` - Server-side logic
- `area: api` - API changes
- `area: database` - Data layer

### Label Best Practices
- Use colors consistently (red for urgent, yellow for medium, etc.)
- Keep the total number manageable (15-25 labels)
- Document label meanings in CONTRIBUTING.md
- Combine labels rather than creating too many specific ones
- Use label automation with tools like Probot

---

## Triage Process

**Source:** [Triage Process - Element/Matrix](https://github.com/vector-im/element-meta/wiki/triage-process)

*Note: This article was not accessible during summarization. Common triage best practices:*

### Issue Triage Workflow

**1. Initial Assessment**
- Is this a valid issue?
- Is it a duplicate?
- Is there enough information to act on it?

**2. Categorization**
- Apply appropriate labels
- Assign to correct project/milestone
- Determine priority

**3. Response**
- Acknowledge the issue
- Ask for clarification if needed
- Set expectations for resolution

**4. Assignment**
- Assign to team member if appropriate
- Leave unassigned for community contribution
- Link to related issues or PRs

### Triage Frequency
- Critical bugs: Immediate
- High priority: Daily
- Normal issues: Weekly
- Low priority: Monthly

### Closing Issues
- Fixed/resolved
- Won't fix (with explanation)
- Duplicate (link to original)
- Cannot reproduce (after reasonable effort)
- Stale/abandoned

---

## Every Programmer Should Know

**Source:** [Every Programmer Should Know](https://github.com/mtdvio/every-programmer-should-know)

This comprehensive resource identifies essential topics every developer should master:

### Foundational CS Concepts
Algorithms, data structures, complexity analysis (Big O), and number theory form the technical bedrock.

### System-Level Knowledge
Understanding memory management, latency benchmarks, time/timezone handling, and distributed systems principles is crucial for writing performant code.

### Practical Skills
String handling (Unicode, encoding), regular expressions, security best practices, and cryptography protect applications from vulnerabilities.

### Architecture & Design
Developers benefit from learning system design patterns, code organization principles, and evolutionary architecture approaches.

### Professional Development
The guide emphasizes soft skills—problem-solving, communication, and mental health—alongside career guidance on negotiation, remote work, and technical interviewing.

### Modern Practices
Topics include testing methodologies, refactoring legacy code, open-source contribution, and emerging disciplines like Platform Engineering focused on developer experience.

### Continuous Learning
The resource recommends studying academic papers, engaging with coding practice platforms (LeetCode, HackerRank), and exploring multiple programming paradigms.

The overarching message: becoming an excellent programmer requires balancing deep technical knowledge with practical engineering wisdom and human-centered soft skills.

---

## Team Practices Summary

### Issue Management

**Creating Good Issues:**
1. **Clear Title**: Descriptive, specific
2. **Problem Statement**: What's wrong or what's needed
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What currently happens (for bugs)
5. **Steps to Reproduce**: Clear, numbered steps
6. **Environment**: OS, version, browser, etc.
7. **Screenshots/Logs**: Visual aids when helpful
8. **Acceptance Criteria**: Definition of "done"

**Issue Templates:**
- Bug report template
- Feature request template
- Documentation improvement template
- Custom templates for project-specific needs

**Issue Hygiene:**
- Close stale issues (use bots like Stale)
- Keep issues focused on one topic
- Update status with labels
- Link related issues
- Archive obsolete issues

### Project Organization

**Milestones:**
- Group related issues
- Set target dates
- Track progress toward goals
- Communicate roadmap

**Projects (Boards):**
- Kanban-style workflow
- Columns: Backlog, To Do, In Progress, Review, Done
- Automate card movement
- Link issues and PRs

**Releases:**
- Semantic versioning
- Changelog generation
- Release notes
- Tag strategy

### Team Communication

**Commit Messages:**
- Use conventional commits format
- Reference issue numbers
- Explain why, not just what
- Keep first line under 50 characters

**PR Descriptions:**
- Link to related issues
- Explain approach
- Highlight breaking changes
- Include testing notes
- Add screenshots for UI changes

**Code Comments:**
- Explain why, not what
- Document non-obvious decisions
- Link to relevant issues/discussions
- Keep comments updated

### Automation

**GitHub Actions:**
- CI/CD pipelines
- Automated testing
- Linting and formatting checks
- Dependency updates
- Release automation

**Bots and Apps:**
- **Dependabot**: Dependency updates
- **Stale**: Close inactive issues
- **Probot**: Custom automation
- **CodeCov**: Coverage reporting
- **Renovate**: Dependency management

**Branch Protection:**
- Require PR reviews
- Require status checks to pass
- Enforce linear history
- Restrict who can push
- Require signed commits

### Collaboration Patterns

**Working Agreements:**
- Define "done"
- Code style guide
- Review expectations
- Response time commitments
- Meeting schedules

**Communication Channels:**
- GitHub Issues: Project work
- Discussions: Open-ended topics
- Wiki: Documentation
- Slack/Discord: Real-time chat
- Email: External communication

**Documentation:**
- README: Getting started
- CONTRIBUTING: How to contribute
- CODE_OF_CONDUCT: Community standards
- SECURITY: Reporting vulnerabilities
- Wiki: Detailed guides

### Remote Team Best Practices

**Asynchronous Work:**
- Document decisions
- Written communication default
- Flexible working hours
- Clear handoffs
- Over-communicate

**Time Zones:**
- Schedule overlap hours
- Rotate meeting times
- Record meetings
- Share agendas in advance
- Async standups

**Building Culture:**
- Virtual social events
- Celebrate wins
- Share learnings
- Pair programming
- Mentorship programs

---

## GitHub Features for Teams

### Organizations
- Team permissions
- SAML/SSO integration
- Audit logging
- Security policies
- Billing management

### Team Management
- Nested teams
- Code owner assignments
- Team discussions
- Team mentions
- Permission inheritance

### Security
- Dependabot alerts
- Code scanning
- Secret scanning
- Security advisories
- Private vulnerability reporting

### Insights
- Contributor statistics
- Pulse (recent activity)
- Traffic analytics
- Dependency graph
- Network graph

---

## Anti-Patterns to Avoid

### Issue Management
- Too many labels (confusion)
- No labels (lack of organization)
- Never closing issues (perception of neglect)
- Closing without explanation (frustrating)
- No templates (inconsistent information)

### Pull Requests
- Massive PRs (hard to review)
- No description (missing context)
- Ignoring CI failures (quality issues)
- Force pushing without warning (lost review comments)
- Merging own PRs without review (bypassing process)

### Communication
- Only using @mentions (alert fatigue)
- Not linking related items (lost context)
- Vague commit messages (archaeological debugging)
- No documentation updates (stale docs)
- Private decisions (excluding team)

### Process
- Too much process (bureaucracy)
- Too little process (chaos)
- Inconsistent enforcement (unfairness)
- No automation (wasted time)
- Over-automation (losing human judgment)

---

## Tools and Resources

### GitHub CLI
- `gh`: Official GitHub CLI
- Create issues and PRs from terminal
- Review PRs locally
- Manage releases

### Browser Extensions
- Refined GitHub: Enhanced UI
- OctoLinker: Navigate dependencies
- GitHub Dark Theme: Eye comfort
- Notifications Preview: Quick scanning

### Third-Party Tools
- GitKraken: Visual Git client
- Fork: Git client
- SourceTree: Free Git GUI
- Git Tower: macOS/Windows client

### Integration Platforms
- Zapier: Connect GitHub to other services
- IFTTT: Automation recipes
- Integromat: Advanced workflows

---

## Further Reading

- [GitHub Guides](https://guides.github.com/)
- [GitHub Skills](https://skills.github.com/)
- [GitHub Blog](https://github.blog/)
- [GitHub Changelog](https://github.blog/changelog/)
- [GitHub Community Forum](https://github.community/)
