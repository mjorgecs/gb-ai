[PLANNING MODE]

# Before you start

To perform this task you must read ONLY these files: _CLAUDE.md_, _4-structure-backoffice_, _7-section-type-codenames_.

You may also browse the internet for more information about GoodBarber's [sections](https://www.goodbarber.com/help/organize-your-content-r93/understand-app-sections-and-structure-a34/) and [extensions](https://www.goodbarber.com/extensions/).

---

# Description

I want to build a Claude agent (with skills, a system prompt and a CLAUDE.md file very similar to yours) that can identify the structure required by an app described in plain English. This agent must be able to:

1. Identify the required section types (Articles, Sound, etc.).
2. Within each section, identify the most suitable service (GBModuleTypeArticle -> mcms (simple article section), GBModuleTypeArticle -> rss (RSS feed section)).
3. If no section matches the requirements, state that no existing section or extension can do what the user asked and suggest two solutions:
    1. A similar extension that already exists.
    2. A custom-code section (built from scratch), along with a description of its structure — this description must be detailed enough for a developer to build the section after reading it.
4. Generate a document describing all of the above.

The agent must look up the existing sections it suggests, either in the tables in the _7-section-type-codenames_ file or by searching the extensions link above.

---

# Questions

1. What type of file should be generated at the end — JSON or Markdown?
2. How many skills should the agent have?
    - One skill that handles every section type.
    - One skill per section.
    - Skills grouped by section family or complexity — the Article section has many different services, so it needs a dedicated skill; the Facebook, Instagram and Twitter sections are roughly the same, so a single skill can handle all of them; and so on.

---

# Example

### User's prompt

I am a tour guide in New York and I would like to build an app about New York for tourists to use. The app must have a page with news about New York, a photos section connected to an API with images of New York, a maps page showing the location of interesting places, and an informative section where I can upload any kind of information.

### Agent's process

1. The user is asking for an app to use with their tourists.
2. The description concerns the app's structure (not its design).
3. **News about New York:** the user is asking for a feed/article section with news about New York — check whether such a section or extension exists: it does, the **RSS Feed** extension. Create a section using that extension and suggest a content source.
4. **Photos:** the user is asking for an image section connected to an API — check whether such a section or extension exists: it does not. Two solutions follow: suggest similar extensions (e.g. CMS Photos, Custom photo feed, etc.); or a custom-code section — a web page connected to an external API with images of New York.
5. **Maps:** the user is asking for a maps section — check whether such a section or extension exists: it does, the **CMS Map** extension. Create a section using that extension.
6. **Informative section:** the user is asking for an article section — check whether such a section or extension exists: it does, the **CMS Articles** extension. Create a section using that extension.

### Agent's output

(Assuming the output is JSON, although it could be Markdown.)

```json
{
	"appId": 1234,
	"sections": {
		"1": {
			"name": "news",
			"type": "GBModuleTypeArticle",
			"service": "rss",
			"baseSource": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
			"price": "free"
		},
		"2": {
			"name": "photos",
			"type": null,
			"service": null,
			"options": [
				["GBModuleTypePhoto", "mcms"],
				["GBModuleTypePhoto", "custom"]
			],
			"customCode": "A web page connected to an external API with images of New York",
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

- The agent must be aware of the conditions attached to each section or extension and tell the user when an extension is paid.
- The custom-code description must be more detailed.