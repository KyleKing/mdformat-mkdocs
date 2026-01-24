# Research: Unsupported mdformat-mkdocs Features

## Executive Summary

This document identifies MkDocs, Material for MkDocs, and PyMdown Extensions features that are currently unsupported by mdformat-mkdocs but would benefit from auto-formatting support.

**Date**: 2026-01-24  
**Version**: Research conducted against mdformat-mkdocs v5.1.3

## Quick Reference Table

| Feature | Priority | Use Case | Syntax Example | Complexity |
|---------|----------|----------|----------------|------------|
| PyMdown Keys | High | Keyboard shortcuts | `++ctrl+alt+del++` | Medium |
| Critic Markup | High | Change tracking | `{--deleted--}{++added++}` | Medium-High |
| Task Lists (Enhanced) | High | Checklists/TODOs | `- [x] Done` | Low-Medium |
| MagicLink | High | Auto-linking | `@username`, `#123` | Medium |
| SmartSymbols | High | Typography | `(c)` → `©` | Low-Medium |
| Material Annotations | High | Inline tooltips | `text (1)` + definition | High |
| Material Grids | High | Card layouts | `<div class="grid cards">` | High |
| Highlight | Medium | Text marking | `==marked==` | Low-Medium |
| Caret & Tilde | Medium | Super/subscript | `H^2^O`, `CH~3~` | Low-Medium |
| Details | Medium | Collapsible content | `??? note` | Low |
| Emoji | Medium | Icons/emoji | `:smile:`, `:material-icon:` | Low |
| InlineHilite | Medium | Inline code syntax | `:::python code` | Low-Medium |
| Blocks | Low | Generic containers | `/// type \| attr` | High |
| ProgressBar | Low | Visual progress | `[=50% "50%"]` | Low-Medium |
| Superfences (Custom) | Low | Diagram formatting | mermaid, plantuml | Medium-High |
| Tabbed | Low | Legacy tabs | `=== "Tab"` (likely supported) | Low |
| Mermaid Formatting | Low | Diagram code | Format within fences | High |
| Data Tables | Low | Enhanced tables | Tables with attributes | Low |

## Currently Supported Features

For reference, mdformat-mkdocs currently supports:

- Material for MkDocs Admonitions (`!!!`, `???`, `???+`)
- Material for MkDocs Content Tabs (`=== "Tab Name"`)
- Material for MkDocs Definition Lists
- mkdocstrings Anchors (autorefs)
- mkdocstrings Cross-References
- Python Markdown Abbreviations (`*[abbr]: definition`)
- Python Markdown Attribute Lists (`{: #id .class }`)
- Python Markdown Admonitions (ReStructuredText-style)
- PyMdown Extensions Snippets (`--8<-- "path/to/file.py"`)
- PyMdown Extensions Captions (`/// caption`)
- PyMdown Extensions Arithmatex (Math/LaTeX: `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, AMS environments)

## Unsupported Features Analysis

### High Priority: Direct Formatting Benefits

#### 1. PyMdown Extensions: Keys

**Description**: Renders keyboard key combinations with special styling.

**Syntax**:
```markdown
++ctrl+alt+delete++
++cmd+shift+p++
```

**Why it matters**:
- Widely used in technical documentation for keyboard shortcuts
- Clear visual syntax that could benefit from consistent formatting
- Could normalize key separators (`+` vs `++`)

**Formatting opportunities**:
- Normalize spacing around key combinations
- Consistent capitalization (e.g., `Ctrl` vs `ctrl`)
- Validate key names against known keys
- Format multi-key sequences consistently

**Implementation complexity**: Medium (requires new parser plugin and renderer)

---

#### 2. PyMdown Extensions: Critic Markup

**Description**: Track changes and editorial comments in markdown.

**Syntax**:
```markdown
{--deleted text--}
{++added text++}
{~~old~>new~~}
{==highlight==}
{>>comment<<}
```

**Why it matters**:
- Used for collaborative editing and reviewing
- Tracks document history directly in markdown
- Multiple syntactic elements that need consistent formatting

**Formatting opportunities**:
- Normalize spacing inside markers
- Ensure proper nesting of critic markup
- Validate matching opening/closing delimiters
- Format multi-line critic blocks consistently

**Implementation complexity**: Medium-High (complex grammar with multiple modes)

---

#### 3. PyMdown Extensions: Task Lists (Enhanced)

**Description**: Extended task list syntax beyond basic GFM.

**Syntax**:
```markdown
- [x] Completed task
- [ ] Incomplete task
- [X] Alternative completed (uppercase X)
```

**Why it matters**:
- Common in documentation TODOs and checklists
- Already has basic support via GFM, but PyMdown adds enhancements
- Formatting can normalize checkbox markers

**Formatting opportunities**:
- Normalize checkbox markers (`[x]` vs `[X]`)
- Consistent spacing after checkbox
- Handle indentation of multi-line task items

**Implementation complexity**: Low-Medium (extends existing GFM support)

---

#### 4. PyMdown Extensions: MagicLink

**Description**: Auto-converts URLs and email addresses to links, with special handling for repository references.

**Syntax**:
```markdown
https://example.com (becomes a link)
user@example.com (becomes a mailto link)
@username (GitHub mention)
#123 (issue reference)
```

**Why it matters**:
- Commonly used for automatic link generation
- Multiple link types that could benefit from normalization
- Repository references need consistent formatting

**Formatting opportunities**:
- Normalize URL schemes (http vs https)
- Format email addresses consistently
- Ensure proper spacing around auto-generated links
- Validate and format repository references

**Implementation complexity**: Medium (requires URL parsing and validation)

---

#### 5. PyMdown Extensions: SmartSymbols

**Description**: Converts ASCII symbols to their typographic equivalents.

**Syntax**:
```markdown
(c) --> ©
(tm) --> ™
(r) --> ®
-- --> –
--- --> —
--> --> →
<-- --> ←
```

**Why it matters**:
- Improves typography automatically
- Needs preservation during formatting
- Should not be reversed/corrupted

**Formatting opportunities**:
- Preserve converted symbols
- Optionally normalize to ASCII or Unicode
- Consistent handling of symbol conversions
- Ensure symbols are not escaped incorrectly

**Implementation complexity**: Low-Medium (mostly preservation logic)

---

#### 6. Material for MkDocs: Annotations

**Description**: Inline annotations that appear as superscript numbers with hover tooltips.

**Syntax**:
```markdown
Lorem ipsum dolor sit amet, (1) consectetur adipiscing elit.
{ .annotate }

1. This is an annotation
```

**Why it matters**:
- New feature in Material for MkDocs (v8.0+)
- Becoming popular for inline documentation
- Complex multi-part syntax that needs coordination

**Formatting opportunities**:
- Align annotation numbers with definitions
- Format annotation blocks consistently
- Ensure proper spacing and indentation
- Validate annotation number sequences

**Implementation complexity**: High (requires coordinated formatting of multiple elements)

---

#### 7. Material for MkDocs: Grids

**Description**: Card grids and content layouts.

**Syntax**:
```markdown
<div class="grid cards" markdown>

- :material-clock-fast: **Set up in 5 minutes**

    ---

    Install with pip and get started in minutes

- :fontawesome-brands-markdown: **It's just Markdown**

    ---

    Focus on content, Material handles the layout

</div>
```

**Why it matters**:
- Increasingly popular for landing pages and feature showcases
- Mix of HTML and markdown that needs careful handling
- Could benefit from consistent indentation and spacing

**Formatting opportunities**:
- Consistent HTML tag formatting
- Normalize spacing between grid items
- Format markdown within grid cards
- Ensure proper attribute formatting

**Implementation complexity**: High (requires HTML and markdown mixed content handling)

---

### Medium Priority: Consistency Improvements

#### 8. PyMdown Extensions: Highlight

**Description**: Highlights text with configurable markers.

**Syntax**:
```markdown
==marked text==
^^inserted text^^
```

**Why it matters**:
- Used for emphasis and highlighting
- Simple syntax but needs preservation

**Formatting opportunities**:
- Preserve highlight markers during wrapping
- Consistent spacing within markers
- Handle nested or adjacent highlights

**Implementation complexity**: Low-Medium

---

#### 9. PyMdown Extensions: Caret & Tilde

**Description**: Superscript and subscript text.

**Syntax**:
```markdown
H^2^O (superscript)
CH~3~CH~2~OH (subscript)
```

**Why it matters**:
- Essential for scientific and mathematical notation
- Needs careful preservation to avoid data loss

**Formatting opportunities**:
- Preserve superscript/subscript markers
- Validate nesting and pairing
- Handle spacing around markers

**Implementation complexity**: Low-Medium

---

#### 10. PyMdown Extensions: Details

**Description**: Native HTML `<details>` and `<summary>` elements.

**Syntax**:
```markdown
???+ note "Custom Title"
    This is a collapsible note
```

Note: This might already be partially supported via Material Admonitions, but Details is the PyMdown base extension.

**Formatting opportunities**:
- Consistent spacing and indentation
- Normalize open/closed state markers
- Format content within details blocks

**Implementation complexity**: Low (likely already covered by admonitions)

---

#### 11. PyMdown Extensions: Emoji

**Description**: Emoji support with custom indexes.

**Syntax**:
```markdown
:smile:
:material-account-circle:
:fontawesome-brands-github:
```

**Why it matters**:
- Commonly used in documentation for visual cues
- Icon syntax varies (material, fontawesome, etc.)

**Formatting opportunities**:
- Validate emoji shortcodes
- Normalize icon syntax format
- Consistent spacing around emoji

**Implementation complexity**: Low (validation and preservation)

---

#### 12. PyMdown Extensions: InlineHilite

**Description**: Inline code highlighting with syntax hints.

**Syntax**:
```markdown
`:::python def function():` 
```

**Why it matters**:
- Adds language context to inline code
- Should be preserved during formatting

**Formatting opportunities**:
- Preserve language hints
- Validate language identifiers
- Consistent spacing within inline code

**Implementation complexity**: Low-Medium

---

### Lower Priority: Advanced/Specialized Features

#### 13. PyMdown Extensions: Blocks & Block Extensions

**Description**: Generic container blocks with various plugins.

**Syntax**:
```markdown
/// tab | Tab 1
    content
///

/// tab | Tab 2
    content
///
```

**Why it matters**:
- Extensible block system for custom plugins
- Generic syntax that could encompass many use cases

**Formatting opportunities**:
- Consistent block delimiter formatting
- Normalize indentation within blocks
- Format block attributes

**Implementation complexity**: High (generic extensible system)

---

#### 14. PyMdown Extensions: ProgressBar

**Description**: Progress bars in documentation.

**Syntax**:
```markdown
[=0% "0%"]
[=50% "50%"]
[=100% "100%"]
```

**Why it matters**:
- Visual indicators for completion
- Structured format that could benefit from normalization

**Formatting opportunities**:
- Normalize percentage formats
- Validate percentage values (0-100)
- Consistent spacing and quote usage

**Implementation complexity**: Low-Medium

---

#### 15. PyMdown Extensions: Superfences (Custom Fences)

**Description**: Enhanced code fences with custom formatters and options.

**Syntax**:
````markdown
```mermaid
graph LR
    A --> B
```
````

**Why it matters**:
- Widely used for diagrams (mermaid, plantuml)
- Code blocks with special processing needs
- Already has some support via mdformat, but could be enhanced

**Formatting opportunities**:
- Format diagram code within fences
- Normalize fence delimiters (triple vs longer)
- Handle custom fence options and attributes

**Implementation complexity**: Medium-High (requires diagram parsers for proper formatting)

---

#### 16. PyMdown Extensions: Tabbed

**Description**: Alternative tabbed content syntax (predecessor to Material Content Tabs).

**Syntax**:
```markdown
=== "Tab 1"
    Content 1

=== "Tab 2"
    Content 2
```

Note: This is likely already supported via Material Content Tabs plugin.

**Formatting opportunities**:
- Consistent spacing and indentation
- Normalize tab marker format

**Implementation complexity**: Low (likely already covered)

---

#### 17. Material for MkDocs: Diagrams (Mermaid)

**Description**: Native mermaid diagram support.

**Syntax**:
````markdown
```mermaid
graph LR
    A --> B
```
````

**Why it matters**:
- Popular for technical diagrams
- Diagram code should be formatted according to mermaid syntax rules

**Formatting opportunities**:
- Format mermaid code with proper indentation
- Validate mermaid syntax
- Normalize diagram structure

**Implementation complexity**: High (requires mermaid parser)

---

#### 18. Material for MkDocs: Data Tables (Sortable)

**Description**: Enhanced markdown tables with sorting and filtering.

**Syntax**:
```markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Value 1  | Value 2  |
{ data-search data-sort }
```

**Why it matters**:
- Tables are core markdown, but Material adds enhancements
- Attribute lists for tables need preservation
- mdformat-gfm already handles basic tables

**Formatting opportunities**:
- Preserve table attributes
- Format table attributes consistently
- Align table columns (already done by mdformat-gfm)

**Implementation complexity**: Low (extends existing table support)

---

## Features Unlikely to Need Formatting

Some features are primarily runtime/rendering features that don't have significant formatting implications:

1. **Material for MkDocs: Search** - No markdown syntax
2. **Material for MkDocs: Social Cards** - Configuration-based, no markdown syntax
3. **Material for MkDocs: Blog plugin** - File structure, not inline syntax
4. **PyMdown Extensions: PathConverter** - Path transformation, no syntax
5. **PyMdown Extensions: Sane Lists** - Behavior change, not syntax
6. **PyMdown Extensions: StripHTML** - Processing directive, no syntax
7. **PyMdown Extensions: Mark** - Simple marker `==text==` (covered by Highlight)

## Implementation Recommendations

### Phase 1: High-Impact, Lower-Complexity Features
1. **Task Lists** (extends existing GFM)
2. **SmartSymbols** (preservation focus)
3. **Highlight, Caret, Tilde** (simple markers)

### Phase 2: Specialized but Valuable Features
4. **Keys** (keyboard shortcuts)
5. **Critic Markup** (collaborative editing)
6. **InlineHilite** (inline code with syntax)

### Phase 3: Complex but Comprehensive Features
7. **Annotations** (Material for MkDocs v8.0+)
8. **MagicLink** (auto-link conversion)
9. **Emoji** (with validation)

### Phase 4: Advanced/Optional Features
10. **Blocks** (generic extensibility)
11. **Grids** (layout system)
12. **Mermaid formatting** (diagram code)
13. **ProgressBar** (visual indicators)

## Testing Strategy

For each new feature:
1. Create test fixtures in `tests/format/fixtures/` with various edge cases
2. Add rendering tests in `tests/render/fixtures/` to verify HTML output
3. Test integration with existing features (e.g., keys inside admonitions)
4. Verify idempotency (format twice should produce same result)
5. Test with `--wrap` and other mdformat options

## Reference Links

### MkDocs Documentation
- Material for MkDocs Reference: https://squidfunk.github.io/mkdocs-material/reference/
- PyMdown Extensions: https://facelessuser.github.io/pymdown-extensions/
- Python Markdown: https://python-markdown.github.io/extensions/

### Plugin Architecture References
- markdown-it-py: https://markdown-it-py.readthedocs.io/
- mdformat: https://mdformat.readthedocs.io/
- mdit-py-plugins: https://github.com/executablebooks/mdit-py-plugins

## Conclusion

There are approximately 15+ features from the MkDocs ecosystem that would benefit from mdformat-mkdocs support. The highest priority items are:

1. **PyMdown Keys** - Very common in technical docs (keyboard shortcuts)
2. **PyMdown Critic Markup** - Important for collaborative editing and change tracking
3. **Material Annotations** - Growing in popularity (v8.0+ feature)
4. **PyMdown Task Lists** - Already partially supported via GFM, needs enhancement
5. **PyMdown SmartSymbols** - Needs careful preservation to avoid data loss

Each feature should be evaluated based on:
- **User demand** (how often it's used in real projects)
- **Formatting value** (how much it improves consistency and readability)
- **Implementation complexity** (parser difficulty and development time)
- **Maintenance burden** (ongoing support costs and edge cases)

The plugin's modular architecture makes it straightforward to add new features incrementally without disrupting existing functionality. Each new feature would follow the pattern:

1. Create a new file in `mdformat_mkdocs/mdit_plugins/` (e.g., `_pymd_keys.py`)
2. Implement the markdown-it parser plugin
3. Add a renderer in `mdformat_mkdocs/plugin.py`
4. Add test fixtures in `tests/format/fixtures/` and `tests/render/fixtures/`
5. Update documentation in `README.md`

## Next Steps

1. **Community feedback**: Share this research with users to gauge interest in specific features
2. **Prioritization**: Based on user feedback, prioritize features for implementation
3. **Prototype**: Start with Phase 1 features (Task Lists, SmartSymbols) as proof of concept
4. **Iterate**: Add features incrementally with full test coverage
5. **Document**: Update README and add examples for each new feature
