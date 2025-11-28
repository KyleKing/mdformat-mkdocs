ReLU Function with Mixed Syntax (Issue #45)
.
$$
ReLU(x) =
     \begin{cases}
       x &\quad\text{if } x > 0\\\
       0 &\quad\text{otherwise}
     \end{cases}
  $$

\[ x = \frac{4}{5} \]

What about inline expressions? $\Delta_{distance}= \text{Speed} \cdot \text{Time}$
.
$$
ReLU(x) =
     \begin{cases}
       x &\quad\text{if } x > 0\\\
       0 &\quad\text{otherwise}
     \end{cases}
$$

\[
x = \frac{4}{5}
\]

What about inline expressions? $\Delta_{distance}= \text{Speed} \cdot \text{Time}$
.

AMS Math - align* (unnumbered)
.
The aligned equations without numbers:

\begin{align*}
x &= a + b \\
y &= c + d \\
z &= e + f
\end{align*}

These are unnumbered aligned equations.
.
The aligned equations without numbers:

\begin{align*}
x &= a + b \\
y &= c + d \\
z &= e + f
\end{align*}

These are unnumbered aligned equations.
.

AMS Math - gather
.
Multiple equations centered:

\begin{gather}
a = b + c \\
x = y + z \\
m = n + p
\end{gather}

The gather environment centers equations.
.
Multiple equations centered:

\begin{gather}
a = b + c \\
x = y + z \\
m = n + p
\end{gather}

The gather environment centers equations.
.

AMS Math - gather*
.
Multiple equations centered without numbers:

\begin{gather*}
\sin^2 x + \cos^2 x = 1 \\
e^{i\pi} + 1 = 0 \\
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
\end{gather*}

Unnumbered gathered equations.
.
Multiple equations centered without numbers:

\begin{gather*}
\sin^2 x + \cos^2 x = 1 \\
e^{i\pi} + 1 = 0 \\
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
\end{gather*}

Unnumbered gathered equations.
.

AMS Math - multline
.
Long equation split across multiple lines:

\begin{multline}
a + b + c + d + e + f \\
+ g + h + i + j + k + l \\
+ m + n + o + p = q
\end{multline}

The multline environment handles long equations.
.
Long equation split across multiple lines:

\begin{multline}
a + b + c + d + e + f \\
+ g + h + i + j + k + l \\
+ m + n + o + p = q
\end{multline}

The multline environment handles long equations.
.

AMS Math - split
.
Split within equation environment:

\begin{equation}
\begin{split}
a &= b + c \\
  &= d + e \\
  &= f
\end{split}
\end{equation}

Split provides alignment within a single equation number.
.
Split within equation environment:

\begin{equation}
\begin{split}
a &= b + c \\
  &= d + e \\
  &= f
\end{split}
\end{equation}

Split provides alignment within a single equation number.
.

AMS Math - cases
.
Piecewise function definition:

$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
$$

The cases environment is useful for piecewise functions.
.
Piecewise function definition:

$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
$$

The cases environment is useful for piecewise functions.
.

AMS Math - matrix
.
Basic matrix:

$$
A = \begin{matrix}
a & b \\
c & d
\end{matrix}
$$

Simple matrix without delimiters.
.
Basic matrix:

$$
A = \begin{matrix}
a & b \\
c & d
\end{matrix}
$$

Simple matrix without delimiters.
.

AMS Math - pmatrix (parentheses)
.
Matrix with parentheses:

$$
B = \begin{pmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{pmatrix}
$$

The pmatrix environment adds parentheses.
.
Matrix with parentheses:

$$
B = \begin{pmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{pmatrix}
$$

The pmatrix environment adds parentheses.
.

AMS Math - bmatrix (brackets)
.
Matrix with brackets:

$$
C = \begin{bmatrix}
x & y \\
z & w
\end{bmatrix}
$$

The bmatrix environment adds square brackets.
.
Matrix with brackets:

$$
C = \begin{bmatrix}
x & y \\
z & w
\end{bmatrix}
$$

The bmatrix environment adds square brackets.
.

AMS Math - Bmatrix (braces)
.
Matrix with braces:

$$
D = \begin{Bmatrix}
\alpha & \beta \\
\gamma & \delta
\end{Bmatrix}
$$

The Bmatrix environment adds curly braces.
.
Matrix with braces:

$$
D = \begin{Bmatrix}
\alpha & \beta \\
\gamma & \delta
\end{Bmatrix}
$$

The Bmatrix environment adds curly braces.
.

AMS Math - vmatrix (vertical bars)
.
Matrix with vertical bars (determinant):

$$
\det(E) = \begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
$$

The vmatrix environment adds vertical bars for determinants.
.
Matrix with vertical bars (determinant):

$$
\det(E) = \begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
$$

The vmatrix environment adds vertical bars for determinants.
.

AMS Math - Vmatrix (double vertical bars)
.
Matrix with double vertical bars:

$$
\|F\| = \begin{Vmatrix}
x & y \\
z & w
\end{Vmatrix}
$$

The Vmatrix environment adds double vertical bars.
.
Matrix with double vertical bars:

$$
\|F\| = \begin{Vmatrix}
x & y \\
z & w
\end{Vmatrix}
$$

The Vmatrix environment adds double vertical bars.
.

AMS Math - alignat
.
Alignment at multiple points:

\begin{alignat}{2}
x &= a &&+ b \\
y &= c &&+ d \\
z &= e &&+ f
\end{alignat}

The alignat environment allows multiple alignment points.
.
Alignment at multiple points:

\begin{alignat}{2}
x &= a &&+ b \\
y &= c &&+ d \\
z &= e &&+ f
\end{alignat}

The alignat environment allows multiple alignment points.
.

AMS Math - flalign
.
Full-width alignment:

\begin{flalign}
x &= a + b \\
y &= c + d
\end{flalign}

The flalign environment uses full line width.
.
Full-width alignment:

\begin{flalign}
x &= a + b \\
y &= c + d
\end{flalign}

The flalign environment uses full line width.
.

AMS Math - eqnarray (legacy, but still supported)
.
Legacy equation array:

\begin{eqnarray}
a &=& b + c \\
x &=& y + z
\end{eqnarray}

The eqnarray environment is legacy but still works.
.
Legacy equation array:

\begin{eqnarray}
a &=& b + c \\
x &=& y + z
\end{eqnarray}

The eqnarray environment is legacy but still works.
.

Mixed AMS Environments
.
Combining different environments:

\begin{equation}
A = \begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}
\end{equation}

\begin{align}
\det(A) &= \begin{vmatrix}
1 & 2 \\
3 & 4
\end{vmatrix} \\
&= 1 \cdot 4 - 2 \cdot 3 \\
&= -2
\end{align}

Multiple environments working together.
.
Combining different environments:

\begin{equation}
A = \begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}
\end{equation}

\begin{align}
\det(A) &= \begin{vmatrix}
1 & 2 \\
3 & 4
\end{vmatrix} \\
&= 1 \cdot 4 - 2 \cdot 3 \\
&= -2
\end{align}

Multiple environments working together.
.
