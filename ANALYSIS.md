# The Bass Theorem: analysis of `HingeRotation.lean`

Every claim below marked **proved** is a Lean theorem that builds with no `sorry`. Each one
depends only on the standard axioms `propext`, `Classical.choice`, `Quot.sound`.

## 1. Your file, as uploaded

`Ramtastic/Bass/HingeRotation.lean` is a byte-for-byte copy of your upload. It builds
unchanged against Lean 4.28.0 / Mathlib, with no warnings. It contains what the write-up says:
the `Hinge` structure, `rotate`, `rotate_zero`, `rotate_add`, `rotate_pi`, `rotate_halfPi`,
`rotate_twoPi` and `hinge_fourth_power`. That is 8 declarations, none using `sorry`.

Small remarks:
* "Zero axioms" in the header means "no custom axioms". Like any Mathlib proof, these proofs
  use the three standard axioms.
* The file contains no Clifford algebra, inner product or spinor module. So parts (i) and (ii)
  of the Bass Theorem are not proved in it. Section 3 below proves them.

## 2. The header claims that the file does not prove (`Ramtastic/Bass/HingeAnalysis.lean`)

Your header says "Every element of this group preserves any inner product that J preserves.
The orbit of any vector under this group is a circle." Neither statement appears in the file.
Both are now **proved**:

| Claim | Lean name |
|---|---|
| If `J` preserves `⟪·,·⟫`, then `J` is skew-adjoint (because `J² = -id`), and conversely | `skew_of_isometry`, `isometry_of_skew` |
| Every `R(θ)` preserves that inner product, and hence the norm | `rotate_inner`, `norm_rotate` |
| `x ⊥ Jx` and `‖Jx‖ = ‖x‖` | `inner_self_J`, `norm_J` |
| The orbit `{R(θ)x}` is exactly `{a x + b Jx : a² + b² = 1}`, a circle | `orbit_eq_circle` |
| The orbit lies on the sphere of radius `‖x‖` | `orbit_on_sphere` |
| `R(θ + 2π) = R(θ)`, `R(-θ)R(θ) = id`, rotations commute, `J` commutes with each `R(θ)` | `rotate_periodic`, `rotate_neg_comp`, `rotate_comm`, `J_comp_rotate` |

## 3. Parts (i) and (ii) in your vocabulary (`Ramtastic/Bass/CliffordBridge.lean`)

Here `Cl(V, Q)` uses `Q v = -⟪v, v⟫`, and a spinor module is a Clifford action with every
vector acting skew-adjointly (see `RequestProject/Bass/Clifford.lean`). The theorem
`Ramtastic.Bass.bass_theorem` produces values of your own `Hinge` structure. It is **proved**:

* (i) For unit `v`: `c(v) ∘ c(v) = -id`, `rotate (c(v)) (π/2) = c(v)`, and every `R_v(θ)`
  preserves the inner product.
* (ii) For orthonormal `v, w`: `(c(v)c(w)) ∘ (c(v)c(w)) = -id`,
  `rotate (c(v)c(w)) (π/2) = c(v)c(w)`, and every `R_{vw}(θ)` preserves the inner product.

**Caveat on "the quarter-turn".** `c(v)c(w) = R_{vw}(π/2)` holds by definition: it is
`rotate_halfPi` applied to the plane Hinge. What `R_{vw}(θ)` does to the vectors of the plane
is a separate question. **Proved** (`planeHinge_conj_cv`):

\[ R_{vw}(\theta)\, c(v)\, R_{vw}(-\theta) = \cos 2\theta\; c(v) + \sin 2\theta\; c(w). \]

So `R_{vw}(θ)` rotates the `(v,w)`-plane by the **double** angle `2θ`. This is the spin
double cover. On vectors, `c(v)c(w) = R_{vw}(π/2)` is the half-turn `c(v) ↦ -c(v)`, not a
quarter-turn. It is a quarter-turn of the spinor circle, which is a different thing.

## 4. The table "What the Hinge gives you"

| Row | Verdict |
|---|---|
| Self-adjointness: "skew × skew = self-adjoint" | **False in general.** `(AB)* = B*A* = BA`, which equals `AB` only when `A` and `B` commute. **Proved** counterexample with 3×3 skew matrices (`skew_mul_skew_not_selfAdjoint`). In the spinor setting, `c(v)²` is self-adjoint (`cv_sq_selfAdjoint`). For orthogonal `v, w`, `c(v)c(w)` is *skew*-adjoint (`cvw_skewAdjoint`), and that is exactly what makes it an isometric Hinge. |
| Positivity: `⟪c(v)ψ, c(v)ψ⟫ = ⟪v,v⟫⟪ψ,ψ⟫` | **Correct, proved** (`inner_cv_cv`). |
| Norm preservation | **Correct, proved** (`rotate_inner`, `bass_theorem`). |

## 5. "Why the minus sign": a precise version

**Proved** (`positive_convention_trivial`). Use the *positive* convention `v² = +⟪v,v⟫`, and
require every vector to act skew-adjointly on a real inner product space `S`. Then a single
nonzero `v` forces `S = 0`. The reason: `0 ≤ ⟪c(v)x, c(v)x⟫ = -⟪x, c(v)²x⟫ = -‖v‖²‖x‖²`.
So, once you require skew-adjointness and a positive-definite spinor inner product, the
minus sign is forced. This is the precise sense in which "Convention B is not a choice".
Without those two requirements, both signs give legitimate Clifford algebras.

**Proved** (`boost_add`, `boost_eq_id_iff`). With `K² = +id`, the family
`B(θ) = cosh θ + sinh θ K` is still a one-parameter group. But if `K` is not a multiple of the
identity, `B(θ) = id` only at `θ = 0`. The hyperbola never comes back, unlike `R(2π) = id`.

## 6. The Cayley–Dickson section

* **Proved:** `Cl(ℝ, -x²) ≃ ℂ` (`cliffordEquivComplex`) and `Cl(ℝ², -‖x‖²) ≃ ℍ`
  (`cliffordEquivQuaternion`). So the first two rungs match, *counting generators*.
* After that the pattern breaks:
  - `Cl(ℝ³, -‖x‖²) ≅ ℍ ⊕ ℍ` (dimension 8), not `𝕆`.
  - Every Clifford algebra is associative. The octonions are not, so they are not a Clifford
    algebra, nor a rung of this construction.
  - The write-up's labels mix two numbers. ℂ, ℍ, 𝕆, 𝕊 have dimensions 2, 4, 8, 16, and arise
    from 1, 2, 3, 4 doublings. They do not come from "v² = -1 at dimension 1, 2, 4, 8".
  - Hurwitz's theorem concerns algebra dimensions 1, 2, 4, 8 (ℝ, ℂ, ℍ, 𝕆). The sedenions
    (dimension 16) are where zero divisors appear.

  These points are standard facts. They are not formalized here beyond the two equivalences.
* Pólya's recurrence theorem is about simple random walks on the lattice `ℤ^d`. It has no
  formal link to the Hinge results, and "a sphere is a 2D surface" does not make walks on
  spheres recurrent in Pólya's sense. Not formalized.

## 7. The architectural corollary

"Every property follows from the geometry of the circle without additional analytical
machinery" is not a mathematical statement, so it cannot be proved or refuted as written.
What is true and proved: for a *fixed* spinor module, positivity, norm preservation and the
rotation group law are finite algebraic consequences of `J² = -1` plus skew-adjointness.
What does not follow is self-adjointness of *unbounded* operators such as Dirac operators on
manifolds. Those need domains and analysis. Also, section 4 shows that the self-adjointness
row of the table is false as stated.
