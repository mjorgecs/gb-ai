# The Entities

The structure of an AI-Powered No-Code App Builder described by the **Hybrid Approach** can be thought as an interaction between four entities: **User, App Builder Platform, Description Agent and Implementation Agent.**

These entities will work together with the objective to **create the most representative app** based on the user's description. Therefore, the interaction must be as easy as possible because the app will not be ready until the user ships it.
## User

The user is involved in the process from start to finish. It is the entity that will interact directly with the AI agent and make changes when needed. As a result, the user must be capable and, at least, comfortable, to talk to the agent and describe effectively the idea behind the app, its structure and design.

Once we are working with LLMs it is important to describe what we want clearly and detailed. Therefore, we can divide the user into two types:

- **Non-expert:** This user may provide a poor description about the app with very little context and details. He or she may not know about techniques to enhance the results and how the the prompt is connected with the platform's logic.
- **Expert:** This user is someone who has some expertise to interact with AI agents and to build apps on a traditional way - it can be using the traditional XX app builder platform or programming. The people who use the platform to build apps for their clients may be included in this category, so it would be a good idea make these AI tools available first to them. By doing this, we could train the agent and get a more detailed feedback.
## App Builder Platform

This is the platform already built that enables users to create native apps without coding. Its strengths are the JSON-based app structure, which is the cornerstone of all the app building process, and all the infrastructure and features (extensions, APIs, layouts, etc.) already built around the platform.

Not take advantage from this platform would be a big mistake, therefore, the new agentic AI tools must be integrated seamlessly with the platform to keep the actual level of maintainability and coding maturity.
## Description Agent (DA)

This is the AI agent responsible to extract and refine all the information about the app provided by the user (business logic, design, extensions, etc.). It has all the capabilities of an AI agent (skills development, data access, subagent deployment, etc.) directed to the platform context and usage.

- **What does the DA need to know?**
	1. **The operation process of the platform:** The DA needs to know how the app builder platform works, so it can make the most suitable and effective choices. Knowing how the platform works means to have the correct context window related to the platform usage.
	2. **Pre-made components and layouts:** With the objective to reuse all the work already done and tested, the DA must know where and how to find it; it also means being able to distinguish components and layouts by their function and usage. 
	3. **User's prompt:** It is what will trigger the DA. The user's prompt is a crucial step in our logic, therefore it must be as specific as possible. We must develop strategies to help users to write the most detailed and representative description of their apps: ask if the user wants to create a plan before creating the app; suggest pre-made prompts that have excellent results.
- **What will the DA produce?**
	Given the final description of the app, must generate a structured document using that information. The document must follow a structure, such as a JSON file, to maintain the specification and improve the understanding when it will be used in the implementation stage.

	There are two approaches to generate this document:
	 1. **Non-pre-structured JSON:** There is not a pre-formatted JSON. However, there are some guidelines about what must be contained in the JSON file (information about the app's design, services, etc.).
		 - **Advantages:** This is a more flexible approach and enables us to get almost all information about the app and, which results in an completed description parsed into a JSON.
		 - **Disadvantages:** Working with a file which we do not know its format nor tags can result in a repetitive and inefficient process due to the inconsistent number of tags and need to interpret them everytime.
	 2. **Pre-structured JSON:** There is a pre-formatted JSON with all the main fields that must be filled  with the information about the app (theme, extensions, sections, special requirements, etc.).
		```
		{
			"app_id": 1234,
			"type": "content",
			"theme": "nature",
			"sections": ["home", "chat", "maps"],
			"extentions": ["chatbot", "notifications"],
			...
		}
		```
		- **Advantages:** This approach delivers a concise description with all the fundamental information needed to create an app. Since the user will be able to modify the app later, the main goal is to create a working "prototype" which matches the user's requirements faster rather than very detailed. 
		- **Disadvantages:** Some nuances may be left due to the restrictive set of tags that must be filled. This problem can be mitigated by having extra fields that be filled with more detailed information.
## Implementation Agent (IA)

Given the formatted document generated by the DA, the IA must select all the components needed to build the app. To do that, it also must be seamlessly integrated with the platform and able to manipulate all the tools available.

Although the Implementation Agent is outside the scope of this project, it is a very important step on the final development phase. 