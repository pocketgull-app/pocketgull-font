// Typst library for PocketGull Math
// Humanist Clinical Sans-Serif Mathematics

#let pocketgull-math-rules(
  body,
  font-size: 11pt,
  slashed-zero: true,
  curved-l: true,
  serifed-I: true,
  dark-mode: false,
) = {
  let features = ()
  if slashed-zero { features.push("cv08") }
  if curved-l { features.push("cv05") }
  if serifed-I { features.push("ss02") }

  let bg-color = if dark-mode { rgb("#09090b") } else { rgb("#ffffff") }
  let fg-color = if dark-mode { rgb("#f4f4f5") } else { rgb("#09090b") }

  set page(fill: bg-color)
  set text(
    font: ("PocketGull Math", "PocketGull", "Atkinson Hyperlegible", "sans-serif"),
    size: font-size,
    fill: fg-color,
    features: features,
  )

  // Math equations styling
  show math.equation: set text(
    font: ("PocketGull Math", "New Computer Modern Math"),
    features: features,
  )

  body
}

// Math shortcut macros for Clinical and ML workflows
#let lasl = $cal(L)_"ASL"$
#let egfr = $"eGFR"$
#let auc = $"AUC"$
#let cp(t) = $C_p (#t)$
#let rset = $bb(R)$
#let nset = $bb(N)$
#let zset = $bb(Z)$
#let cset = $bb(C)$
#let qset = $bb(Q)$
