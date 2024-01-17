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

Nested Python Classes. Resolves #13: https://github.com/KyleKing/mdformat-mkdocs/issues/13
.
1. Add a serializer class

    ```python
    class RecurringEventSerializer(serializers.ModelSerializer):  # (1)!
        """Used to retrieve recurring_event info"""

        class Meta:
            model = RecurringEvent  # (2)!
    ```
.
1. Add a serializer class

    ```python
    class RecurringEventSerializer(serializers.ModelSerializer):  # (1)!
        """Used to retrieve recurring_event info"""

        class Meta:
            model = RecurringEvent  # (2)!
    ```
.


Simple admonition
.
!!! note
    *content*
.
!!! note
    *content*
.


Could contain block elements too
.
!!! note
    ### heading

    -----------

.
!!! note
    ### heading

    ______________________________________________________________________

.


Shows custom title
.
!!! note Custom title

    Some text

.
!!! note Custom title
    Some text

.


Shows no title
.
!!! note ""
    Some text

.
!!! note ""
    Some text

.


Removes extra quotes from the title
.
!!! danger "Don't try this at home"
    ...

.
!!! danger "Don't try this at home"
    ...

.


Parse additional classes to support Python markdown (https://github.com/executablebooks/mdit-py-plugins/issues/93#issuecomment-1601822723)
.
!!! a b c d inline-classes   "Note: note about "foo""
    ...

.
!!! a b c d inline-classes   "Note: note about "foo""
    ...

.


Closes block after 2 empty lines
.
!!! note
    Some text


    A code block
.
!!! note
    Some text

```
A code block
```
.


Nested blocks
.
!!! note
    !!! note
        Some text

            code block
.
!!! note
    !!! note
        Some text

        ```
        code block
        ```
.


Consecutive admonitions
.
!!! note

!!! warning
.
!!! note

!!! warning
.


Marker may be indented up to 3 chars
.
   !!! note
       content
.
!!! note
    content
.


But that's a code block
.
    !!! note
        content
.
```
!!! note
    content
```
.


Some more indent checks
.
  !!! note
   not a code block

    code block
.
!!! note

not a code block

```
code block
```
.


Type could be adjacent to marker
.
!!!note
   xxx

.
!!! note
    xxx

.


Type could be adjacent to marker and content may be shifted up to 3 chars
.
!!!note
      xxx

.
!!! note
    xxx

.


Or several spaces apart
.
!!!     note
        xxx
.
!!! note
    xxx
.


Admonitions self-close at the end of the document
.
!!! note
    xxx
.
!!! note
    xxx
.


These are not admonitions
.
- !!! note
      - a
      - b
- !!! warning
      - c
      - d
.
- !!! note
    - a
    - b
- !!! warning
    - c
    - d
.


Or in blockquotes
.
> !!! note
>     xxx
>     > yyy
>     zzz
>
.
> !!! note
>     xxx
>
>     > yyy
>     > zzz
.


Renders unknown admonition type
.
!!! unknown title
    content
.
!!! unknown title
    content
.


Does not render
.
!!!
    content
.
!!!
content
.


MKDocs Closed Collapsible Sections
.
??? note
     content
.
??? note
    content
.


MKDocs Open Collapsible Sections
.
???+ note
     content
.
???+ note
    content
.


Support Content Tabs (https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#grouping-code-blocks). Resolves #17: https://github.com/KyleKing/mdformat-admon/issues/17
.
Ultralytics commands use the following syntax:

!!! Example

    === "CLI"

        ```bash
        yolo TASK MODE ARGS
        ```

    === "Python"

        ```python
        from ultralytics import YOLO

        # Load a YOLOv8 model from a pre-trained weights file
        model = YOLO('yolov8n.pt')

        # Run MODE mode using the custom arguments ARGS (guess TASK)
        model.MODE(ARGS)
        ```
.
Ultralytics commands use the following syntax:

!!! Example
    === "CLI"
        ```bash
        yolo TASK MODE ARGS
        ```

    === "Python"
        ```python
        from ultralytics import YOLO

        # Load a YOLOv8 model from a pre-trained weights file
        model = YOLO('yolov8n.pt')

        # Run MODE mode using the custom arguments ARGS (guess TASK)
        model.MODE(ARGS)
        ```
.


(1/2) Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/0e7221fb62191e18e5ec4f7a9fe6d8927a4446c2/docs/zh/datasets/index.md#L105-L127)
.
### 优化和压缩数据集的示例代码

!!! Example "优化和压缩数据集"

    === "Python"

    ```python
    from pathlib import Path
    from ultralytics.data.utils import compress_one_image
    from ultralytics.utils.downloads import zip_directory

    # 定义数据集目录
    path = Path('path/to/dataset')

    # 优化数据集中的图像（可选）
    for f in path.rglob('*.jpg'):
        compress_one_image(f)

    # 将数据集压缩成 'path/to/dataset.zip'
    zip_directory(path)
    ```

通过遵循这些步骤，您可以贡献一个与 Ultralytics 现有结构良好融合的新数据集。
.
### 优化和压缩数据集的示例代码

!!! Example "优化和压缩数据集"
    === "Python"

    ```python
    from pathlib import Path
    from ultralytics.data.utils import compress_one_image
    from ultralytics.utils.downloads import zip_directory

    # 定义数据集目录
    path = Path('path/to/dataset')

    # 优化数据集中的图像（可选）
    for f in path.rglob('*.jpg'):
        compress_one_image(f)

    # 将数据集压缩成 'path/to/dataset.zip'
    zip_directory(path)
    ```

通过遵循这些步骤，您可以贡献一个与 Ultralytics 现有结构良好融合的新数据集。
.


(2/2) FYI: the code block must be manually indented for the parser to identify the fenced block
.
### 优化和压缩数据集的示例代码

!!! Example "优化和压缩数据集"

    === "Python"

        ```python
        from pathlib import Path
        from ultralytics.data.utils import compress_one_image
        from ultralytics.utils.downloads import zip_directory

        # 定义数据集目录
        path = Path('path/to/dataset')

        # 优化数据集中的图像（可选）
        for f in path.rglob('*.jpg'):
            compress_one_image(f)

        # 将数据集压缩成 'path/to/dataset.zip'
        zip_directory(path)
        ```

通过遵循这些步骤，您可以贡献一个与 Ultralytics 现有结构良好融合的新数据集。
.
### 优化和压缩数据集的示例代码

!!! Example "优化和压缩数据集"
    === "Python"
        ```python
        from pathlib import Path
        from ultralytics.data.utils import compress_one_image
        from ultralytics.utils.downloads import zip_directory

        # 定义数据集目录
        path = Path('path/to/dataset')

        # 优化数据集中的图像（可选）
        for f in path.rglob('*.jpg'):
            compress_one_image(f)

        # 将数据集压缩成 'path/to/dataset.zip'
        zip_directory(path)
        ```

通过遵循这些步骤，您可以贡献一个与 Ultralytics 现有结构良好融合的新数据集。
.


Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/datasets/classify/caltech101.md#L60-L79)
.
## Citations and Acknowledgments

If you use the Caltech-101 dataset in your research or development work, please cite the following paper:

!!! Quote ""

    === "BibTeX"
        ```bibtex
        @article{fei2007learning,
          title={Learning generative visual models from few training examples: An incremental Bayesian approach tested on 101 object categories},
          author={Fei-Fei, Li and Fergus, Rob and Perona, Pietro},
          journal={Computer vision and Image understanding},
          volume={106},
          number={1},
          pages={59--70},
          year={2007},
          publisher={Elsevier}
        }
        ```
.
## Citations and Acknowledgments

If you use the Caltech-101 dataset in your research or development work, please cite the following paper:

!!! Quote ""
    === "BibTeX"
        ```bibtex
        @article{fei2007learning,
          title={Learning generative visual models from few training examples: An incremental Bayesian approach tested on 101 object categories},
          author={Fei-Fei, Li and Fergus, Rob and Perona, Pietro},
          journal={Computer vision and Image understanding},
          volume={106},
          number={1},
          pages={59--70},
          year={2007},
          publisher={Elsevier}
        }
        ```
.


Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/guides/isolating-segmentation-objects.md#L15)
.
## Recipe Walk Through

1. Begin with the necessary imports

    ```py
    from pathlib import Path
    
    import cv2 as cv
    import numpy as np
    from ultralytics import YOLO
    ```
    
    ???+ tip "Ultralytics Install"

        See the Ultralytics [Quickstart](../quickstart.md/#install-ultralytics) Installation section for a quick walkthrough on installing the required libraries.

    ***

2. Load a model and run `predict()` method on a source.

    ```py
    from ultralytics import YOLO

    # Load a model
    model = YOLO('yolov8n-seg.pt')
    
    # Run inference
    result = model.predict()
    ```

    ??? question "No Prediction Arguments?"

        Without specifying a source, the example images from the library will be used:

        ```
        'ultralytics/assets/bus.jpg'
        'ultralytics/assets/zidane.jpg'
        ```

        This is helpful for rapid testing with the `predict()` method.

    For additional information about Segmentation Models, visit the [Segment Task](../tasks/segment.md#models) page. To learn more about `predict()` method, see [Predict Mode](../modes/predict.md) section of the Documentation.
    
    ***

3. Now iterate over the results and the contours. For workflows that want to save an image to file, the source image `base-name` and the detection `class-label` are retrieved for later use (optional).
.
## Recipe Walk Through

1. Begin with the necessary imports

    ```py
    from pathlib import Path

    import cv2 as cv
    import numpy as np
    from ultralytics import YOLO
    ```

    ???+ tip "Ultralytics Install"
        See the Ultralytics [Quickstart](../quickstart.md/#install-ultralytics) Installation section for a quick walkthrough on installing the required libraries.

    ______________________________________________________________________

1. Load a model and run `predict()` method on a source.

    ```py
    from ultralytics import YOLO

    # Load a model
    model = YOLO('yolov8n-seg.pt')

    # Run inference
    result = model.predict()
    ```

    ??? question "No Prediction Arguments?"
        Without specifying a source, the example images from the library will be used:

        ```
        'ultralytics/assets/bus.jpg'
        'ultralytics/assets/zidane.jpg'
        ```

        This is helpful for rapid testing with the `predict()` method.

    For additional information about Segmentation Models, visit the [Segment Task](../tasks/segment.md#models) page. To learn more about `predict()` method, see [Predict Mode](../modes/predict.md) section of the Documentation.

    ______________________________________________________________________

1. Now iterate over the results and the contours. For workflows that want to save an image to file, the source image `base-name` and the detection `class-label` are retrieved for later use (optional).
.


Example of non-code content from Material-MKDocs documentation without admonitions
.
=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci
.
=== "Unordered list"
    - Sed sagittis eleifend rutrum
    - Donec vitae suscipit est
    - Nulla tempor lobortis orci

=== "Ordered list"
    1. Sed sagittis eleifend rutrum
    1. Donec vitae suscipit est
    1. Nulla tempor lobortis orci
.


Example from Material-MKDocs documentation within an admonition
.
!!! example
    === "Unordered List"
        ```markdown
        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci
        ```

    === "Ordered List"
        ```markdown
        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
        ```
.
!!! example
    === "Unordered List"
        ```markdown
        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci
        ```

    === "Ordered List"
        ```markdown
        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
        ```
.
