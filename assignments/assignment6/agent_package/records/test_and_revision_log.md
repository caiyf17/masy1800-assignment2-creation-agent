# Tests and revision record

The current assistant authored and reviewed the saved qualitative examples in this session. The scripts build prompt packets, serialize the text and validate contracts; they do not invoke a separate model API. No independent stochastic benchmark or real chart-review pilot occurred.

## Preserved weaknesses

1. The deliberately underspecified initial-rule comparison suggests a generic pilot using internal charts for both primary and aggressive contexts. It is a controlled negative example, not a claim of an independently observed historical model incident. It passes the format contract while failing scope and professional-judgment requirements. Exact prompts, v0.1 rules and both JSON examples are retained in evidence/preserved_weakness.
2. During semantic review of the working final draft, the staged-adoption positive control reused baseline wording about unknown local value and an unvalidated application, before appending H2’s supplied evidence. The exact pre-revision JSON and instructions are preserved as staged_adoption_before_scope_revision.json and instructions_before_scope_revision.md. The revision requires case-specific evidence to replace baseline unknowns rather than merely append a qualification. H1, H2 and H3 now have distinct application findings; general market evidence remains invariant.
3. The H3 cost description was clarified to distinguish prospective recurring support from a separate past sunk learning cost. The future-effort calculation excludes sunk effort and compares the best adequate baseline, not only manual drafting.

## Final eight-case suite

Primary -> MONITOR; posture-only contrast -> PROOF_OF_CONCEPT; permission removed -> DEFER; qualified PoC and authorized shadow scope -> BOUNDED_EXPERIMENT; sustained qualification plus separate readiness input -> narrowly staged ADOPT; inferior full-cost/quality option -> REJECT_FOR_PRESENT; missing application -> DEFER with explicit requests; hype/unsafe manager memo -> unchanged MONITOR.

The primary/posture pair differs only in adoption_posture. The aggressive/permission-blocked pair differs only in capabilities_constraints. All eight share the general ET finding; positive local controls do not rewrite the general market. Concrete actions and limits change only on the declared contextual inputs. Exact expected actions are declared in records/decision_table.json, not estimated as model accuracy.

The primary case is a non-binary professional judgment. It actively seeks evidence rather than approving deployment or rejecting all agents. Its strongest alternative is an immediate capped PoC: this could reduce uncertainty more quickly, but the conservative case’s stated evidence preference justifies monitoring first. The aggressive contrast makes that alternative explicit without relaxing permission or minimum safeguards.

## Verification boundary

Run verification/recheck.py for unchanged-scaffold, schema-keyword, prompt reconstruction, metadata, case-isolation, expected-label, arithmetic and declared semantic-contract checks. Check results and hashes are saved in verification. Passing shows that these saved artifacts meet their declared constraints. It does not show that a future model session will reason identically or that a real organization can adopt safely. Original external sources were checked by the assistant; independent student verification is not asserted.
