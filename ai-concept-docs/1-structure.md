# The Entities

Under the **Hybrid Approach**, the app-building process can be modeled as an interaction between four entities: the **User**, the **App Builder Platform**, the **Description Agent (DA)**, and the **Implementation Agent (IA)**. Together, these entities pursue a single objective — producing the application that most faithfully represents the user's original description. Because the application is only considered complete once the user actually ships it, the interaction between these four entities must be as effortless and intuitive as possible; any unnecessary complexity at this stage directly increases the likelihood of the user abandoning the process before publishing.

## User

The user is present throughout the entire process, from the initial description to the final review and any subsequent adjustments. As the only human entity in this interaction, the user is responsible for communicating directly with the Description Agent and for validating or correcting its output when necessary. Given that the quality of an AI agent's output is directly proportional to the quality of the input it receives, the user must be reasonably comfortable articulating the intended structure, functionality, and design of the app in natural language.

Since the system relies on large language models (LLMs), the precision and level of detail in the user's description have a direct impact on the quality of the generated application. Users can therefore be broadly classified into two categories:

- **Non-expert users:** These users typically provide short, vague, or incomplete descriptions, often lacking the context an AI agent needs to make accurate decisions. They are generally unfamiliar with prompt-engineering techniques and may not understand how their wording maps onto the platform's underlying logic. For example, a non-expert user might describe an app simply as "a shop app for my store," without specifying catalog structure, payment methods, or required integrations.
- **Expert users:** These users have prior experience either with traditional no-code platforms or with software development, and are consequently more capable of producing detailed, structured, and technically grounded descriptions. This category includes freelancers and agencies who build applications on behalf of clients — a segment that represents a strategic early-adopter group, since exposing the AI tools to this audience first would generate higher-quality feedback and richer training signal for refining the Description Agent's behavior before a broader rollout.

## App Builder Platform

The App Builder Platform is the pre-existing system that already enables users to create native applications without writing code. Its core strengths lie in its JSON-based application structure — the foundation upon which the entire app-building process is built — and in the mature ecosystem of infrastructure and features already developed around it, including extensions, APIs, layout systems, and integrations.

Failing to leverage this existing platform would represent a significant strategic misstep. Consequently, any new agentic AI capability must be integrated seamlessly into the platform's existing architecture, preserving its current level of maintainability, code quality, and technical maturity rather than introducing a parallel, disconnected system.

## Description Agent (DA)

The Description Agent is the AI entity responsible for extracting, interpreting, and refining all information related to the desired application — including business logic, visual design, and required extensions — based on the user's natural-language input. As an AI agent, the DA possesses the full range of capabilities associated with modern agentic systems (skill composition, data access, and the ability to delegate tasks to specialized subagents), all of which are directed specifically toward the platform's context and operational logic.

### What does the DA need to know?

1. **The platform's operating logic:** The DA must have a thorough understanding of how the App Builder Platform functions internally, in order to make suitable and effective decisions when translating a description into a valid app structure. This requires providing the DA with a context window that accurately reflects the platform's real usage patterns and constraints.
2. **The library of pre-made components and layouts:** To fully capitalize on work that has already been built and validated, the DA must be able to locate and correctly interpret existing components and layouts, distinguishing between them by function and intended use case (for example, differentiating a "product catalog" layout from a "blog feed" layout, even though both may display a list of items).
3. **The user's prompt:** This is the trigger for the entire process, and consequently one of the most critical inputs in the whole system. Since the quality of the final app depends heavily on the specificity of this prompt, the platform should actively support users in producing better descriptions — for instance, by offering an optional planning step before generation begins, or by suggesting pre-made prompt templates that are known to yield strong results.

### What does the DA produce?

Once the user's description has been finalized, the DA must generate a structured document that encodes this information in a consistent, machine-readable format — typically a JSON file — so that the specification is preserved accurately and can be reliably consumed during the implementation stage.

Two approaches were considered for generating this document:

**1. Unstructured (schema-free) JSON**

Under this approach, no predefined JSON schema exists. Instead, the DA follows a set of general guidelines describing what categories of information the document should contain (e.g., design preferences, required services), without constraining the exact fields or their structure.

```json
{
  "app_theme": "nature inspired, calm color palette",
  "core_purpose": "connect local hikers to organize group trips",
  "requested_features": [
    "user profiles with hiking experience level",
    "trip creation with map-based route drawing",
    "in-app group chat per trip",
    "push notifications for trip updates"
  ],
  "design_notes": "outdoorsy, minimal, large touch targets for use on trail"
}
```

- **Advantages:** This approach is highly flexible and allows the DA to capture nearly the full richness of the user's description, resulting in a more complete and representative specification.
- **Disadvantages:** Because the resulting file has no fixed format or fixed set of tags, it becomes harder to process consistently. The Implementation Agent — and any other system consuming this document — must re-interpret an inconsistent structure on every run, which increases processing overhead and the risk of misinterpretation.

**2. Pre-structured (schema-based) JSON**

Under this approach, a fixed JSON schema defines the main fields that must be populated with information about the app (e.g., theme, extensions, sections, and any special requirements):

```json
{
  "app_id": 1234,
  "type": "content",
  "theme": ["nature", "calm"],
  "sections": ["home", "chat", "maps", "profile"],
  "extensions": ["chatbot", "notifications"],
  "special_requirements": []
}
```

- **Advantages:** This approach produces a concise, predictable specification containing all the fundamental information required to build a functional application. Since the user retains the ability to refine the app after its initial generation, the primary objective at this stage is to quickly produce a working "prototype" that reasonably matches the user's requirements, rather than to capture every possible nuance upfront.
- **Disadvantages:** A fixed and restrictive set of fields may fail to capture certain nuances of the user's original description. This limitation can be partially mitigated by including optional, free-text fields within the schema, reserved for additional details that do not map cleanly onto the predefined structure.

## Implementation Agent (IA)

Given the structured document produced by the Description Agent, the Implementation Agent is responsible for selecting and assembling all the components required to build the requested application. To perform this task effectively, the IA must, like the DA, be seamlessly integrated with the App Builder Platform and capable of operating the full range of tools it exposes (component library, layouts, extension system, and APIs).

Although the detailed design of the Implementation Agent falls outside the scope of the present project, it constitutes a critical stage in the overall pipeline, since it is ultimately responsible for translating the DA's specification into a functioning, shippable application.

---

_The following section of this report addresses the application of Prompt Engineering and Context Engineering in the configuration of the AI agents._