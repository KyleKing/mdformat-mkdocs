Dashed list
.
- item 1
    - item 2
.
{
    "new_indents": [
        "",
        "    "
    ],
    "new_contents": [
        "- item 1",
        "- item 2"
    ],
    "lines": [
        {
            "parsed": [
                "",
                "- item 1",
                null
            ],
            "parents": []
        },
        {
            "parsed": [
                "    ",
                "- item 2",
                null
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    null
                ]
            ]
        }
    ],
    "code_block_indents": [
        null,
        null
    ]
}
.

Asterisk list
.
* item 1
    * item 2
.
{
  "new_indents": [
    "",
    "    "
  ],
  "new_contents": [
    "- item 1",
    "- item 2"
  ],
  "bullets": [
    "-",
    "-"
  ],
  "code_block_indents": [
    null,
    null
  ]
}
.

Numbered list
.
1. item 1
    1. item 2
    2. item 2
        1. item 3
        2. item 3
.
{
  "new_indents": [
    "",
    "    ",
    "        ",
    "            ",
    "                ",
    ""
  ],
  "new_contents": [
    "1. item 1",
    "1. item 2",
    "2. item 2",
    "1. item 3",
    "2. item 3",
    ""
  ],
  "bullets": [
    "",
    "",
    "",
    "",
    "",
    ""
  ],
  "code_block_indents": [
    null,
    null,
    null,
    null,
    null,
    null
  ]
}
.

Combination list
.
- item 1
    * item 2
        1. item 3
.
{
  "new_indents": [
    "",
    "    ",
    "            ",
    ""
  ],
  "new_contents": [
    "- item 1",
    "* item 2",
    "1. item 3",
    ""
  ],
  "bullets": [
    "",
    "",
    "",
    ""
  ],
  "code_block_indents": [
    null,
    null,
    null,
    null
  ]
}
.

Corrected Indentation from 3x
.
- item 1
   - item 2
      - item 3
         - item 4
.
{
  "new_indents": [
    "",
    "    ",
    "        ",
    "                ",
    ""
  ],
  "new_contents": [
    "- item 1",
    "- item 2",
    "- item 3",
    "- item 4",
    ""
  ],
  "bullets": [
    "",
    "",
    "",
    "",
    ""
  ],
  "code_block_indents": [
    null,
    null,
    null,
    null,
    null
  ]
}
.
