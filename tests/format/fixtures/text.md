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


Table (squished by mdformat>=0.7.19)
.
| Label          |   Rating | Comment              |
|:---------------|---------:|:---------------------|
| Name           |         2| <!-- Comment -->     |
.
| Label | Rating | Comment |
|:---------------|---------:|:---------------------|
| Name | 2| <!-- Comment --> |
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
# [h1] The largest heading

## [h2] heading

### [h3] heading

#### [h4] heading

##### [h5] heading

###### [h6] The smallest heading
.

Task List / Check List
.
- [x] #739
  - [ ] Add delight to the experience when all tasks are complete :tada:
.
- [x] #739
    - [ ] Add delight to the experience when all tasks are complete :tada:
.

Footnotes (WARN: escaping is prevented by mdformat-gfm. Tested by py#-hook)
.
Here is a simple footnote[^1].

You can also use words, to fit your writing style more closely[^note].

  [^1]: My reference.
  [^note]: Named footnotes will still render with numbers instead of the text but allow easier identification and linking.\
    This footnote also has been made with a different syntax using 4 spaces for new lines.
.
Here is a simple footnote[^1].

You can also use words, to fit your writing style more closely[^note].

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


MkDocs Closed Collapsible Sections
.
??? note
     content
.
??? note
    content
.


MkDocs Open Collapsible Sections
.
???+ note
     content
.
???+ note
    content
.


Formats non-root lists
.
!!! note
    1. a
        1. b
        2. c
            1. d
.
!!! note
    1. a
        1. b
        1. c
            1. d
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


Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/fd82a671015a30a869d740c45c65f5633d1d93c4/docs/en/guides/isolating-segmentation-objects.md?plain=1#L148-L259)
.
1. Next the there are 2 options for how to move forward with the image from this point and a subsequent option for each.

    ### Object Isolation Options

    !!! example ""

        === "Black Background Pixels"

            ```py
            # Create 3-channel mask
            mask3ch = cv.cvtColor(b_mask, cv.COLOR_GRAY2BGR)

            # Isolate object with binary mask
            isolated = cv.bitwise_and(mask3ch, img)

            ```

            ??? question "How does this work?"

                - First, the binary mask is first converted from a single-channel image to a three-channel image. This conversion is necessary for the subsequent step where the mask and the original image are combined. Both images must have the same number of channels to be compatible with the blending operation.

                - The original image and the three-channel binary mask are merged using the OpenCV function `bitwise_and()`. This operation retains <u>only</u> pixel values that are greater than zero `(> 0)` from both images. Since the mask pixels are greater than zero `(> 0)` <u>only</u> within the contour region, the pixels remaining from the original image are those that overlap with the contour.

            ### Isolate with Black Pixels: Sub-options

            ??? info "Full-size Image"

                There are no additional steps required if keeping full size image.

                <figure markdown>
                    ![Example Full size Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/845c00d0-52a6-4b1e-8010-4ba73e011b99){ width=240 }
                    <figcaption>Example full-size output</figcaption>
                </figure>

            ??? info "Cropped object Image"

                Additional steps required to crop image to only include object region.

                ![Example Crop Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/103dbf90-c169-4f77-b791-76cdf09c6f22){ align="right" }

                ``` { .py .annotate }
                # (1) Bounding box coordinates
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
                # Crop image to object region
                iso_crop = isolated[y1:y2, x1:x2]

                ```

                1.  For more information on bounding box results, see [Boxes Section from Predict Mode](../modes/predict.md/#boxes)

                ??? question "What does this code do?"

                    - The `c.boxes.xyxy.cpu().numpy()` call retrieves the bounding boxes as a NumPy array in the `xyxy` format, where `xmin`, `ymin`, `xmax`, and `ymax` represent the coordinates of the bounding box rectangle. See [Boxes Section from Predict Mode](../modes/predict.md/#boxes) for more details.

                    - The `squeeze()` operation removes any unnecessary dimensions from the NumPy array, ensuring it has the expected shape.

                    - Converting the coordinate values using `.astype(np.int32)` changes the box coordinates data type from `float32` to `int32`, making them compatible for image cropping using index slices.

                    - Finally, the bounding box region is cropped from the image using index slicing. The bounds are defined by the `[ymin:ymax, xmin:xmax]` coordinates of the detection bounding box.

        === "Transparent Background Pixels"

            ```py
            # Isolate object with transparent background (when saved as PNG)
            isolated = np.dstack([img, b_mask])

            ```

            ??? question "How does this work?"

                - Using the NumPy `dstack()` function (array stacking along depth-axis) in conjunction with the binary mask generated, will create an image with four channels. This allows for all pixels outside of the object contour to be transparent when saving as a `PNG` file.

            ### Isolate with Transparent Pixels: Sub-options

            ??? info "Full-size Image"

                There are no additional steps required if keeping full size image.

                <figure markdown>
                    ![Example Full size Isolated Object Image No Background](https://github.com/ultralytics/ultralytics/assets/62214284/b1043ee0-369a-4019-941a-9447a9771042){ width=240 }
                    <figcaption>Example full-size output + transparent background</figcaption>
                </figure>

            ??? info "Cropped object Image"

                Additional steps required to crop image to only include object region.

                ![Example Crop Isolated Object Image No Background](https://github.com/ultralytics/ultralytics/assets/62214284/5910244f-d1e1-44af-af7f-6dea4c688da8){ align="right" }

                ``` { .py .annotate }
                # (1) Bounding box coordinates
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
                # Crop image to object region
                iso_crop = isolated[y1:y2, x1:x2]

                ```

                1.  For more information on bounding box results, see [Boxes Section from Predict Mode](../modes/predict.md/#boxes)

                ??? question "What does this code do?"

                    - When using `c.boxes.xyxy.cpu().numpy()`, the bounding boxes are returned as a NumPy array, using the `xyxy` box coordinates format, which correspond to the points `xmin, ymin, xmax, ymax` for the bounding box (rectangle), see [Boxes Section from Predict Mode](../modes/predict.md/#boxes) for more information.

                    - Adding `squeeze()` ensures that any extraneous dimensions are removed from the NumPy array.

                    - Converting the coordinate values using `.astype(np.int32)` changes the box coordinates data type from `float32` to `int32` which will be compatible when cropping the image using index slices.

                    - Finally the image region for the bounding box is cropped using index slicing, where the bounds are set using the `[ymin:ymax, xmin:xmax]` coordinates of the detection bounding box.

    ??? question "What if I want the cropped object **including** the background?"

        This is a built in feature for the Ultralytics library. See the `save_crop` argument for  [Predict Mode Inference Arguments](../modes/predict.md/#inference-arguments) for details.

    ---
.
1. Next the there are 2 options for how to move forward with the image from this point and a subsequent option for each.

    ### Object Isolation Options

    !!! example ""
        === "Black Background Pixels"
            ```py
            # Create 3-channel mask
            mask3ch = cv.cvtColor(b_mask, cv.COLOR_GRAY2BGR)

            # Isolate object with binary mask
            isolated = cv.bitwise_and(mask3ch, img)

            ```

            ??? question "How does this work?"
                - First, the binary mask is first converted from a single-channel image to a three-channel image. This conversion is necessary for the subsequent step where the mask and the original image are combined. Both images must have the same number of channels to be compatible with the blending operation.

                - The original image and the three-channel binary mask are merged using the OpenCV function `bitwise_and()`. This operation retains <u>only</u> pixel values that are greater than zero `(> 0)` from both images. Since the mask pixels are greater than zero `(> 0)` <u>only</u> within the contour region, the pixels remaining from the original image are those that overlap with the contour.

            ### Isolate with Black Pixels: Sub-options

            ??? info "Full-size Image"
                There are no additional steps required if keeping full size image.

                <figure markdown>
                ![Example Full size Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/845c00d0-52a6-4b1e-8010-4ba73e011b99){ width=240 }
                <figcaption>Example full-size output</figcaption>
                </figure>

            ??? info "Cropped object Image"
                Additional steps required to crop image to only include object region.

                ![Example Crop Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/103dbf90-c169-4f77-b791-76cdf09c6f22){ align="right" }

                ```{ .py .annotate }
                # (1) Bounding box coordinates
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
                # Crop image to object region
                iso_crop = isolated[y1:y2, x1:x2]

                ```

                1. For more information on bounding box results, see [Boxes Section from Predict Mode](../modes/predict.md/#boxes)

                ??? question "What does this code do?"
                    - The `c.boxes.xyxy.cpu().numpy()` call retrieves the bounding boxes as a NumPy array in the `xyxy` format, where `xmin`, `ymin`, `xmax`, and `ymax` represent the coordinates of the bounding box rectangle. See [Boxes Section from Predict Mode](../modes/predict.md/#boxes) for more details.

                    - The `squeeze()` operation removes any unnecessary dimensions from the NumPy array, ensuring it has the expected shape.

                    - Converting the coordinate values using `.astype(np.int32)` changes the box coordinates data type from `float32` to `int32`, making them compatible for image cropping using index slices.

                    - Finally, the bounding box region is cropped from the image using index slicing. The bounds are defined by the `[ymin:ymax, xmin:xmax]` coordinates of the detection bounding box.

        === "Transparent Background Pixels"
            ```py
            # Isolate object with transparent background (when saved as PNG)
            isolated = np.dstack([img, b_mask])

            ```

            ??? question "How does this work?"
                - Using the NumPy `dstack()` function (array stacking along depth-axis) in conjunction with the binary mask generated, will create an image with four channels. This allows for all pixels outside of the object contour to be transparent when saving as a `PNG` file.

            ### Isolate with Transparent Pixels: Sub-options

            ??? info "Full-size Image"
                There are no additional steps required if keeping full size image.

                <figure markdown>
                ![Example Full size Isolated Object Image No Background](https://github.com/ultralytics/ultralytics/assets/62214284/b1043ee0-369a-4019-941a-9447a9771042){ width=240 }
                <figcaption>Example full-size output + transparent background</figcaption>
                </figure>

            ??? info "Cropped object Image"
                Additional steps required to crop image to only include object region.

                ![Example Crop Isolated Object Image No Background](https://github.com/ultralytics/ultralytics/assets/62214284/5910244f-d1e1-44af-af7f-6dea4c688da8){ align="right" }

                ```{ .py .annotate }
                # (1) Bounding box coordinates
                x1, y1, x2, y2 = c.boxes.xyxy.cpu().numpy().squeeze().astype(np.int32)
                # Crop image to object region
                iso_crop = isolated[y1:y2, x1:x2]

                ```

                1. For more information on bounding box results, see [Boxes Section from Predict Mode](../modes/predict.md/#boxes)

                ??? question "What does this code do?"
                    - When using `c.boxes.xyxy.cpu().numpy()`, the bounding boxes are returned as a NumPy array, using the `xyxy` box coordinates format, which correspond to the points `xmin, ymin, xmax, ymax` for the bounding box (rectangle), see [Boxes Section from Predict Mode](../modes/predict.md/#boxes) for more information.

                    - Adding `squeeze()` ensures that any extraneous dimensions are removed from the NumPy array.

                    - Converting the coordinate values using `.astype(np.int32)` changes the box coordinates data type from `float32` to `int32` which will be compatible when cropping the image using index slices.

                    - Finally the image region for the bounding box is cropped using index slicing, where the bounds are set using the `[ymin:ymax, xmin:xmax]` coordinates of the detection bounding box.

    ??? question "What if I want the cropped object **including** the background?"
        This is a built in feature for the Ultralytics library. See the `save_crop` argument for [Predict Mode Inference Arguments](../modes/predict.md/#inference-arguments) for details.

    ______________________________________________________________________
.


Example of non-code content from Material-MkDocs documentation without admonitions
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


Example from Material-MkDocs documentation within an admonition
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

Example with '===!' (break) from <https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/#syntax>
.
=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b

===! "Tab A"
     Different tab set.

=== "Tab B"
    ```
    More content.
    ```
.
=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b

===! "Tab A"
    Different tab set.

=== "Tab B"
    ```
    More content.
    ```
.


Example with '===+' (active) from <https://facelessuser.github.io/pymdown-extensions/extensions/tabbed/#syntax>
.
=== "Not Me"
     Markdown **content**.

     Multiple paragraphs.

===+ "Select Me"
     More Markdown **content**.

     - list item a
     - list item b

=== "Not Me Either"
     Another Tab
.
=== "Not Me"
    Markdown **content**.

    Multiple paragraphs.

===+ "Select Me"
    More Markdown **content**.

    - list item a
    - list item b

=== "Not Me Either"
    Another Tab
.


More complex example to validate formatting when nested
.
1. List Outer

    ???+ Note

        === "First"

             Markdown **content**.

             Multiple paragraphs.

            ??? "Second"

                 Markdown **content**.

                 Multiple paragraphs.

                ===+ "Third"

                     - List Item

                     - Another Item

                        === "Fourth"

                             - List Item

                             - Another Item

                        ===! "Lastly a new item"

                            Markdown **content** for last item.

                            Very last indented paragraph.

2. Next
.
1. List Outer

    ???+ Note
        === "First"
            Markdown **content**.

            Multiple paragraphs.

            ??? "Second"
                Markdown **content**.

                Multiple paragraphs.

                ===+ "Third"
                    - List Item

                    - Another Item

                        === "Fourth"
                            - List Item

                            - Another Item

                        ===! "Lastly a new item"
                            Markdown **content** for last item.

                            Very last indented paragraph.

1. Next
.


Deterministic indents for HTML
.
1. List Item

    ### Object Isolation Options

    ??? info "Full-size Image"
        There are no additional steps required if keeping full size image.

        <figure markdown>
            ![Example Full size Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/845c00d0-52a6-4b1e-8010-4ba73e011b99){ width=240 }
          <figcaption>Example full-size output</figcaption>
         </figure>
.
1. List Item

    ### Object Isolation Options

    ??? info "Full-size Image"
        There are no additional steps required if keeping full size image.

        <figure markdown>
        ![Example Full size Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/845c00d0-52a6-4b1e-8010-4ba73e011b99){ width=240 }
        <figcaption>Example full-size output</figcaption>
        </figure>
.


Another Ultralytics Example
.
## Generating Feature Vectors for Object Detection Dataset

1. Start by creating a new Python file and import the required libraries.

2. The following is a sample view of the populated DataFrame:

    ```pandas
                                                           0    1    2    3    4    5
    '0000a16e4b057580_jpg.rf.00ab48988370f64f5ca8ea4...'  0.0  0.0  0.0  0.0  0.0  7.0
    '0000a16e4b057580_jpg.rf.7e6dce029fb67f01eb19aa7...'  0.0  0.0  0.0  0.0  0.0  7.0
    '0000a16e4b057580_jpg.rf.bc4d31cdcbe229dd022957a...'  0.0  0.0  0.0  0.0  0.0  7.0
    '00020ebf74c4881c_jpg.rf.508192a0a97aa6c4a3b6882...'  0.0  0.0  0.0  1.0  0.0  0.0
    '00020ebf74c4881c_jpg.rf.5af192a2254c8ecc4188a25...'  0.0  0.0  0.0  1.0  0.0  0.0
     ...                                                  ...  ...  ...  ...  ...  ...
    'ff4cd45896de38be_jpg.rf.c4b5e967ca10c7ced3b9e97...'  0.0  0.0  0.0  0.0  0.0  2.0
    'ff4cd45896de38be_jpg.rf.ea4c1d37d2884b3e3cbce08...'  0.0  0.0  0.0  0.0  0.0  2.0
    'ff5fd9c3c624b7dc_jpg.rf.bb519feaa36fc4bf630a033...'  1.0  0.0  0.0  0.0  0.0  0.0
    'ff5fd9c3c624b7dc_jpg.rf.f0751c9c3aa4519ea3c9d6a...'  1.0  0.0  0.0  0.0  0.0  0.0
    'fffe28b31f2a70d4_jpg.rf.7ea16bd637ba0711c53b540...'  0.0  6.0  0.0  0.0  0.0  0.0
    ```

The rows index the label files, each corresponding to an image in your dataset, and the columns correspond to your class-label indices. Each row represents a pseudo feature-vector, with the count of each class-label present in your dataset. This data structure enables the application of K-Fold Cross Validation to an object detection dataset.
.
## Generating Feature Vectors for Object Detection Dataset

1. Start by creating a new Python file and import the required libraries.

1. The following is a sample view of the populated DataFrame:

    ```pandas
                                                           0    1    2    3    4    5
    '0000a16e4b057580_jpg.rf.00ab48988370f64f5ca8ea4...'  0.0  0.0  0.0  0.0  0.0  7.0
    '0000a16e4b057580_jpg.rf.7e6dce029fb67f01eb19aa7...'  0.0  0.0  0.0  0.0  0.0  7.0
    '0000a16e4b057580_jpg.rf.bc4d31cdcbe229dd022957a...'  0.0  0.0  0.0  0.0  0.0  7.0
    '00020ebf74c4881c_jpg.rf.508192a0a97aa6c4a3b6882...'  0.0  0.0  0.0  1.0  0.0  0.0
    '00020ebf74c4881c_jpg.rf.5af192a2254c8ecc4188a25...'  0.0  0.0  0.0  1.0  0.0  0.0
     ...                                                  ...  ...  ...  ...  ...  ...
    'ff4cd45896de38be_jpg.rf.c4b5e967ca10c7ced3b9e97...'  0.0  0.0  0.0  0.0  0.0  2.0
    'ff4cd45896de38be_jpg.rf.ea4c1d37d2884b3e3cbce08...'  0.0  0.0  0.0  0.0  0.0  2.0
    'ff5fd9c3c624b7dc_jpg.rf.bb519feaa36fc4bf630a033...'  1.0  0.0  0.0  0.0  0.0  0.0
    'ff5fd9c3c624b7dc_jpg.rf.f0751c9c3aa4519ea3c9d6a...'  1.0  0.0  0.0  0.0  0.0  0.0
    'fffe28b31f2a70d4_jpg.rf.7ea16bd637ba0711c53b540...'  0.0  6.0  0.0  0.0  0.0  0.0
    ```

The rows index the label files, each corresponding to an image in your dataset, and the columns correspond to your class-label indices. Each row represents a pseudo feature-vector, with the count of each class-label present in your dataset. This data structure enables the application of K-Fold Cross Validation to an object detection dataset.
.

Support Link Reference Definitions
.
[foo]: /url "title"

[foo]

[link][foo]
.
[foo]

[link][foo]

[foo]: /url "title"
.

mdformat>=0.7.19 no longer escapes brackets (https://github.com/KyleKing/mdformat-mkdocs/issues/19)
.
[package.module.object][]
[Object][package.module.object]
.
[package.module.object][]
[Object][package.module.object]
.

Do not format lists in code blocks
.
* Item 1

   ```text
   * sample plain text block.
   ```
.
- Item 1

    ```text
    * sample plain text block.
    ```
.

Ignore multiple empty lines within code blocks
.
* Item 1

    ```text




    * Asterisk
    ```
.
- Item 1

    ```text




    * Asterisk
    ```
.

0-indexed markdown list (https://github.com/KyleKing/mdformat-mkdocs/issues/24)
.
0. xyz
4. abc
    1. inner
    3. next
.
0. xyz
0. abc
    1. inner
    1. next
.

Unsupported versions of 0-indexed markdown list (Within unordered list)
.
* unordered
    0. xyz
    5. abc
        1. inner
        4. next
.
- unordered
    0\. xyz
    5\. abc
    1\. inner
    4\. next
.

Unsupported versions of 0-indexed markdown list (Within ordered list)
.
0. ordered
    0. xyz
    5. abc
        1. inner
        4. next
1. next
.
0. ordered
    0\. xyz
    5\. abc
    1\. inner
    4\. next
0. next
.

Broken code block because of `>` (https://github.com/KyleKing/mdformat-mkdocs/issues/31)
.
# Title

1.  Without '<'

     ```bash
     echo \
      container name>
     ```

1.  With '<'

     ```bash
     echo \
      <container name>
     echo $VAR
     ```
.
# Title

1. Without '\<'

    ```bash
    echo \
     container name>
    ```

1. With '\<'

    ```bash
    echo \
     <container name>
    echo $VAR
    ```
.

Broken formatting (https://github.com/KyleKing/mdformat-mkdocs/issues/35)
.
# A B C

1. Test
    ```bash
    python -m pip install foo
    ```

2. Another
   For example:

    ```yaml
    repos:
      - repo: https://github.com/psf/black
        rev: v24.4
        hooks:
        - id: black
    ```
.
# A B C

1. Test

    ```bash
    python -m pip install foo
    ```

1. Another
    For example:

    ```yaml
    repos:
      - repo: https://github.com/psf/black
        rev: v24.4
        hooks:
        - id: black
    ```
.

Support inline bulleted code (https://github.com/KyleKing/mdformat-mkdocs/issues/40)
.
- ```python
  for idx in range(10):
      print(idx)
  ```

  1. ```bash
     for match in %(ls);
         do echo match;
     done
     ```

     - ```powershell
       iex (new-object net.webclient).DownloadString('https://get.scoop.sh')
       ```
.
- ```python
  for idx in range(10):
      print(idx)
  ```

    1. ```bash
       for match in %(ls);
           do echo match;
       done
       ```

        - ```powershell
          iex (new-object net.webclient).DownloadString('https://get.scoop.sh')
          ```
.
