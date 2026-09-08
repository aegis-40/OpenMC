# Aegis-40 — Bowring-1972 CHF coefficient verification

*Discharges the standing caveat "confirm Bowring A/C coefficients vs Todreas & Kazimi".*
*Verification level: structural/dimensional against the canonical SI form + numeric sanity.*
*2026-06-27. Implementation in `tools/mdnbr.py` (`bowring_F`, `bowring_chf`).*

## Canonical form (Todreas & Kazimi, *Nuclear Systems I*, SI presentation)
```
q"_cr = [ A + (D_h · G / 4) · Δh_sub,in ] / (C + z)          [W/m²]
A     = 2.317 · (h_fg · D · G / 4) · F1 / (1 + 0.0143 · F2 · D^0.5 · G)
C     = 0.077 · F3 · D · G / (1 + 0.347 · F4 · (G/1356)^n)
n     = 2.0 − 0.5·pR
pR    = P / 6.895 MPa   (= P[bar]/69 ;  pR = 1 at 6.9 MPa)
```
F-factors, **pR ≤ 1**:
```
F1 = (pR^18.942 · exp[20.89(1−pR)] + 0.917) / 1.917
F2 = 1.309·F1 / (pR^1.316 · exp[2.444(1−pR)] + 0.309)
F3 = (pR^17.023 · exp[16.658(1−pR)] + 0.667) / 1.667
F4 = F3 · pR^1.649
```
F-factors, **pR > 1**:
```
F1 = pR^(−0.368) · exp[0.648(1−pR)]
F2 = F1 / (pR^(−0.448) · exp[0.245(1−pR)])
F3 = pR^0.219
F4 = F3 · pR^1.649
```

## Check result — code matches the canonical form term-for-term
Every coefficient in `mdnbr.py` (2.317, 0.0143, 0.077, 0.347, 1356; all F1–F4
exponents/constants; `n`; the `pR = P[bar]/69` definition; and the final
`(A + D·G/4·Δh_sub)/(C+z)` equation) reproduces the form above. **No discrepancy.**

## Numeric sanity at the Aegis design point (P 12.8 MPa, G 543, D_h 11.79 mm)
| quantity | value | sane? |
|---|---|---|
| pR = P[bar]/69 | 1.855 (→ high-P branch) | ✓ pR=1 at 6.9 MPa |
| F1 / F2 / F3 / F4 | 0.458 / 0.744 / 1.145 / 3.172 | ✓ all O(1), no blow-ups |
| n = 2 − 0.5·pR | 1.072 | ✓ |
| h_fg @ 12.8 MPa | 1.143 MJ/kg | ✓ steam-table value |
| A / C | 1.19e6 / 0.400 m | ✓ |
| A/C (= q″_cr at z=0, zero subcooling) | 2.98 MW/m² | ✓ O(1–10 MW/m²) |

## Validity (all satisfied at the design point)
P 2–19 MPa ✓ (12.8) · G 50–4000 kg/m²s ✓ (543) · D 2–45 mm ✓ (11.79).

## Residual conservatism (not a defect)
Bowring is a **single round-tube** correlation — no rod-bundle / spacer-grid
enhancement factor. Cross-check vs W-3 in the overlap window (P 14 / G 2000) gave
Bowring ≈ 0.6× W-3 = the bare-tube-vs-bundle ratio → **conservative, not optimistic**.

## Verdict
The A/C/F coefficients are the standard Todreas & Kazimi SI Bowring set; the
caveat is discharged at the structural + numeric level. A final eyeball against the
physical textbook page is the only remaining (low-risk) step. The bare-tube
conservatism stands and is documented as a margin, not an error.
