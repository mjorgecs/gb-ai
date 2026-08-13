
[PLANNING MODE]

# Before start

To perform this task you must ONLY read these files: *CLAUDE.md, 4-structure-backoffice, 7-section-type-codenames*.

You can also browser on the internet to get more information about GoodBarber's [sections](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) and [extensions](https://www.goodbarber.com/extensions/)

---
#  Description

I want to build a Claude agent (with skills, a system prompt and a CLAUDE.md file very similar to your) that can identify the required structure of a give description of an app in plain-english. This agent must be able to:
1. Identify the required types of sections (Articles, Sound, etc.)
2. Within the section, it must identify the must suitable service (GBModuleTypeArticle->mcms (simple article section), GBModuleTypeArticle->rss (Feed RSS section)).
3. If there is not a section that matches the requirements, it must say that does not exist a section/extension that can perform what the users asked and suggest two solutions: 
	1. A similar extension that already exist.
	2. A custom code section (built from scratch) and describe its structure  — this description must be very detailed, a developer must be able to create the section after read it.
4. Generate a document where it all is described.

The agent must look for the existing section to suggest — it could be done either through the tables that are in the *7-section-type-conemames* file or searching through the extension link (above).

---
# Questions

1. What type of file must be generated at the end? — a JSON or a Markdown.
2. What is the most suitable number of SKILLs that the agent must have?
	- One skill that handles all types of section.
	- One skill for each section.
	- Skills divided by groups of section/complexity — the Article section has a lot of different services, so it must have a dedicated skill; the section Facebook, Instagram, Twitter are roughly the same, so one skill can handles all of them; etc..

---
# Example

### User's prompt

I am a tour guide in New York and I'd like to build an app about Barcelona to be used by the tourists. The app must have a page with news about New York, a photos section linked to an api with images of New York, a maps page with the location of interesting places and an informative section where I can upload any information.

### Agent's process

1. The user is asking for an app to use with his/her tourists.
2. The given description is about the app's structure (and not design).
3. **News about New York:** the user is asking for a feed/article section with news about New York — check if there is any section/extension like that: exist and it is the **RSS Feed** extension. Create a section with that extension and suggest a content source.
4. **Photos:** the user is asking for an image section linked to an api — check if there is any section/extension like that: does not exist. Now, 2 solutions: suggest similar extensions (e.g., CMS Photos, Custom photo feed, etc.); custom code section — a web page linked to an external API with images of New York.
5.  **Maps:** the user is asking for an maps section — check if there is any section/extension like that: exist and it is the **CMS Map** extension. Create a section with that extension.
6.  **Informative section:** the user is asking for an article — check if there is any section/extension like that: exist and it is the **CMS Articles** extension. Create a section with that extension.
### Agent's output
(Assuming the out put is a JSON, but it could be a Markdown)
```json
{
	appId: 1234,
	sections: {
		"1": {
			"name": "news",
			"type": "GBModuleTypeArticle",
			"service": "rss",
			"baseSource": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
			"price": "free"
		},
		"2": {
			"name": "photos",
			"type": none,
			"service": none,
			options: [("GBModuleTypePhoto", "mcms"), ("GBModuleTypePhoto","custom"), "customCode": "A web page linked to an external API with images of New York"],
			"price": "free"
		},
		"3": {
			"name": "maps",
			"type": "GBModuleTypeMaps",
			"service": "mcms",
			"price": "free"
		},
		"4": {
			"name": "info",
			"type": "GBModuleTypeArticle",
			"service": "mcms",
			"price": "free"
		}
	}
}
```

---
### Extras

- The agent must be aware of the conditions of each section/extension and tell the user when an extension is paid.
- The custom code description must be more detailed.