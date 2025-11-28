Escaped Delimiters
.
This is not math: \$escaped\$ and \\(also escaped\\).

Literal dollar: I paid \$5.00 for \$3.00 worth.
.
This is not math: $escaped$ and \\(also escaped\\).

Literal dollar: I paid $5.00 for $3.00 worth.
.

Math in Lists
.
1. First item with math $x = y$
2. Second item with block math:

    $$
    E = mc^2
    $$

3. Third item with nested list:
    - Nested with $a = b$
    - More nested:

        $$
        F = ma
        $$
.
1. First item with math $x = y$

1. Second item with block math:

    $$
    E = mc^2
    $$

1. Third item with nested list:

    - Nested with $a = b$

    - More nested:

        $$
        F = ma
        $$
.

Math in Blockquotes
.
> Einstein said $E = mc^2$
>
> The full equation:
>
> $$
> E = mc^2
> $$
.
> Einstein said $E = mc^2$
>
> The full equation:
>
> $$
> > E = mc^2
> >
> $$
.

Equation Labels with Square Brackets
.
The Pythagorean theorem:

\[
a^2 + b^2 = c^2
\] (eq:pythagoras)

Reference equation (eq:pythagoras) above.
.
The Pythagorean theorem:

\[
a^2 + b^2 = c^2
\] (eq:pythagoras)

Reference equation (eq:pythagoras) above.
.

Equation Labels with Dollar Signs
.
Maxwell's equations:

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}
$$ (eq:gauss)

See equation (eq:gauss) for Gauss's law.
.
Maxwell's equations:

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}
$$ (eq:gauss)

See equation (eq:gauss) for Gauss's law.
.

Math with Line Breaks
.
$$
x = a + b + c
  + d + e
  + f
$$
.
$$
x = a + b + c
  + d + e
  + f
$$
.

Math in Tables
.
| Formula | Description |
| ------- | ----------- |
| $E=mc^2$ | Energy-mass |
| $F=ma$ | Force |
| \(p=mv\) | Momentum |
.
| Formula | Description |
| ------- | ----------- |
| $E=mc^2$ | Energy-mass |
| $F=ma$ | Force |
| \(p=mv\) | Momentum |
.

Math at Line Boundaries
.
$start of line$ and $end of line$
$x=y$
\(a=b\) and \(c=d\)
.
$start of line$ and $end of line$
$x=y$
\(a=b\) and \(c=d\)
.

Special Characters in Math
.
Brackets: $[a, b]$ and braces: $\{x \in X\}$

Pipes: $|x|$ and backslash: $\backslash$

Underscores: $x_1, x_2, \ldots, x_n$

Carets: $x^2 + y^2 = z^2$
.
Brackets: $[a, b]$ and braces: $\{x \in X\}$

Pipes: $|x|$ and backslash: $\backslash$

Underscores: $x_1, x_2, \ldots, x_n$

Carets: $x^2 + y^2 = z^2$
.

Adjacent Math Expressions
.
Multiple inline: $a$ $b$ $c$

With text between: $x$ and $y$ and $z$

Different delimiters: $a$ \(b\) $c$
.
Multiple inline: $a$ $b$ $c$

With text between: $x$ and $y$ and $z$

Different delimiters: $a$ \(b\) $c$
.

Math with Leading/Trailing Whitespace
.
$$
   x = y
$$

\[
   a = b
\]
.
$$
x = y
$$

\[
a = b
\]
.

Multiline Inline Math
.
This has inline math $\frac{a}{b}$ in it.

Complex fraction: $\frac{\frac{a}{b}}{\frac{c}{d}}$ is nested.
.
This has inline math $\frac{a}{b}$ in it.

Complex fraction: $\frac{\frac{a}{b}}{\frac{c}{d}}$ is nested.
.

Math in Code Fences (Should Not Be Parsed)
.
```python
# This should not be parsed as math
cost = $5.00 + $3.00
energy = "E = mc^2"
```

But this should: $E = mc^2$
.
```python
# This should not be parsed as math
cost = $5.00 + $3.00
energy = "E = mc^2"
```

But this should: $E = mc^2$
.

Mixed Math and Text on Same Line
.
The equation $E = mc^2$ was derived by Einstein in 1905.

Multiple: $a=1$, $b=2$, and $c=3$.

Parenthesis: \(x=y\) is equivalent to \(y=x\).
.
The equation $E = mc^2$ was derived by Einstein in 1905.

Multiple: $a=1$, $b=2$, and $c=3$.

Parenthesis: \(x=y\) is equivalent to \(y=x\).
.
