# Tokens

The AI tools embedded in the platform will be provided be a third-part company through an API service that charges per input and output tokens. Since the number of tokens translates, roughly, to pieces of words, it would be important to have succinct inputs that describe the app properties with minimum number of unnecessary words as possible.

Instead of a drawback it can be an opportunity to explore other tools and methods to improve the reasoning quality of the agents and minimize the number of wasted tokens. Beside the token pricing methodology, another motivation to improve the agent's reasoning is the fact that most of the users will give short and incomplete descriptions of their apps. By focusing on developing a high-quality reasoning logic that represents the correct usage of the platform these two difficulties will be overcome simultaneously.
# Methods to Improve Agents

There are few ways to improve agent's reasoning (...)

(context window; why context eng is more important than prompt - what is that?)
 
(...)
## Prompt Engineering

It is about how the instructions are written — clarity, structure, examples. Despite the fact that the the user is who will make the prompts, therefore, it should not be our responsibility to care how to prompt is written. It is worth noting that all instructions in the context window are interpreted by the model, therefore it must be well structured and accurate.

(...)
## Context Engineering

It aggregates everything that ends up in the model's context window ate each turn — system prompt, tool definition, retrieved data, message history — not just the words of prompt itself (...)

(...)