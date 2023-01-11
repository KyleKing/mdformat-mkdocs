
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
.
> Based on [External Link]
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
# [h1] The largest heading

## [h2] heading

### [h3] heading

#### [h4] heading

##### [h5] heading

###### [h6] The smallest heading
.

Check List
.
- [x] #739
- [ ] Add delight to the experience when all tasks are complete :tada:
.
- [x] #739
- [ ] Add delight to the experience when all tasks are complete :tada:
.

Footnotes
.
Here is a simple footnote[^1].

You can also use words, to fit your writing style more closely[^note].

  [^1]: My reference.
  [^note]: Named footnotes will still render with numbers instead of the text but allow easier identification and linking.\
    This footnote also has been made with a different syntax using 4 spaces for new lines.
.
Here is a simple footnote[^1].

You can also use words, to fit your writing style more closely[^note].

  [^1]: My reference.
  [^note]: Named footnotes will still render with numbers instead of the text but allow easier identification and linking.\
    This footnote also has been made with a different syntax using 4 spaces for new lines.
.
