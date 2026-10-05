# START HERE

## Before the first specialist assignment

1. Download the frozen ZIP from Brightspace and keep it unchanged.
2. Unzip a separate working copy.
3. Initialize the working copy in **your own GitHub repository**.
4. Run:

   `python tools/check_frozen_core.py`

5. Create a specialist agent from the template, for example:

   `python tools/new_agent.py creation_agent "Emerging Technology Creation Agent"`

6. Upload the weekly assignment memo and relevant scaffold files to ChatGPT/Codex. Ask Codex to preserve FROZEN CORE and edit only the new agent folder unless the assignment explicitly says otherwise.
7. Edit `agents/<agent>/specialist_instructions.md` so it embodies the week's analytical framework.
8. Fill the case files in `agents/<agent>/cases/`.
9. Build a prompt packet:

   `python tools/build_prompt.py --agent agents/<agent> --case agents/<agent>/cases/primary.json`

10. Paste the generated `work/..._prompt.txt` into ChatGPT. Ask ChatGPT to return **JSON only** using the required output contract.
11. Save the result under `agents/<agent>/responses/`, then validate it:

   `python tools/validate_response.py agents/<agent>/responses/primary_response.json`

12. Repeat with at least one contrast case. Diagnose a weakness, revise, retest, then commit your final candidate.

The supplied code intentionally does not call the OpenAI API.
