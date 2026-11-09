# Lab7 Organizational Adoption Agent

Version 1.0 is an individual candidate, not a team release or real company approval.

Build a prompt with the original frozen tool:

    python3 tools/build_prompt.py --agent agents/organizational_adoption_agent --case agents/organizational_adoption_agent/cases/primary.json --out work/lab7_primary.txt

Paste the complete prompt into an interactive LLM, save JSON only, then use tools/validate_response.py on the saved response. No API account/key is required. The included examples are same-assistant qualitative reasoning, not independently sampled inference runs.

Recheck the delivered evidence and saved examples:

    python3 verification/recheck.py

This script does not invoke a model or deploy a chart tool. It verifies the supplied schema keywords, original bytes, exact prompt rebuilding, case relations, declared readiness judgments and arithmetic. The controlled weak examples remain separate from the final responses. Four readiness labels are conveyed within the existing output strings; no frozen schema is changed.
