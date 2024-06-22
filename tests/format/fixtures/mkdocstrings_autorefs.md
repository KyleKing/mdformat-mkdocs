Header-Anchor links, but I'm unsure how to remove the line separator (Initial attempt: https://github.com/KyleKing/mdformat-mkdocs/commit/055aca6ebadc505d60a00c3a8ae575314b11c276)
.
[](){#some-anchor-name}
# Some Title
.
[](){#some-anchor-name}

# Some Title
.

Broken Anchor links (https://github.com/KyleKing/mdformat-mkdocs/issues/25)
.
[](<>){#some-anchor-name}
.
[](){#some-anchor-name}
.
