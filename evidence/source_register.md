# Agentic AI Creation Evidence Register

Access date for web sources: 2026-10-05.

## Core creation and evolution evidence

1. Vaswani, A., et al. (2017). *Attention Is All You Need*. https://arxiv.org/abs/1706.03762
   - Primary research introducing the Transformer architecture based on attention rather than recurrence or convolution.
   - Supports the predecessor-capability claim that scalable Transformer models underlie later LLM agents.

2. Brown, T. B., et al. (2020). *Language Models are Few-Shot Learners*. https://arxiv.org/abs/2005.14165
   - Primary research showing that a large autoregressive language model could perform varied tasks from natural-language instructions and a small number of examples without task-specific gradient updates.
   - Supports the transition from task-specific models toward general-purpose language interfaces.

3. Ouyang, L., et al. (2022). *Training language models to follow instructions with human feedback*. https://arxiv.org/abs/2203.02155
   - Primary research on supervised instruction tuning and reinforcement learning from human feedback.
   - Supports the claim that improved intent-following and behavioral alignment made models more usable as workflow controllers, while documented mistakes show that alignment did not remove reliability limits.

4. Yao, S., et al. (2022; ICLR 2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. https://arxiv.org/abs/2210.03629
   - Primary research interleaving language-model reasoning traces with task-specific actions and interaction with external sources or environments.
   - Supports the creation-history link between LLM reasoning and iterative action loops.

5. Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. https://arxiv.org/abs/2302.04761
   - Primary research demonstrating a language model trained to decide which APIs to call, when to call them, and how to incorporate results.
   - Supports tool selection as a predecessor capability of agentic systems.

6. Anthropic. (2024, November 25). *Introducing the Model Context Protocol*. https://www.anthropic.com/news/model-context-protocol
   - Official announcement of an open standard for connecting AI applications to data sources and tools.
   - Supports the ecosystem-enabler claim that an open protocol can replace some fragmented, source-specific integrations; it does not establish universal adoption or implementation quality.

7. OpenAI. (2025, March 11). *New tools for building agents*. https://openai.com/index/new-tools-for-building-agents/
   - Official launch description for the Responses API, built-in tools, Agents SDK, guardrails, tracing, and orchestration support.
   - Supports the shift from research patterns toward packaged developer infrastructure.

8. OpenAI. (retrieved 2026-10-05). *A practical guide to building agents*. https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
   - Official practitioner guide defining agents as systems in which an LLM manages workflow execution and selects tools within guardrails.
   - Identifies complex decisions, difficult rules, and unstructured data as needs that agentic systems address; also recommends evals, layered guardrails, and human intervention for high-risk actions.
   - A course-provided PDF capture is available in the MASY1-GC 1800 Prep Lab 2 materials.

9. OpenAI. (2026, September 10). *Introducing the Agents API*. https://openai.com/index/introducing-the-agents-api/
   - Official announcement of a managed agent harness with context management, tool search, programmatic tool calling, MCP support, subagents, sandboxes, and observability.
   - The service was released in public beta, supporting the conclusion that agentic infrastructure is increasingly productized but still evolving.

## Evidence interpretation rule

The sources document predecessor capabilities, research demonstrations, standards, and provider infrastructure. The conclusion that modern agentic AI emerged from their convergence is an analytical synthesis, not a claim that one paper, company, or individual invented the entire category. Vendor publications establish what those vendors released and recommend; they do not independently establish cross-vendor reliability or organizational value.
