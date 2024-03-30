
Dashed list
.
- item 1
    - item 2
.
- item 1
    - item 2
.

Asterisk list
.
* item 1
    * item 2
.
- item 1
    - item 2
.

Numbered list
.
1. item 1
    1. item 2
    2. item 2
        1. item 3
        2. item 3
.
1. item 1
    1. item 2
    1. item 2
        1. item 3
        1. item 3
.

Combination list
.
- item 1
    * item 2
        1. item 3
.
- item 1
    - item 2
        1. item 3
.

Corrected Indentation from 3x
.
- item 1
   - item 2
      - item 3
         - item 4
.
- item 1
    - item 2
        - item 3
            - item 4
.

Corrected Indentation from 5x
.
- item 1
     - item 2
          - item 3
               - item 4
.
- item 1
    - item 2
        - item 3
            - item 4
.

Handle Jagged Indents 2x
.
- item 1
  - item 2
    - item 3
      - item 4
        - item 5
    - item 6
    - item 7
- item 8
.
- item 1
    - item 2
        - item 3
            - item 4
                - item 5
        - item 6
        - item 7
- item 8
.

Handle Jagged Indents 5x
.
- item 1
     - item 2
          - item 3
               - item 4
                    - item 5
          - item 6
          - item 7
- item 8
.
- item 1
    - item 2
        - item 3
            - item 4
                - item 5
        - item 6
        - item 7
- item 8
.

Handle Mixed Indents
.
- item 1
   - item 2
       - item 3
            - item 4
            - item 5
          - item 6
  - item 7
- item 8
.
- item 1
    - item 2
        - item 3
            - item 4
            - item 5
            - item 6
    - item 7
- item 8
.

List with (what should be converted to a) code block
.
- item 1
    
    code block
.
- item 1

    code block
.

List with explicit code block (that should keep indentation)
.
- item 1
        
    ```txt
    code block
    ```
.
- item 1

    ```txt
    code block
    ```
.


Hanging List (https://github.com/executablebooks/mdformat/issues/371 and https://github.com/KyleKing/mdformat-mkdocs/issues/4)
.
1. Here indent width is
   three.

      2. Here indent width is
       three.

123. Here indent width is
     five. It needs to be so, because

     Otherwise this next paragraph doesn't belong in the same list item.
.
1. Here indent width is
   three.

    1. Here indent width is
       three.

1. Here indent width is
   five. It needs to be so, because

    Otherwise this next paragraph doesn't belong in the same list item.
.


Code block in semantic indent (https://github.com/KyleKing/mdformat-mkdocs/issues/6)
.
1. Item 1
   with a semantic line feed

   ```bash
   echo "I get moved around by prettier/mdformat, originally I am 3 spaces deep"
   ```

1. Item 2
1. Item 3
.
1. Item 1
   with a semantic line feed

    ```bash
    echo "I get moved around by prettier/mdformat, originally I am 3 spaces deep"
    ```

1. Item 2

1. Item 3
.


Nested semantic lines (https://github.com/KyleKing/mdformat-mkdocs/issues/7)
.
1. Line
   semantic line 1 (3 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
.
1. Line
   semantic line 1 (3 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
.


Bulleted semantic lines (https://github.com/KyleKing/mdformat-mkdocs/issues/7)
.
- Line
  semantic line 1 (2 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
.
- Line
  semantic line 1 (2 spaces deep)
    - Bullet (4 spaces deep)
      semantic line 2 (6 spaces deep)
.


Nested semantic lines (https://github.com/KyleKing/mdformat-mkdocs/issues/7)
.
- Line
    semantic line 1 (2 spaces deep)
    1. Bullet (4 spaces deep)
        semantic line 2 (7 spaces deep)
.
- Line
  semantic line 1 (2 spaces deep)
    1. Bullet (4 spaces deep)
       semantic line 2 (7 spaces deep)
.


Table
.
| Label          |   Rating | Comment              |
|:---------------|---------:|:---------------------|
| Name           |         2| <!-- Comment -->     |
.
| Label          |   Rating | Comment              |
|:---------------|---------:|:---------------------|
| Name           |         2| <!-- Comment -->     |
.

Floating Link
.
> Based on [External Link]
 
[external link]: https://github.com/czuli/github-markdown-example/tree/7326f19c94be992319394e5bfeaa07b30f858e46
.
> Based on [External Link]

[external link]: https://github.com/czuli/github-markdown-example/tree/7326f19c94be992319394e5bfeaa07b30f858e46
.

Headings
.
# [h1] The largest heading

## [h2] heading

### [h3] heading

#### [h4] heading

##### [h5] heading

###### [h6] The smallest heading
.
# \[h1\] The largest heading

## \[h2\] heading

### \[h3\] heading

#### \[h4\] heading

##### \[h5\] heading

###### \[h6\] The smallest heading
.

Task List / Check List (WARN: escaping is prevented by mdformat-gfm. Tested by py#-hook)
.
- [x] #739
  - [ ] Add delight to the experience when all tasks are complete :tada:
.
- \[x\] #739
    - \[ \] Add delight to the experience when all tasks are complete :tada:
.

Footnotes (WARN: escaping is prevented by mdformat-gfm. Tested by py#-hook)
.
Here is a simple footnote[^1].

You can also use words, to fit your writing style more closely[^note].

  [^1]: My reference.
  [^note]: Named footnotes will still render with numbers instead of the text but allow easier identification and linking.\
    This footnote also has been made with a different syntax using 4 spaces for new lines.
.
Here is a simple footnote\[^1\].

You can also use words, to fit your writing style more closely\[^note\].

\[^1\]: My reference.
\[^note\]: Named footnotes will still render with numbers instead of the text but allow easier identification and linking.\
This footnote also has been made with a different syntax using 4 spaces for new lines.
.
