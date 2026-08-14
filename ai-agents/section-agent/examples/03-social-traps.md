# Example 03 — Social and brand-name traps

**What this example tests:** whether the agent pattern-matches on brand names. Three intents, each of which produces a technically correct answer that misleads the user unless a specific sentence is added.

## Input

> I want a TikTok feed in the app so people can watch our videos, an AI chatbot that answers questions from our PDF manuals, and our Shopify store.

## Must get right

- TikTok → `GBModuleTypeFakeclickto` + `clicktotiktok`, **with the explicit statement that it is a link, not a feed**, and an alternative offered.
- Chatbot → `GBModuleTypePlugin` + `rag`, **paid**, with a dated figure and an explicit statement of *how* the figure was obtained. The price is high enough to surface immediately, not at the end.
- If the detail page wasn't opened, the output says so. A band read off a category page is not the same as a confirmed price, and presenting it as one is the failure this case tests.
- Shopify → `GBModuleTypeShop` + `shopify`, with the `Shop` vs `Commerce` distinction named.

## Must not do

- Present the TikTok section as if videos will play in the app.
- Quote the RAG Chatbot as free, state a price without a date, or present a category-page band as a verified price.
- Silently assume the user wants native eCommerce, or silently assume they don't.
- Route the chatbot to custom code — it ships as an extension.

---

# App Structure — Social and commerce add-ons

## Summary

Three requested features. All three exist in the platform. All three come with a caveat that changes what the user should expect.

One is free, one is paid, one depends on a decision not yet made.

## Sections

### 1. TikTok — `GBModuleTypeFakeclickto` + `clicktotiktok`

> **This is a link, not a feed.** A TikTok section appears in the menu like any other section, but tapping it opens the TikTok app or website. Your videos will not play inside your app.

The type name is candid about this — `Fakeclickto` is a branded link-out styled to look native. TikTok, Reddit, WhatsApp, Discord, Threads and Snapchat all work this way. Facebook, Instagram and X have first-class types instead.

**If videos should play in the app**, that's a different section: `GBModuleTypeVideo`. Options —

- `youtube` or `vimeo` if the videos are also posted there;
- `custom`, pointing at your own JSON feed of video URLs;
- `mcms`, uploading videos into GoodBarber directly.

Any of those gives real in-app playback. The TikTok link is worth adding **as well**, to send people to the profile — but it should not be the answer to "so people can watch our videos".

### 2. Manual chatbot — `GBModuleTypePlugin` + `rag`

The RAG Chatbot extension: answers questions from documents you supply. Exactly the described feature, and it ships — no custom code needed.

> **Paid — a band of roughly $35–55/month, read off the extensions category page on 2026-08-13.**
>
> **This is not a confirmed price.** The detail page was not opened, so neither the exact figure nor which tier applies has been established. Open `goodbarber.com/extensions/` → RAG Chatbot and read the full pricing line before committing — the category badge and the detail page's pricing line can disagree, and only the pricing line is reliable.

This is the most expensive item in the plan by a wide margin, which is why it's stated here rather than in a summary at the end — and why the uncertainty is stated with it rather than buried.

Worth confirming before building: what the manuals are (page count, whether they're text PDFs or scans), since a scanned PDF with no text layer is a different problem.

### 3. Store — `GBModuleTypeShop` + `shopify`

A section that opens your existing Shopify store.

> **`Shop` and `Commerce` are different products.** `GBModuleTypeShop` is a link to a storefront that lives on Shopify — available on any plan, free. Native in-app selling, with products, collections, a cart and checkout inside the app, is `GBModuleTypeCommerce` and **requires a Shop plan**.

Which one you want depends on something you haven't said:

- **Keep selling on Shopify, app links to it** → this section, free, done.
- **People browse and buy without leaving the app** → a Shop plan and a different structure entirely, covered separately.

Planned as the link, since that's what "our Shopify store" implies. Say if it isn't.

## Extensions

The RAG Chatbot is listed under Sections above because it materialises as a section. No behaviour-only extensions in this plan.

## Gaps

None. All three requests are covered by existing sections.

## Validation

- The `Fakeclickto` link disclosure is present in prose, not only implied by the type name.
- The chatbot price carries an `asOf` date, a `priceVerified: false` flag, the source it came from, and a re-verification instruction. It is not presented as confirmed.
- `Shop` vs `Commerce` named explicitly, with the plan gate.
- Nothing routed to custom code — the chatbot ships as an extension.

## Plan (JSON)

```json
{
  "appId": null,
  "generatedAt": "2026-08-13",
  "summary": "Social link, document chatbot and storefront link.",
  "sections": [
    {
      "order": 1,
      "name": "TikTok",
      "intent": "People watch our videos",
      "status": "matched",
      "type": "GBModuleTypeFakeclickto",
      "typeVerified": true,
      "service": "clicktotiktok",
      "serviceVerified": true,
      "catalogEntry": "TikTok",
      "createRoute": "/manage/app/content-add-clicktotiktok/",
      "createRouteVerified": true,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "LINK, NOT A FEED — opens the TikTok app. Does not satisfy 'watch our videos' on its own. For in-app playback use GBModuleTypeVideo with youtube, vimeo, custom or mcms."
    },
    {
      "order": 2,
      "name": "Manual assistant",
      "intent": "AI chatbot answering from our PDF manuals",
      "status": "matched",
      "type": "GBModuleTypePlugin",
      "typeVerified": true,
      "service": "rag",
      "serviceVerified": true,
      "catalogEntry": "RAG Chatbot",
      "createRoute": "/manage/app/content-add-rag/",
      "createRouteVerified": true,
      "pricing": {
        "tier": "paid",
        "price": "$35-55/month",
        "priceVerified": false,
        "asOf": "2026-08-13",
        "source": "extensions category page",
        "note": "BAND, NOT A CONFIRMED PRICE. Detail page not opened this run — exact figure and applicable tier unestablished. Read the full pricing line before committing."
      },
      "notes": "Ships as an extension — no custom code needed. Confirm the manuals have a text layer."
    },
    {
      "order": 3,
      "name": "Store",
      "intent": "Our Shopify store",
      "status": "matched",
      "type": "GBModuleTypeShop",
      "typeVerified": true,
      "service": "shopify",
      "serviceVerified": true,
      "catalogEntry": "Shopify",
      "createRoute": "/manage/app/content-add-shopify/",
      "createRouteVerified": true,
      "pricing": { "tier": "free", "asOf": "2026-08-13" },
      "notes": "Links out to Shopify. Native in-app selling is GBModuleTypeCommerce and requires a Shop plan — confirm which is wanted."
    }
  ],
  "extensions": [],
  "validation": {
    "sectionCount": 3,
    "warnings": [
      "TikTok section is a link; it does not satisfy the stated goal of watching videos in the app.",
      "RAG Chatbot price is an unverified band from a category page, not a confirmed figure. Detail page not opened. Re-verify before committing.",
      "Shop vs Commerce is an open decision affecting the plan tier."
    ]
  }
}
```

## Sources

- `section-docs/0-section-type-codenames.md` — the `Clickto`/`Fakeclickto` distinction and the `Plugin`/`Shop` service lists, back-office capture 2026-08-12.
- [GoodBarber Extensions](https://www.goodbarber.com/extensions/) — RAG Chatbot pricing band, accessed 2026-08-13.
