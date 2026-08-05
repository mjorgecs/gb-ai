# Tokens

The AI tools embedded in the platform will be provided be a third-party company through an API service that charges per input and output tokens. Since the number of tokens translates, roughly, to pieces of words, it would be important to have succinct inputs that describe the app properties with the minimum number of unnecessary words as possible.

Instead of a drawback it can be an opportunity to explore other tools and methods to improve the reasoning quality of the agents and minimize the number of wasted tokens. Beside the token pricing methodology, another motivation to improve the agent's reasoning is the fact that most of the users will give short and incomplete descriptions of their apps. By focusing on developing a high-quality reasoning logic that represents the correct usage of the platform these two difficulties will be overcome simultaneously.
# Context Window

As said before, these AI tools are based on a LLMs structure which means the response that they generate is probabilistic. They do this by choosing the next word based on its probability to appear next on that text. That probability is calculated using neural networks that are calibrated through all the data given to the AI model. As a result, the AI's response is directly related to all the instructions and information given to it in advance, therefore it is very important to provide the instructions accurately.

The model's role, instructions, and background rules are set in the context window — the total space of tokens the model sees at inference time (system prompt, tool definitions, retrieved data, message history, etc.). We can use techniques like Prompt Engineering and Context Engineering to improve the quality and accuracy of the context window. These techniques are widely used and their main goal is to provide the **smallest** set of high-signal tokens that reliably produces the right behavior — not the most complete.
## Prompt Engineering

It is about how the instructions are written — clarity, structure, examples. Despite the fact that the the user is who will make the prompts, therefore, it should not be our responsibility to care how to prompt is written, it is worth noting that all instructions written by te programmer in the context window are interpreted by the model, therefore it must be well structured and accurate.
#### Advantages
- Fast to iterate — change the wording, test, done. No architecture or infrastructure changes needed.
- Low overhead to prototype, especially for narrow, one-shot tasks (classification, extraction, simple generation).
#### Disadvantages
- Doesn't scale well to multi-turn or agentic workflows — a prompt alone can't manage a growing conversation history or fetch new data mid-task.
- Tends toward brittleness over time: teams keep adding edge-case rules to "fix" behavior, and the prompt becomes fragile and hard to maintain.
## Context Engineering

It is a more broad discipline that aggregates everything that ends up in the model's context window at each turn — system prompt, tool definition, retrieved data, message history — not just the words of prompt itself. (what is actually done)

As the context window is getting bigger, it is an opportunity to include more information about the usage of the platform, the existing components, etc.. But, as the number of tokens in context grows, a model's ability to accurately recall and reason over that information degrades — this happens across all models to some degree, because the transformer architecture means every token attends to every other token, so attention gets stretched thinner as context grows.
#### Advantages
- Scales to multi-turn, agentic systems where prompt engineering alone breaks down.
- Directly addresses context rot — keeping only high-signal tokens tends to improve accuracy, especially on longer or more complex interactions.
- Naturally reduces token cost, since minimal/just-in-time context means fewer tokens per call, and pairs well with caching.
- More maintainable as the platform grows: instead of hardcoding an ever-longer list of rules, you build retrieval/tools/memory that adapt as the component catalog and business logic expand.
#### Disadvantages
- More upfront engineering effort — build retrieval systems, tool interfaces, and memory/compaction logic, not just write text.
- Can add latency — just-in-time retrieval means extra tool-call round trips instead of everything being available immediately.
- Needs ongoing evaluation and tuning — deciding what counts as "high signal" isn't obvious upfront and requires iterating against real failure cases, more overhead than adjusting a single prompt.