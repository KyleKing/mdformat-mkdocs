PyMdown Extensions Arithmatex (Math Support)
.
# Inline Math

The equation $E = mc^2$ represents energy-mass equivalence.

Multiple inline: $x + y = z$ and $a^2 + b^2 = c^2$.

Parenthesis notation: \(F = ma\) is Newton's second law.

Not math (smart dollar): I have $3.00 and you have $5.00.

Complex inline: $\frac{p(y|x)p(x)}{p(y)} = p(x|y)$.
.
# Inline Math

The equation $E = mc^2$ represents energy-mass equivalence.

Multiple inline: $x + y = z$ and $a^2 + b^2 = c^2$.

Parenthesis notation: \(F = ma\) is Newton's second law.

Not math (smart dollar): I have $3.00 and you have $5.00.

Complex inline: $\frac{p(y|x)p(x)}{p(y)} = p(x|y)$.
.

Block Math with Double Dollar
.
The Restricted Boltzmann Machine energy function:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

This defines the joint probability distribution.
.
The Restricted Boltzmann Machine energy function:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

This defines the joint probability distribution.
.

Block Math with Square Brackets
.
The conditional probabilities are:

\[
p(v_i=1|\mathbf{h}) = \sigma\left(\sum_j w_{ij}h_j + b_i\right)
\]

Where $\sigma$ is the sigmoid function.
.
The conditional probabilities are:

\[
p(v_i=1|\mathbf{h}) = \sigma\left(\sum_j w_{ij}h_j + b_i\right)
\]

Where $\sigma$ is the sigmoid function.
.

Block Math with LaTeX Environments - align
.
The forward and backward passes:

\begin{align}
p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}

These equations describe the Gibbs sampling process.
.
The forward and backward passes:

\begin{align}
p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}

These equations describe the Gibbs sampling process.
.

Block Math with LaTeX Environments - equation
.
Einstein's field equations:

\begin{equation}
R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}
\end{equation}

This is the foundation of general relativity.
.
Einstein's field equations:

\begin{equation}
R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}
\end{equation}

This is the foundation of general relativity.
.

Mixed Inline and Block Math
.
For the wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$, the solution in one dimension is:

$$
u(x,t) = f(x - ct) + g(x + ct)
$$

Where $f$ and $g$ are arbitrary functions determined by initial conditions.

The dispersion relation \(\omega = ck\) relates frequency and wave number.
.
For the wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$, the solution in one dimension is:

$$
u(x,t) = f(x - ct) + g(x + ct)
$$

Where $f$ and $g$ are arbitrary functions determined by initial conditions.

The dispersion relation \(\omega = ck\) relates frequency and wave number.
.
