# The Entities

The structure of an AI-Powered No-Code App Builder as described by the **Hybrid Approach** can be thought as an interaction between four entities: **User, App Builder Platform, Description Agent and the Implementation Agent.**

## User

The user is involved in the process from start to finish. It is the entity that will interact directly with the AI agent and make changes when needed. As a result, the user must be capable and, at least, comfortable, to talk to the agent and describe effectively the idea behind the app, its structure and design.

Once we are working with LLMs it is important to describe what we want clearly and detailed. Therefore, we can divide the user into two types:

- **Non-expert:** This user may provide a poor description about the app with very little context and details. He or she may not know about techniques to enhance the results and how the the prompt is connected with the platform's logic.
- **Expert:** This user is someone who has some expertise to interact with AI agents and to build apps on a traditional way - it can be using the traditional XX app builder platform or programming. The people who use the platform to build apps for their clients may be included in this category, so it would be a good idea make these AI tools available first to them. By doing this, we could train the agent and get a more detailed feedback.
## App Builder Platform

This is the platform already built which enables users to create native apps without coding. Its strengths are the JSON-based app structure, which is the cornerstone of all the app building process, and all the infrastructure and features (extensions, APIs, layouts, etc.) already built around the platform.

Not take all advantages from this platform would be a big mistake, therefore, the new agentic AI tools must be integrated seamlessly with the platform to minimize bugs, and other problems.

## Description Agent (DA)

This is the AI agent responsible to extract and refine all the information about the app provided by the user (business logic, design, extensions, etc.).

- **What does the DA need to know?**
	1. **The operation process of the platform:** The DA needs to know how the app builder platform works, so it can make the most suitable and effective choices. Knowing how the platform works means to have the correct context window...
	2. **Pre-made components and layouts:** With the objective to reuse all the work already done and tested, the DA must know where and how to find it; it also means being able to distinguish components and layouts by their function and usage. 
	3. **User's prompt:** It is what will trigger the DA. The user's prompt is a crucial step in our logic, therefore it must be as specific as possible. We must develop strategies to help users to write the most detailed and representative description of their apps such as: ...
- **What will the DA produce?**
	dfwfw