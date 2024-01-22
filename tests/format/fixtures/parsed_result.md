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
                "LIST"
            ],
            "parents": []
        },
        {
            "parsed": [
                "    ",
                "- item 2",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
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


Numbered list
.
1. item 1
    1. item 2-a
        1. item 3-a
    2. item 2-b
        1. item 3-b
        2. item 3-b
.
{
    "new_indents": [
        "",
        "    ",
        "        ",
        "    ",
        "        ",
        "        "
    ],
    "new_contents": [
        "1. item 1",
        "1. item 2-a",
        "1. item 3-a",
        "1. item 2-b",
        "1. item 3-b",
        "1. item 3-b"
    ],
    "lines": [
        {
            "parsed": [
                "",
                "1. item 1",
                "LIST"
            ],
            "parents": []
        },
        {
            "parsed": [
                "    ",
                "1. item 2-a",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "1. item 1",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "        ",
                "1. item 3-a",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "1. item 1",
                    "LIST"
                ],
                [
                    "    ",
                    "1. item 2-a",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "    ",
                "2. item 2-b",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "1. item 1",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "        ",
                "1. item 3-b",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "1. item 1",
                    "LIST"
                ],
                [
                    "    ",
                    "2. item 2-b",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "        ",
                "2. item 3-b",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "1. item 1",
                    "LIST"
                ],
                [
                    "    ",
                    "2. item 2-b",
                    "LIST"
                ]
            ]
        }
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
        "        "
    ],
    "new_contents": [
        "- item 1",
        "- item 2",
        "1. item 3"
    ],
    "lines": [
        {
            "parsed": [
                "",
                "- item 1",
                "LIST"
            ],
            "parents": []
        },
        {
            "parsed": [
                "    ",
                "* item 2",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "        ",
                "1. item 3",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "    ",
                    "* item 2",
                    "LIST"
                ]
            ]
        }
    ],
    "code_block_indents": [
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
        "            "
    ],
    "new_contents": [
        "- item 1",
        "- item 2",
        "- item 3",
        "- item 4"
    ],
    "lines": [
        {
            "parsed": [
                "",
                "- item 1",
                "LIST"
            ],
            "parents": []
        },
        {
            "parsed": [
                "   ",
                "- item 2",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "      ",
                "- item 3",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "   ",
                    "- item 2",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "         ",
                "- item 4",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "   ",
                    "- item 2",
                    "LIST"
                ],
                [
                    "      ",
                    "- item 3",
                    "LIST"
                ]
            ]
        }
    ],
    "code_block_indents": [
        null,
        null,
        null,
        null
    ]
}
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
{
    "new_indents": [
        "",
        "    ",
        "        ",
        "            ",
        "                ",
        "        ",
        "        ",
        ""
    ],
    "new_contents": [
        "- item 1",
        "- item 2",
        "- item 3",
        "- item 4",
        "- item 5",
        "- item 6",
        "- item 7",
        "- item 8"
    ],
    "lines": [
        {
            "parsed": [
                "",
                "- item 1",
                "LIST"
            ],
            "parents": []
        },
        {
            "parsed": [
                "  ",
                "- item 2",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "    ",
                "- item 3",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "  ",
                    "- item 2",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "      ",
                "- item 4",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "  ",
                    "- item 2",
                    "LIST"
                ],
                [
                    "    ",
                    "- item 3",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "        ",
                "- item 5",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "  ",
                    "- item 2",
                    "LIST"
                ],
                [
                    "    ",
                    "- item 3",
                    "LIST"
                ],
                [
                    "      ",
                    "- item 4",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "    ",
                "- item 6",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "  ",
                    "- item 2",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "    ",
                "- item 7",
                "LIST"
            ],
            "parents": [
                [
                    "",
                    "- item 1",
                    "LIST"
                ],
                [
                    "  ",
                    "- item 2",
                    "LIST"
                ]
            ]
        },
        {
            "parsed": [
                "",
                "- item 8",
                "LIST"
            ],
            "parents": []
        }
    ],
    "code_block_indents": [
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
    ]
}
.
