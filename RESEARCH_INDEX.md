# Research: Unsupported mdformat-mkdocs Features

## Overview

This directory contains comprehensive research on MkDocs, Material for MkDocs, and PyMdown Extensions features that are currently unsupported by mdformat-mkdocs but would benefit from auto-formatting support.

## Research Documents

### 📋 [RESEARCH_SUMMARY.md](./RESEARCH_SUMMARY.md)
**Quick reference guide** - Start here for a high-level overview of the top 5 features and implementation phases.

**Best for**: Quick decision-making, prioritization discussions, and high-level planning.

### 📚 [RESEARCH_UNSUPPORTED_FEATURES.md](./RESEARCH_UNSUPPORTED_FEATURES.md)
**Comprehensive analysis** - Detailed documentation of 18+ unsupported features with:
- Feature descriptions and syntax examples
- Why each feature matters for auto-formatting
- Specific formatting opportunities
- Implementation complexity assessments
- Testing strategies
- Phase-based implementation recommendations

**Best for**: Implementation planning, technical design, and detailed feature analysis.

### 💡 [RESEARCH_EXAMPLES.md](./RESEARCH_EXAMPLES.md)
**Practical examples** - Real-world markdown examples demonstrating each unsupported feature.

**Best for**: Understanding syntax, testing implementations, and creating test fixtures.

## Key Findings

### Top Priority Features (High Impact, Actionable)

1. **PyMdown Keys** - Keyboard shortcut notation (`++ctrl+alt+del++`)
2. **Critic Markup** - Change tracking (`{--deleted--}{++added++}`)
3. **Material Annotations** - Inline tooltips (Material v8.0+)
4. **Task Lists Enhanced** - Better checkbox formatting
5. **SmartSymbols** - Typography preservation (`(c)` → `©`)

### Implementation Approach

**Phase 1**: Low-hanging fruit (Task Lists, SmartSymbols, Highlight/Caret/Tilde)
**Phase 2**: High-value features (Keys, Critic Markup, InlineHilite)
**Phase 3**: Complex features (Annotations, MagicLink, Emoji)
**Phase 4**: Advanced/optional (Grids, Mermaid formatting, ProgressBar)

## Current Support

mdformat-mkdocs v5.1.3 currently supports:
- Material Admonitions, Content Tabs, Definition Lists
- mkdocstrings Anchors and Cross-References
- Python Markdown Abbreviations, Attribute Lists, Admonitions
- PyMdown Snippets, Captions, Arithmatex (Math/LaTeX)

## Next Steps

1. **Community Feedback**: Share research with users to validate priorities
2. **Proof of Concept**: Implement Phase 1 features (Task Lists, SmartSymbols)
3. **Iterative Development**: Add features incrementally with full test coverage
4. **Documentation**: Update README and examples for each new feature
5. **Maintenance**: Monitor user feedback and adjust priorities

## Contributing

If you're interested in implementing any of these features:

1. Review the [RESEARCH_UNSUPPORTED_FEATURES.md](./RESEARCH_UNSUPPORTED_FEATURES.md) for detailed analysis
2. Check [RESEARCH_EXAMPLES.md](./RESEARCH_EXAMPLES.md) for syntax examples
3. Follow the plugin architecture pattern in `mdformat_mkdocs/mdit_plugins/`
4. Add test fixtures in `tests/format/fixtures/` and `tests/render/fixtures/`
5. See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup

## Research Metadata

- **Date**: 2026-01-24
- **Version**: Research against mdformat-mkdocs v5.1.3
- **Scope**: MkDocs, Material for MkDocs, PyMdown Extensions
- **Features Analyzed**: 18 major features + several minor variations
- **Total Documentation**: ~600 lines across 3 documents

## Questions or Feedback?

Open an issue on GitHub to discuss:
- Feature prioritization
- Implementation approaches
- Use cases and requirements
- Testing strategies

---

**Research conducted by**: GitHub Copilot Workspace Agent  
**Repository**: [KyleKing/mdformat-mkdocs](https://github.com/KyleKing/mdformat-mkdocs)
