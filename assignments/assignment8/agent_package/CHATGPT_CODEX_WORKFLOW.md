# ChatGPT + Codex Reference Workflow

ChatGPT is the required course AI environment. Codex is the supported coding/development path.

- Give ChatGPT/Codex the weekly assignment memo and relevant scaffold files.
- Ask Codex to inspect before editing and to preserve FROZEN CORE.
- Use Codex to help specialize `specialist_instructions.md`, edit case JSON, explain local scripts, and diagnose errors.
- Use `tools/build_prompt.py` to create a prompt packet.
- Run that packet in ChatGPT. Save the JSON result locally.
- Use `tools/validate_response.py` to check the contract.
- Test contrasting cases, revise the specialist logic, then commit the final candidate.

The reference scaffold does not call the OpenAI API and does not require an API key.
