Standard mkdocstrings injection
.
::: package.module.Class
.
::: package.module.Class
.

mkdocstrings injection with options
.
::: package.module.Class
    options:
      heading_level: 2
      show_source: true
.
::: package.module.Class
    options:
      heading_level: 2
      show_source: true
.

mkdocstrings injection with blank line in options
.
::: package.module.Class
    options:
      heading_level: 2

      show_source: true
.
::: package.module.Class
    options:
      heading_level: 2

      show_source: true
.

mkdocstrings injection nested in list
.
- List item:
    ::: package.module.Class
        options:
          heading_level: 2
.
- List item:
    ::: package.module.Class
        options:
          heading_level: 2
.

mkdocstrings injection nested in list with blank line
.
- List item:
    ::: package.module.Class
        options:
          heading_level: 2

          show_source: true
.
- List item:
    ::: package.module.Class
        options:
          heading_level: 2

          show_source: true
.

mkdocstrings injection with private submodule
.
::: my_package._private_module
.
::: my_package._private_module
.

mkdocstrings injection with private submodule nested in list
.
- List item:
    ::: my_package._private_module
        options:
          heading_level: 2
.
- List item:
    ::: my_package._private_module
        options:
          heading_level: 2
.
