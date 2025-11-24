# Testing Best Practices

A collection of testing strategies and best practices for software development.

## Overview

This document compiles insights on effective testing strategies, including test design, mocking approaches, and practical testing philosophies.

---

## Python Testing Style Guide

**Source:** [My Python Testing Style Guide](https://blog.thea.codes/my-python-testing-style-guide/)

Stargirl Flowers' testing philosophy emphasizes pragmatism over dogmatism, focusing on behavior rather than implementation details.

### Key Principles

#### Test Organization & Naming
Follow pytest conventions with files named `test_*.py`. Match test names to their targets, adding descriptive suffixes for different scenarios (e.g., `test_refresh_failure`).

#### Assert Outcomes, Not Steps
Tests should verify the final state rather than method invocations. As the guide notes, "Your assertions should test that the state of the world matches the outcome you expected."

#### Prefer Real Objects
Use actual collaborators whenever feasible. This catches bugs and encourages cleaner code design. Mock objects should be reserved for situations where real implementations aren't practical.

#### Strict Mock Specifications
When mocking is necessary, always use `mock.create_autospec()` or `mock.patch(autospec=True)`. This ensures your tests break when interfaces change, preventing hidden bugs in production code.

#### Consider Alternatives to Mocks
Stubs (objects with canned responses) and fakes (simplified working implementations) often provide better test clarity than complex mocks.

#### Naming Convention
Name mocks identically to real collaborators—avoid prefixes like `mock_` or `fake_`. This reinforces treating them as genuine substitutes.

#### Fixture Usage
Use fixtures sparingly, preferring factory helpers for setup. Reserve fixtures for complex setup/teardown logic or dependency injection scenarios.

---

## Stubbing vs. Mocking

**Source:** [Outside-In Testing Concepts - Stubbing and Mocking](https://outsidein.dev/testing-concepts.html#stubbing-and-mocking)

*Note: This article was not accessible during summarization. Key concepts typically covered include:*

### Stubs
- Return predetermined responses to method calls
- Used to provide indirect inputs to the system under test
- Don't verify how they were called
- Simpler and more stable than mocks

### Mocks
- Verify that specific methods were called with specific parameters
- Used to verify indirect outputs from the system under test
- More brittle but useful for testing side effects
- Require careful maintenance as code evolves

### When to Use Each
- **Use stubs** when you need to control inputs to your test subject
- **Use mocks** when you need to verify that your code called something correctly
- **Prefer real objects** when practical for more reliable tests

---

## Testing the Diff

**Source:** [Testing the Diff - Vinta Blog](https://www.vinta.com.br/blog/2021/testing-the-diff/)

*Note: This article was not accessible during summarization. This concept typically covers:*

### Core Concept
Instead of running the entire test suite on every change, focus testing efforts on:
- Code that was modified
- Code that depends on the modified code
- Integration points affected by changes

### Benefits
- Faster feedback loops during development
- More efficient use of CI/CD resources
- Encourages smaller, focused commits
- Reduces testing fatigue

### Implementation Strategies
- Use coverage tools to identify affected tests
- Implement test impact analysis
- Tag tests by feature area or component
- Use git diff to identify changed files and related tests

### Considerations
- Still run full test suite before merging/releasing
- Ensure dependency graphs are accurate
- Balance speed with comprehensive coverage
- Consider integration test implications

---

## General Testing Best Practices Summary

Based on the accessible resources and industry standards:

### Test Design
1. **Focus on Behavior**: Test what the code does, not how it does it
2. **One Assertion Concept per Test**: Tests should verify a single logical outcome
3. **Descriptive Names**: Test names should explain what's being tested and expected outcome
4. **Arrange-Act-Assert Pattern**: Structure tests clearly with setup, execution, and verification

### Mock Strategy
1. **Prefer Real Objects**: Use actual implementations when practical
2. **Strict Specifications**: Always use autospec for mocks
3. **Minimize Mocking**: Too many mocks indicate poor design
4. **Test Behavior, Not Implementation**: Don't verify internal method calls unless they're the feature

### Test Organization
1. **Mirror Source Structure**: Test files should match source code organization
2. **Shared Fixtures**: Use factory functions for common test data
3. **Isolated Tests**: Each test should be independent and runnable in any order
4. **Clear Setup/Teardown**: Make test prerequisites explicit

### Efficiency
1. **Fast Tests**: Keep unit tests fast (< 100ms each)
2. **Parallel Execution**: Design tests to run concurrently
3. **Strategic Coverage**: Focus on critical paths and edge cases
4. **Test Pyramid**: Many unit tests, fewer integration tests, minimal E2E tests

### Maintenance
1. **Refactor Tests**: Treat test code with the same care as production code
2. **Delete Obsolete Tests**: Remove tests for removed features
3. **Update with Refactoring**: Keep tests aligned with code changes
4. **Document Complex Tests**: Explain why a test exists if non-obvious

## Related Tools & Frameworks

### Python Testing
- **pytest**: Modern, feature-rich testing framework
- **unittest**: Standard library testing framework
- **hypothesis**: Property-based testing
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution

### Mocking & Stubbing
- **unittest.mock**: Standard library mocking
- **pytest-mock**: pytest integration for mocking
- **responses**: Mock HTTP requests
- **freezegun**: Mock datetime

### Coverage & Analysis
- **coverage.py**: Code coverage measurement
- **pytest-cov**: pytest coverage plugin
- **mutation testing**: Tools like mutmut to test test quality

## Further Reading

- Test-Driven Development (TDD) principles
- Behavior-Driven Development (BDD) approaches
- Property-based testing with Hypothesis
- Integration testing strategies
- End-to-end testing best practices
