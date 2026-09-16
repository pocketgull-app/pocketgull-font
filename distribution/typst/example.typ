#import "lib.typ": *

#show: pocketgull-math-rules.with(
  font-size: 11pt,
  slashed-zero: true,
  curved-l: true,
  serifed-I: true,
  dark-mode: false,
)

= Clinical Deep Learning & Metaplasticity Modeling

== Asymmetric Focal Loss Formulation
In life-critical medical imaging under high label skew, we optimize the network via #lasl:

$ lasl = - sum_(k=1)^K [ y_k (1 - p_k)^(gamma_+) log(p_k) + (1 - y_k) (p_(m,k))^(gamma_-) log(1 - p_(m,k)) ] $

where $gamma_+ = 1.0$ dampens false negative penalties and $gamma_- = 5.0$ penalizes trivial background activations.

== Pharmacokinetic Bolus Decay
The systemic drug concentration #cp($t$) conforms to:

$ cp(t) = [ (D dot k_a) / (V_d dot (k_a - k_e)) ] ( e^(-k_e t) - e^(-k_a t) ) $

== Probability & Measure Spaces
For any random variable $X$ over $rset$:

$ forall x in rset, quad bb(P)(X <= x) = integral_(-infinity)^x f_X(u) dif u $
