Dashed list
.
- item 1
    - item 2
.
.


Numbered list
.
1. item 1
    1. item 2-a
        1. item 3-a
    2. item 2-b
        1. item 3-b
        2. item 3-b
.
.


Combination list
.
- item 1
    * item 2
        1. item 3
.
.


Corrected Indentation from 3x
.
- item 1
   - item 2
      - item 3
         - item 4
.
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
.


Deterministic HTML Formatting
.
??? info "Full-size Image"
    There are no additional steps required if keeping full size image.

    <figure markdown>
         ![Example Full size Isolated Object Image Black Background](https://github.com/ultralytics/ultralytics/assets/62214284/845c00d0-52a6-4b1e-8010-4ba73e011b99){ width=240 }
       <figcaption>Example full-size output</figcaption>
    </figure>
.
.


Correctly identifies peers when numbering
.
1. One
    1. 1-A
2. Two
    1. 2-A
    2. 2-B
.
.

Do not format code (https://github.com/KyleKing/mdformat-mkdocs/issues/36). Also tested in `test_wrap` for resulting format
.
# A B C

1. Create a `.pre-commit-config.yaml` file in your repository and add the desired
   hooks. For example:

   ```yaml
   repos:
     - repo: https://github.com/psf/black
       rev: v24.4

   ```

   ```md
   # Title
   Content
   1. Numbered List
     * Unordered Sub-List
   ```
.
.

Support inline bulleted code (https://github.com/KyleKing/mdformat-mkdocs/issues/40)
.
- ```python
  for idx in range(10):
      print(idx)
  ```
.
.
