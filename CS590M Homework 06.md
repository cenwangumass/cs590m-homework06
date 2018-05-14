% CS590M Homework 06
% Cen Wang

# Telephone System

## Specification

**$S$**

$X(t) = (Z_1(t), ..., Z_N(t))$ such that:

$Z_i(t) \in \{0, 1, 2, ..., K\}$ and if $Z_i(t) = k, k \ne 0$ there must exist $j, (i \ne j)$ such that $Z_j(t) = k$. // i and j are calling over link k

**$E$**

Given in the problem.

**$E(s)$**

For $1 \le i \le N$, $e_i \in E(s)$ if $Z_i = 0$ // If someone is not calling, he can place a call

For $1 \le k \le K$, $e_{N + k} \in E(s)$ if $k$ appears in $Z_1$, ... $Z_2$ // Started phone call will end

**$p(s'; s, e ^ *)$**

For $e_i (1 \le i \le N)$

Select $j$ from $\{1, 2, ..., i - 1, i + 1, ..., N\}$ randomly. If $Z_j \ne 0$ (busy) or the number of nonzeros $n / 2$ = number of links, then $p(s'; s, e_i) = 1$ where $s' = s$ // Call is lost, state does not change

Otherwise, $s = (..., Z_i, ..., Z_j), s' = (..., Z_i', ..., Z_j'), Z_i = Z_j = 0, Z_i = Z_j = k$, $p(s', s, e_i) = 1$ // i and j call over link k

For $1 \le k \le K$, $s = (..., Z_i, ..., Z_j), s' = (..., Z_i', ..., Z_j'), Z_i = Z_j = k, Z_i = Z_j = 0$, $p(s', s, e_{N + k}) = 1$ // Call end

**$F(x; s', e', s, e ^ *)$**

For $e_i$ where $1 \le i \le N, F = \exp(6)$

For $e_{N + k}$ where $1 \le k \le K, F = Uniform(0, 6)$

**$r(s, e) = 1$**

**Initial distribution**

$X(t) = (Z_1(t), ..., Z_N(t)) = (0, ..., 0)$

## Result

### Interquartile range

- Point estimation: 6.994930234229773
- Confidence interval: $[5.834533187692992, 8.155327280766553]$

### Long-run fraction of time

- Point estimation: 0.23446493395742463
- Confidence interval: $[0.2113806271497106, 0.2575492407651387]$

When $s = (0, ..., 0)$, there are only exponential clocks running. By memoryless property, it is regenerative.

### Standard deviation

- Point estimation: 5.584567462807249
- Confidence interval: [4.950303702103369, 6.218831223511129]

$$
n = \frac{s ^ 2 z_{\delta} ^ 2}{\epsilon ^ 2 \mu ^ 2} = 2229
$$

### Selection

Using Dudewicz and Dalal, we have $[3.894624914547033, 5.081568500570215, 4.2775402776803695]$ for the three systems. So, the best one is the second with rate 0.20.

# Squared Coefficient of Correlation

## Taylor-Series

First, express $Corr[U, V] ^ 2$ in terms of means:

$$
Corr[U, V] ^ 2 = \frac{Cov[U, V] ^ 2}{Var[U]Var[V]} = \frac{(E[UV] - E[U]E[V]) ^ 2}{(E[U ^ 2] - E[U] ^ 2)(E[V ^ 2] - E[V] ^ 2)}
$$

Thus,

$$
g(\mu_1, \mu_2, \mu_3, \mu_4, \mu_5) = \frac{(\mu_5 - \mu_1 \mu_2) ^ 2}{(\mu_3 - \mu_1 ^ 2)(\mu_4 - \mu_2 ^ 2)}
$$

Define $a = \mu_5 - \mu_1 \mu_2, b = \mu_3 - \mu_1 ^ 2, c = \mu_4 - \mu_2 ^ 2$

$$
\frac{\partial g}{\partial \mu_1} = \frac{2 a}{b ^ 2 c}(a \mu_1 - b \mu_2)
$$

$$
\frac{\partial g}{\partial \mu_2} = \frac{2 a}{b c ^ 2} (a \mu_2 - c \mu_1)
$$

$$
\frac{\partial g}{\partial \mu_3} = - \frac{a ^ 2}{b ^ 2 c}
$$

$$
\frac{\partial g}{\partial \mu_4} = - \frac{a ^ 2}{b c ^ 2}
$$

$$
\frac{\partial g}{\partial \mu_5} = \frac{2 a}{b c}
$$

From the data we have:

| #  | $U$  | $V$  | $U ^ 2$ | $V ^ 2$ | $UV$ |
|----|------|------|---------|---------|------|
| 1  | 12   | 20   | 144     | 400     | 240  |
| 2  | 18   | 38   | 324     | 1444    | 684  |
| 3  | 15   | 29   | 225     | 841     | 435  |
| 4  | 35   | 55   | 1225    | 3025    | 1925 |
| 5  | 8    | 12   | 64      | 144     | 96   |
| 6  | 16   | 36   | 256     | 1296    | 576  |
| 7  | 2    | 10   | 4       | 100     | 20   |
| 8  | 12   | 47   | 144     | 2209    | 564  |
| 9  | 20   | 40   | 400     | 1600    | 800  |
| 10 | 6    | 10   | 36      | 100     | 60   |

$\mu_1 = 14.4, \mu_2 = 29.7, \mu_3 = 282.2, \mu_4 = 1115.9, \mu_5 = 540$

$a = 112.32, b = 74.84, c = 233.81$

Using the partial derivatives, we have: $c_n = -0.103837882513965, d_n = -0.00169991849822015, e_n = -0.00963348776222338, f_n = -0.00308357308979426, g_n = 0.0128377888911111$

$\alpha_n = g(\mu_1, \mu_2, \mu_3, \mu_4, \mu_5) = 0.720970224124797$

$s_n ^ 2 = (n - 1) ^ {-1} \sum_{i = 1}^{n} (c_n (U_i - \mu_1) + d_n (V_i - \mu_2) + e_n (U_i ^ 2 - \mu_3) + f_n (V_i ^ 2 - \mu_4) + g_n (UV_i - \mu_5)) ^ 2= \frac{1}{9} * 2.977116137 = 0.3307906819$

Point estimate: 0.720970224124797, confidence interval: $[0.36449879710880473, 1.0774416511407894]$.

## Jackknife

$\alpha_n = g(\mu_1, \mu_2, \mu_3, \mu_4, \mu_5) = 0.7209702241247972$

| #  | $a_n ^ i$    | $a_n(i)$     |
|----|--------------|--------------|
| 1  | 0.7265683558 | 0.6705870388 |
| 2  | 0.7157307483 | 0.7681255064 |
| 3  | 0.7221234634 | 0.7105910709 |
| 4  | 0.657221508  | 1.29470867   |
| 5  | 0.7111167599 | 0.8096514022 |
| 6  | 0.7229964256 | 0.702734411  |
| 7  | 0.6587694594 | 1.280777107  |
| 8  | 0.9188361171 | -1.059822813 |
| 9  | 0.7080416598 | 0.8373273031 |
| 10 | 0.6906202005 | 0.9941204369 |

$\alpha_n ^ J = 0.7008800132932412$

$v_n^J = 0.4345515490717894$

Point estimate: 0.7008800132932412, confidence interval: $[0.2923078799767213, 1.109452146609761]$.

# Multiple Performance Measures

The expected number of CIs that do not bracket the true value:

Define $A_i$ = ith confidence interval brackets the true value of the ith performance measure and 

$$
I(A_i) = 
\begin{cases} 
1 & \text{if $A_i$ does not happened} \\
0 & \text{otherwise}
\end{cases}
$$

$$
\begin{aligned}
E[N] & = E[I(A_1) + I(A_2) + ... + I(A_k)] \\
     & = E[I(A_1)] + E[I(A_2)] + ... + E[I(A_k)] \\
     & = k \alpha
\end{aligned}
$$

Bonferroni's inequality:

$$
P(\cap_n A_n) \ge 1 - \sum_n P(A_n ^ c)
$$

$$
1 - (k \alpha ^ *) \ge 1 - \alpha
$$

So, $\alpha ^ * \le \frac{\alpha}{k}$.

# Regenerative Method

First cycle:

$$
E \Big[ \int_0^{\infty} e ^ {- \beta u} q(X(u)) du \Big] = E \Big[ \int_0^{T_1} e ^ {- \beta u} q(X(u)) du \Big] + E[e ^ {- \beta T_1}] E \Big[ \int_{T_1}^{\infty} e ^ {- \beta (u - T_1)} q(X(u)) du \Big]
$$

$$
r = E \Big[ \int_0^{T_1} e ^ {- \beta u} q(X(u)) du \Big] + E[e ^ {- \beta T_1}] r
$$

$$
r = \frac{E \Big[ \int_0^{T_1} e ^ {- \beta u} q(X(u)) du \Big]}{1 - E[e ^ {- \beta T_1}]} = \frac{E \Big[ \int_0^{T_1} e ^ {- \beta u} q(X(u)) du \Big]}{E[1 - e ^ {- \beta T_1}]}
$$

$$X = \int_0^{T_1} e ^ {- \beta u} q(X(u)) du$$

$$Y = 1 - e ^ {- \beta T_1}$$

i-th cycle:

Similarly, 

$$X = \int_{T_{i - 1}}^{T_i} e ^ {- \beta (u - T_{i - 1})} q(X(u)) du$$

$$Y = 1 - e ^ {- \beta (T_{i} - T_{i - 1})}$$

# Control Variates

## m = 2 or m = 3

When $m = 2$, we have

$$
X_c = X - a_1 C_1 - a_2 C_2
$$

$$
Var(X_c) = Var(X) + a_1^2 Var(C_1) + a_2^2 Var(C_2) - 2 (a_1 Cov(X, C_1) + a_2 Cov(X, C_2)) + 2 a_1 a_2 Cov(C_1, C_2)
$$

$$
\frac{\partial Var(X_c)}{\partial a_1} = 2 a_1 Var(C_1) + 2 a_2 Cov(C_1, C_2) - 2 Cov(X, C_1)
$$

$$
\frac{\partial Var(X_c)}{\partial a_2} = 2 a_1 Cov(C_1, C_2) + 2 a_2 Var(C_2) - 2 Cov(X, C_2)
$$

Set both $\frac{\partial Var(X_c)}{\partial a_1}$ and $\frac{\partial Var(X_c)}{\partial a_2}$ to 0 and we can solve a linear equation of $a_1$ and $a_2$.

Finally, we have:

$$
a_1 = \frac{Cov(C_1, C_2) Cov(X, C_2) - Cov(X, C_1) Var(C_2)}{Cov(C_1, C_2)^{2} - Var(C_1) Var(C_2)}
$$

$$
a_2 = \frac{Cov(C_1, C_2) Cov(X, C_1) - Cov(X, C_2) Var(C_1)}{Cov(C_1, C_2)^{2} - Var(C_1) Var(C_2)}
$$

When $m = 3$, we have

$$
X_c = X - a_1 C_1 - a_2 C_2 - a_3 C_3
$$

$$
Var(X_c) = Var(X) + a_1^2 Var(C_1) + a_2^2 Var(C_2) + a_3^2 Var(C_3) - 2 (a_1 Cov(X, C_1) + a_2 Cov(X, C_2) + a_3 Cov(X, C_3)) + 2 a_1 a_2 Cov(C_1, C_2) + 2 a_1 a_3 Cov(C_1, C_3) + 2 a_2 a_3 Cov(C_2, C_3)
$$

$$
\frac{\partial Var(X_c)}{\partial a_1} = 2 a_1 Var(C_1) + 2 a_2 Cov(C_1, C_2) + 2 a_3 Cov(C_1, C_3) - 2 Cov(X, C_1)
$$

$$
\frac{\partial Var(X_c)}{\partial a_2} = 2 a_1 Cov(C_1, C_2) + 2 a_2 Var(C_2) + 2 a_3 Cov(C_2, C_3) - 2 Cov(X, C_2)
$$

$$
\frac{\partial Var(X_c)}{\partial a_3} = 2 a_1 Cov(C_1, C_3) + 2 a_2 Cov(C_2, C_3) + 2 a_3 Var(C_3) - 2 Cov(X, C_3)
$$

Set all three to 0. Finally, we have:

$\alpha = C_1C_2^{2} VC_3 + C_1C_3^{2} VC_2 + C_2C_3^{2} VC_1 - VC_1 VC_2 VC_3 - 2 C_1C_2 C_1C_3 C_2C_3$

$\beta_1 = XC_1 (C_2C_3^{2} - VC_2 VC_3) + XC_2 (C_1C_2 VC_3 - C_1C_3 C_2C_3) + XC_3 (C_1C_3 VC_2 - C_1C_2 C_2C_3)$

$\beta_2 = XC_1 (C_1C_2 VC_3 - C_1C_3 C_2C_3) + XC_2 (C_1C_3^{2} - VC_1 VC_3) + XC_3 (C_2C_3 VC_1 - C_1C_2 C_1C_3)$

$\beta_3 = XC_1 (C_1C_3 VC_2 - C_1C_2 C_2C_3) + XC_2 (C_2C_3 VC_1 - C_1C_2 C_1C_3) + XC_3 (C_1C_2^{2} - VC_1 VC_2)$

$$
a_1 = \frac{\beta_1}{\alpha}
$$

$$
a_2 = \frac{\beta_2}{\alpha}
$$

$$
a_3 = \frac{\beta_3}{\alpha}
$$

## Uncorrelated control variates

This means $Cov(C_1, C_2) = Cov(C_2, C_3) = Cov(C_1, C_3) = 0$. So the result can be simplified to:

$$
a_i = \frac{Cov(X, C_i)}{Var(C_i)}, i \in {1, 2, 3, ..., m}
$$

## Estimation

The covariance between two variable $C_1$ and $C_2$ can be estimated by:

$$
Cov(C_1, C_2) = \frac{\sum_{j = 1}^n (C_{1, i} - \bar{C_1}) (C_{2, i} - \bar{C_2})}{n - 1}
$$

Variance of $X$ can be estimated by:

$$
\frac{1}{n - 1} \sum_{i = 1}^{n} (X_i - \bar{X_i}) ^ 2
$$

Similarly, we can estimate all the coefficients $Cov(C_i, C_j)$, $Cov(X, C_i)$ and $Var(C_i)$

We then plug in all the estimation into the original equations that are derived in the previous section.

Yes. In both situations, the estimators can be improved.

# Reducing Streams

Using common random number, we can use stream 1 for the times between successive demands, stream 2 for the sizes of those demands, and stream 3 for the delivery lag when an order is placed to the supplier. After one replication is done, instead of throwing away the entire stream, we can switch to the next substream.
