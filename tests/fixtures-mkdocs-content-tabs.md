Simple content tab
.
=== "CLI"

    ```bash
    echo 'args'
    ```

Regular content
.
<div class="content-tab">
<p class="content-tab-title">CLI</p>
<pre><code class="language-bash">echo 'args'
</code></pre>
</div>
<p>Regular content</p>
.


No vertical separation
.
=== "CLI"
    ```bash
    echo 'args'
    ```
.
<div class="content-tab">
<p class="content-tab-title">CLI</p>
<pre><code class="language-bash">echo 'args'
</code></pre>
</div>
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
<div class="content-tab">
<p class="content-tab-title">Unordered list</p>
<ul>
<li>Sed sagittis eleifend rutrum</li>
<li>Donec vitae suscipit est</li>
<li>Nulla tempor lobortis orci</li>
</ul>
</div>
<div class="content-tab">
<p class="content-tab-title">Ordered list</p>
<ol>
<li>Sed sagittis eleifend rutrum</li>
<li>Donec vitae suscipit est</li>
<li>Nulla tempor lobortis orci</li>
</ol>
</div>
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
<div class="admonition example">
<p class="admonition-title">Example</p>
<div class="content-tab">
<p class="content-tab-title">Unordered List</p>
<pre><code class="language-markdown">* Sed sagittis eleifend rutrum
* Donec vitae suscipit est
* Nulla tempor lobortis orci
</code></pre>
</div>
<div class="content-tab">
<p class="content-tab-title">Ordered List</p>
<pre><code class="language-markdown">1. Sed sagittis eleifend rutrum
2. Donec vitae suscipit est
3. Nulla tempor lobortis orci
</code></pre>
</div>
</div>
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
<p>Ultralytics commands use the following syntax:</p>
<div class="admonition example">
<p class="admonition-title">Example</p>
<div class="content-tab">
<p class="content-tab-title">CLI</p>
<pre><code class="language-bash">yolo TASK MODE ARGS
</code></pre>
</div>
<div class="content-tab">
<p class="content-tab-title">Python</p>
<pre><code class="language-python">from ultralytics import YOLO

# Load a YOLOv8 model from a pre-trained weights file
model = YOLO('yolov8n.pt')

# Run MODE mode using the custom arguments ARGS (guess TASK)
model.MODE(ARGS)
</code></pre>
</div>
</div>
.


Example from Ultralytics Documentation (https://github.com/ultralytics/ultralytics/blob/0e7221fb62191e18e5ec4f7a9fe6d8927a4446c2/docs/zh/datasets/index.md#L105-L127)
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
<h3>优化和压缩数据集的示例代码</h3>
<div class="admonition example">
<p class="admonition-title">优化和压缩数据集</p>
<div class="content-tab">
<p class="content-tab-title">Python</p>
</div>
<pre><code class="language-python">from pathlib import Path
from ultralytics.data.utils import compress_one_image
from ultralytics.utils.downloads import zip_directory

# 定义数据集目录
path = Path('path/to/dataset')

# 优化数据集中的图像（可选）
for f in path.rglob('*.jpg'):
    compress_one_image(f)

# 将数据集压缩成 'path/to/dataset.zip'
zip_directory(path)
</code></pre>
</div>
<p>通过遵循这些步骤，您可以贡献一个与 Ultralytics 现有结构良好融合的新数据集。</p>
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
<h2>Citations and Acknowledgments</h2>
<p>If you use the Caltech-101 dataset in your research or development work, please cite the following paper:</p>
<div class="admonition quote">
<div class="content-tab">
<p class="content-tab-title">BibTeX</p>
<pre><code class="language-bibtex">@article{fei2007learning,
  title={Learning generative visual models from few training examples: An incremental Bayesian approach tested on 101 object categories},
  author={Fei-Fei, Li and Fergus, Rob and Perona, Pietro},
  journal={Computer vision and Image understanding},
  volume={106},
  number={1},
  pages={59--70},
  year={2007},
  publisher={Elsevier}
}
</code></pre>
</div>
</div>
.


.
!!! Example "Update Ultralytics MLflow Settings"

    === "Python"
        Within the Python environment, call the `update` method on the `settings` object to change your settings:
        ```python
        from ultralytics import settings

        # Update a setting
        settings.update({'mlflow': True})

        # Reset settings to default values
        settings.reset()
        ```

    === "CLI"
        If you prefer using the command-line interface, the following commands will allow you to modify your settings:
        ```bash
        # Update a setting
        yolo settings runs_dir='/path/to/runs'

        # Reset settings to default values
        yolo settings reset
        ```
.
<div class="admonition example">
<p class="admonition-title">Update Ultralytics MLflow Settings</p>
<div class="content-tab">
<p class="content-tab-title">Python</p>
<p>Within the Python environment, call the <code>update</code> method on the <code>settings</code> object to change your settings:</p>
<pre><code class="language-python">from ultralytics import settings

# Update a setting
settings.update({'mlflow': True})

# Reset settings to default values
settings.reset()
</code></pre>
</div>
<div class="content-tab">
<p class="content-tab-title">CLI</p>
<p>If you prefer using the command-line interface, the following commands will allow you to modify your settings:</p>
<pre><code class="language-bash"># Update a setting
yolo settings runs_dir='/path/to/runs'

# Reset settings to default values
yolo settings reset
</code></pre>
</div>
</div>
.
