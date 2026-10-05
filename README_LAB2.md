# MASY1-GC 1800 Assignment 2 Creation Agent

This working copy contains Yufei Cai's Emerging Technology Creation Agent for Agentic AI. It preserves the frozen course core and adds only the specialist package, evidence, tests, and submission record required for Assignment 2.

## Main deliverables

- `agents/creation_agent/specialist_instructions.md` - final version 0.2 specialist logic.
- `agents/creation_agent/cases/` - primary and two context-contrast cases.
- `agents/creation_agent/prompts/` - preserved prompt packets for the weak baseline and final runs.
- `agents/creation_agent/responses/` - weak baseline, final primary response, and two final contrast responses.
- `agents/creation_agent/records/agent_record.md` - concise agent record, including the self-reflection.
- `evidence/source_register.md` - dated evidence register with claim boundaries.
- `evidence/failure_and_revision_record.md` - preserved weakness and revision decision.
- `evidence/context_contrast_analysis.md` - stable-versus-changed comparison.
- `evidence/validation_results.md` - frozen-core and response-validation record.
- `deliverables/Cai_Yufei_Assignment2_Creation_Agent_Record.docx` - final submission-facing Agent Record.

## Reproduce the checks

```bash
python3 tools/check_frozen_core.py
python3 tools/build_prompt.py --agent agents/creation_agent --case agents/creation_agent/cases/primary.json
python3 tools/validate_response.py agents/creation_agent/responses/primary_response.json
python3 tools/validate_response.py agents/creation_agent/responses/contrast_1_response.json
python3 tools/validate_response.py agents/creation_agent/responses/contrast_2_response.json
```

The scaffold does not call the OpenAI API. Prompt packets are designed for ChatGPT, and returned JSON is stored and validated locally.
