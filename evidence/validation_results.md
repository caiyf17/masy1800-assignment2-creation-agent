# Validation Results

Validation date: 2026-10-05.

## Frozen core integrity

Command:

```text
python3 tools/check_frozen_core.py
```

Result: `FROZEN CORE INTACT`

## Response contract validation

Command pattern:

```text
python3 tools/validate_response.py <response-file>
```

Results:

- `primary_response_v0_1_weak.json`: `VALIDATION PASSED`
- `primary_response.json`: `VALIDATION PASSED`
- `contrast_1_response.json`: `VALIDATION PASSED`
- `contrast_2_response.json`: `VALIDATION PASSED`

The weak baseline passing validation is part of the preserved failure: structural validity did not establish analytical quality.

## Input and output field audit

All three case files contain every field required by `core/input_schema.json`. All four preserved response files contain every required field in `core/output_schema.json`, and no response introduces an unapproved top-level field. Creation-specific content is mapped into the frozen common contract.

## Context stability check

The final `general_et_finding` string is identical in the primary and both contrast responses. All three have SHA-256 digest:

```text
ee084c35068e302285167a154321d9abab809e3fba121616d3e59ef26590e370
```

Application, organization, value, risk, recommendation, monitoring, and abstention fields were reviewed and differ in ways traceable to the supplied case context.

## Submission document quality assurance

The final Agent Record was rendered and visually inspected page by page. The four-page document has no clipped body text, split data rows, or unresolved placeholders. Structural audits found one portrait Letter section, six Heading 1 paragraphs, no embedded images, no Word fields, no footnote/endnote references, no content controls, no comments, and no tracked changes. The accessibility audit reported no findings. The source template's package structure was preserved; only `docProps/core.xml`, `word/document.xml`, and `word/footer1.xml` changed. The source template retained SHA-256 `5275ea28e66a27d5ddfae3c0541ce7cf7711655a450da7eecb4d36b0ced7e802`, confirming that it was not overwritten. The final record has SHA-256 `5fdaae7e227228ee749ca19f565a78eee621fde01a50fdebd38beeac26d52531`.
