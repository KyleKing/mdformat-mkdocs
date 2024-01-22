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
