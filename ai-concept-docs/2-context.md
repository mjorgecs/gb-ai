# Tokens

The AI tools embedded in the platform will be provided by a third-party company through an API service that charges based on the number of input and output tokens processed. Since a token roughly corresponds to a word or a fragment of a word [^1], it is important to keep inputs succinct, describing the application's properties with the minimum number of unnecessary words possible.

Rather than being purely a limitation, this constraint represents an opportunity to explore tools and methods that improve the reasoning quality of the agents while minimizing token waste. Beyond the cost implications of the token-based pricing model, there is a second, equally important motivation for improving the agents' reasoning capabilities: the fact that most users will provide short and incomplete descriptions of their intended applications. By focusing on developing a high-quality reasoning process — one that correctly reflects the platform's intended usage — both difficulties can be addressed simultaneously.

# Context Window

As previously discussed, these AI tools are built on Large Language Model (LLM) architectures, which generate responses probabilistically. At each step, the model predicts the most likely next word based on a probability distribution over its entire vocabulary [^2]. Since the model's output depends directly on the tokens it can currently "see," it is essential that the instructions and information supplied at inference time are accurate, well-structured, and unambiguous [^3].

The model's role, instructions, and background rules are defined within the **context window** — the total space of tokens the model has access to at inference time, comprising the system prompt, tool definitions, retrieved data, and message history, among other elements. Two closely related techniques, **Prompt Engineering** and **Context Engineering**, can be used to improve the quality and accuracy of this context window. The central goal of both techniques is to provide the **smallest** set of high-signal tokens that reliably produces the desired behavior — not the most complete or exhaustive one [^4].

## Prompt Engineering

Prompt Engineering concerns _how_ instructions are written — their clarity, structure, and use of illustrative examples. Although, in this platform's context, it is ultimately the end user who writes the application-description prompt (and it is therefore not the platform's responsibility to control how that specific prompt is phrased), it remains essential to note that every instruction the engineering team places within the context window is likewise interpreted by the model. As such, all system-level instructions must be equally well-structured and precise.

**Advantages**

- Fast to iterate: adjusting the wording and re-testing requires no architectural or infrastructural changes.
- Low overhead for prototyping, particularly for narrow, single-shot tasks such as classification, extraction, or simple content generation.

**Disadvantages**

- Does not scale well to multi-turn or agentic workflows: a static prompt alone cannot manage a growing conversation history or retrieve new data mid-task.
- Tends toward brittleness over time, as teams progressively add edge-case rules to correct undesired behavior, gradually making the prompt fragile and difficult to maintain.

## Context Engineering

Context Engineering is a broader discipline that encompasses everything that ultimately populates the model's context window at each turn — the system prompt, tool definitions, retrieved data, and message history — rather than only the wording of the prompt itself. In other words, while Prompt Engineering concerns what is _written_, Context Engineering concerns what is actually _present_ in the model's context at the moment of inference.

As the context window grows larger, it presents an opportunity to include more information about the platform's usage, its existing components, and its business rules. However, as the number of tokens in context increases, the model's ability to accurately recall and reason over that information degrades — a phenomenon commonly referred to as _context rot_. This occurs, to some degree, across all LLMs, because the transformer architecture underlying these models requires every token to attend to every other token; as context grows, this attention is distributed more thinly across a larger set of tokens, reducing the model's effective focus on any single piece of information.

**Advantages**

- Scales effectively to multi-turn, agentic systems, where Prompt Engineering alone is insufficient.
- Directly mitigates context rot: retaining only high-signal tokens tends to improve accuracy, particularly in longer or more complex interactions.
- Naturally reduces token cost, since minimal, just-in-time context results in fewer tokens per call and pairs well with caching strategies.
- More maintainable as the platform scales: instead of relying on an ever-growing list of hardcoded rules, the system can be built around retrieval mechanisms, tools, and memory structures that adapt automatically as the component catalog and business logic expand.

**Disadvantages**

- Requires greater upfront engineering effort, involving the construction of retrieval systems, tool interfaces, and memory or context-compaction logic, rather than simply writing text.
- May introduce additional latency, since just-in-time retrieval requires extra tool-call round trips instead of making all information available immediately.
- Requires ongoing evaluation and tuning: determining what constitutes "high-signal" information is not obvious upfront and requires iterative refinement based on real failure cases, representing more overhead than adjusting a single static prompt.

## References

[^1]: OpenAI. (2026). _What are tokens and how to count them?_ OpenAI Help Center. [https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

[^2]: Jurafsky, D., & Martin, J. H. (2025). _Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition with Language Models_ (3.ª ed.). Manuscrito online. [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/)

[^3]: Anthropic. (2026). _Prompting best practices._ Claude Platform Documentation. [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

[^4]: Rajasekaran, P., Dixon, E., Ryan, C., & Hadfield, J. (2025). _Effective context engineering for AI agents._ Anthropic Engineering. [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
