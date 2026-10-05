# Emerging Technology Creation Agent

This specialist explains how an emerging technology arose, which predecessor capabilities and enabling conditions made it possible, and what that history implies for a specific application and organization. It preserves the frozen common intake and output contracts and keeps creation analysis separate from final adoption approval.

## Package contents

- `specialist_instructions.md` contains the final version 0.2 reasoning and evidence rules.
- `cases/` contains the primary financial-services case and two context contrasts.
- `prompts/` preserves the weak primary prompt and the three final prompt packets used for testing.
- `responses/` contains the preserved weak response and the three validated final responses.
- `records/agent_record.md` records the conclusion, tests, failure, revision, boundary, handoff, and self-reflection.

## Reproduce the primary run

```bash
python3 tools/build_prompt.py \
  --agent agents/creation_agent \
  --case agents/creation_agent/cases/primary.json

python3 tools/validate_response.py \
  agents/creation_agent/responses/primary_response.json
```

The agent may recommend research, prototyping, or a bounded pilot from the creation-history perspective. It must hand off diffusion, adoption readiness, implementation architecture, compliance, security approval, and production risk acceptance to the appropriate specialists and accountable human owners.
