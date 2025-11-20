# Logging Best Practices

A collection of insights and best practices for logging in software applications.

## Overview

Effective logging is crucial for debugging, monitoring, and maintaining software systems. This document summarizes key learnings from various resources about logging best practices.

---

## Log Levels: Rule of Thumb

**Source:** [Stack Overflow - Logging levels logback rule of thumb](https://stackoverflow.com/questions/7839565/logging-levels-logback-rule-of-thumb-to-assign-log-levels/8021604#8021604)

Practical guidelines for assigning logging levels:

### ERROR
Log failures requiring human intervention. Apply the "2AM rule"—if an on-call person should be woken up, use ERROR. Examples: system failures, unhandled exceptions, critical dependency issues.

### WARN
Document unexpected events that don't require immediate action but need attention. As one answer states: "an unexpected technical or business event happened, customers may be affected, but probably no immediate human intervention is required."

### INFO
Record significant lifecycle and boundary events. Use for system startup/shutdown, user sessions, and important business transactions. Keep volume reasonable to remain useful in production.

### DEBUG
Log detailed flow information helpful during development and QA. Include method entry/exit points and decision outcomes. This supports troubleshooting without production overhead.

### TRACE
Reserve for extremely detailed, high-volume data you'd rarely enable. Examples include full object dumps or per-iteration loop logging—typically development-only.

### Key Principle
The core distinction: logs should serve **production support and forensic analysis**. Include sufficient context (thread IDs, user info, specific details) to make messages actionable rather than merely informational.

---

## Python Logging: Professional Practices

**Source:** [How to Log in Python Like a Pro](https://guicommits.com/how-to-log-in-python-like-a-pro/)

*Note: This article was not accessible during summarization. Key topics typically covered include:*
- Proper logger configuration and setup
- Structured logging approaches
- Integration with application frameworks
- Performance considerations
- Common pitfalls to avoid

---

## What to Log and Avoiding Alert Fatigue

**Source:** [What should you log in an application](https://cloudncode.blog/2016/12/30/what-should-you-log-in-an-application-and-how-to-avoid-having-24x7-support-looking-at-them/)

*Note: This article was not accessible during summarization. Key topics typically covered include:*
- Identifying critical events worth logging
- Balancing information needs with log volume
- Preventing alert fatigue for support teams
- Log retention and rotation strategies
- Distinguishing between application and audit logs

---

## Logging Levels: The Wrong Abstraction

**Source:** [Logging levels: the wrong abstraction | IG Labs](https://labs.ig.com/logging-level-wrong-abstraction)

*Note: This article was not accessible during summarization. This article typically discusses:*
- Why traditional log levels might be the wrong mental model
- Alternative approaches to categorizing logs
- Context-based logging strategies
- Moving beyond severity-based logging

---

## General Best Practices Summary

Based on the accessible resources, here are key takeaways:

1. **Purpose-Driven Logging**: Always consider who will read the logs and for what purpose
2. **Actionable Information**: Include enough context to take action without guesswork
3. **Appropriate Levels**: Use the right log level based on required response, not perceived importance
4. **Production Readiness**: Design logging with production support in mind from the start
5. **Performance Awareness**: Balance information needs with application performance
6. **Consistent Context**: Include identifiers (user IDs, transaction IDs, thread IDs) consistently

## Related Resources

- Structured logging libraries for Python (structlog, python-json-logger)
- Log aggregation and analysis tools (ELK stack, Splunk, Datadog)
- Application monitoring and error tracking (Sentry, Rollbar, NewRelic)
