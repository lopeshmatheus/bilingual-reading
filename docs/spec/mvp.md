# MVP spec: Bilingual Reading

Decided through a grilling session on 2026-10-06 and 2026-10-07. Terms follow [GLOSSARY.md](../../GLOSSARY.md); decisions with lock-in are in [docs/adr](../adr). Market research is in [docs/research/market-2026-10.md](../research/market-2026-10.md).

## Problem Statement

Reading real books and articles in a foreign language is the best practice there is, but it is tiring: every unknown word or tangled sentence means leaving the text for a dictionary or a translator. Existing apps either show the translation all the time (so your eyes rest on your own language), hide it behind clumsy lookups, or bury the reading under colours, streaks and paywalls (LingQ at about $15/month). Nobody combines your own EPUBs, context-aware translation, a calm reading screen and sync between phone and desktop. Explanations written in Portuguese are especially rare.

## Solution

A calm reader, inspired by Linga, where help is always one gesture away. On the phone you read the foreign text and tap a word for its Gloss or a Sentence to Reveal its Translation, with a toggle into Bilingual view. On desktop, Bilingual view is the default: each Paragraph's Translation sits right under it. Claude produces Translations, Glosses and Explanations in the Reader's Native language (Portuguese or English), so meanings fit the context. Readers import EPUBs, paste articles, or pick from a public-domain Library, save words as they read, and continue on any device.

## User Stories

### Getting started

1. As a new Reader, I want to sign up with email or Google/Apple, so that my Texts and Saved words follow me across devices.
2. As a new Reader, I want to choose my Native language (Portuguese or English), so that every Translation and Explanation is written in it.
3. As a new Reader, I want to choose the Reading language I'm practising, so that the Library and defaults match it.
4. As a Reader, I want to change my Native language later, so that I'm not locked into my first choice.

### Getting something to read

5. As a Reader, I want to import an EPUB from my phone or computer, so that I can read the books I already own.
6. As a Reader, I want to paste a URL and get a clean Article, so that I can read news and blog posts.
7. As a Reader, I want to paste raw text, so that I can read anything I copied.
8. As a Reader, I want to browse a Library of public-domain Books in my Reading language, so that I have something good to read straight away.
9. As a Reader, I want the app to detect a Text's Reading language and let me correct it, so that Translation uses the right pair.
10. As a Reader, I want imported Books split into their real Chapters with titles, so that navigation matches the original book.
11. As a Reader, I want to see my Texts on a shelf with progress, so that I can pick up where I left off.
12. As a Reader, I want to delete a Text, so that my shelf stays tidy.

### Reading on mobile

13. As a Reader on my phone, I want to see only the foreign text by default, so that I'm actually practising.
14. As a Reader on my phone, I want to tap a word and see its Gloss in a bottom sheet, short meaning first, so that I can keep reading quickly.
15. As a Reader on my phone, I want to long-press or drag across several words to Gloss a phrase or idiom, so that multi-word expressions make sense.
16. As a Reader on my phone, I want to tap a Sentence to Reveal its Translation inline, and tap again to hide it, so that I can check my understanding without leaving the page.
17. As a Reader on my phone, I want a toggle into Bilingual view, so that I can switch to full support on hard passages.
18. As a Reader on my phone, I want comfortable typography (font size, line height, light/dark/sepia), so that long reading sessions are pleasant.
19. As a Reader on my phone, I want my reading position saved continuously, so that I never lose my place.

### Reading on desktop

20. As a Reader on desktop, I want Bilingual view by default, with each Paragraph's Translation directly under it, so that I can read at full speed.
21. As a Reader on desktop, I want to hide Translations with one toggle, so that I can push myself when I'm comfortable.
22. As a Reader on desktop, I want to click or hover a word to see its Gloss, so that I don't need my phone's gestures.
23. As a Reader on desktop, I want to drag across words to Gloss a phrase, so that idioms work the same as on mobile.
24. As a Reader on desktop, I want keyboard shortcuts (next/previous Chapter, toggle Bilingual view, save word), so that I can read without the mouse.

### Understanding more deeply

25. As a Reader, I want a Gloss that reflects how the word is used in this Sentence, not a list of dictionary senses, so that the meaning is right the first time.
26. As a Reader, I want to ask for an Explanation of a Sentence in my Native language, so that I understand the grammar or idiom behind it.
27. As a Reader, I want to hear a word or Sentence read aloud with my device's voice, so that I learn pronunciation.

### Saved words

28. As a Reader, I want to save a word or phrase from its Gloss with one tap, so that I can build my vocabulary while reading.
29. As a Reader, I want Saved words highlighted wherever they appear in any Text, so that I notice them again in context.
30. As a Reader, I want a list of my Saved words with their Gloss and source Sentence, so that I can review them.
31. As a Reader, I want to remove a Saved word, so that words I've learned stop being highlighted.

### Translation behaviour

32. As a Reader, I want the Chapter I open to be ready quickly and the next one prepared in the background, so that I rarely wait.
33. As a Reader, I want a clear loading state when a Chapter is still being translated, so that I know it's coming.
34. As a Reader, I want a Translation I've seen once to be instant afterwards on every device, so that the app feels fast.
35. As a Reader, I want to see the original text even if Translation fails, with a retry, so that a network problem never blocks reading.

### Sync

36. As a Reader who switches devices, I want my position, Texts and Saved words synced between phone and desktop, so that I can continue anywhere.

### Free book and Subscription

37. As a new Reader, I want my first Book of up to about 100k words fully translated for free, so that I can judge the app on a whole book.
38. As a Reader, I want to read Library Books without spending my Free book, so that I can explore freely (Library Translations are shared and cheap for us).
39. As a Reader without a Subscription, I want a clear explanation when a Book exceeds the free size or when I import a second Book, so that I know why and how to continue.
40. As a Reader, I want to subscribe in the app on iOS/Android or on the website, so that I can pay where I am.
41. As a Subscriber, I want my Subscription recognised on every device, so that I don't pay twice.
42. As a Reader, I want to restore purchases and manage or cancel my Subscription, so that I'm in control.

## Implementation Decisions

- **One Flutter app** for iOS, Android and web ([ADR 0001](../adr/0001-flutter-for-mobile-and-web.md)). Layout switches by screen width: below a breakpoint is the mobile reader (foreign text + Reveal + Bilingual toggle), above it is the desktop reader (Bilingual view default).
- **Self-hosted Appwrite** for auth, database, file storage, realtime sync and Dart server functions ([ADR 0002](../adr/0002-self-hosted-appwrite.md)). The app never holds the Claude key.
- **Ingestion module** (server side): takes an EPUB, URL or raw text and produces Text, then Chapters, then Paragraphs, then Sentences, with stable ids. EPUB uses the spine and table of contents; a URL goes through readability-style extraction; an Article is one Chapter. Sentence splitting is per Reading language (EN, ES, FR, DE, IT, PT; no CJK in the MVP).
- **Translation module** (server side, Claude): translates a Chapter in Paragraph batches, a few Paragraphs per call plus the neighbouring Paragraphs as read-only context. A rule-based, per-language splitter marks the source Sentences with stable ids at ingestion; Claude returns the Translation grouped by those ids and may merge neighbouring Sentences, which are then shown together. A call that returns the wrong ids is retried once, then falls back to the Paragraph's Translation only. The style is natural, as a native speaker would say it, with no literal mode. Names of people and places stay in the original, headings are translated, and poems are translated line by line. Jobs run for the opened Chapter and the next one. Results are cached, keyed by Text, Chapter and Native language, and keep the model and prompt version they were made with until a Reader asks to regenerate ([ADR 0003](../adr/0003-claude-translates-chapters-ahead.md)).
- **Models**: a small, cheap Claude model (Haiku) translates Chapters and writes Glosses; a bigger one (Sonnet) writes Explanations. Check current model ids and prices before implementing.
- **Gloss**: every word is Glossed while its Chapter is translated, so taps are instant. A Gloss holds the meaning in context, the base form and the part of speech, with no example sentence in the MVP. Claude also marks Chunks (idioms, phrasal verbs, split verbs such as German "rief … an", names) as spans over the Sentence, each with its own meaning.
- **Explanation** is an on-demand call to the bigger model with the Sentence as context, cached and keyed by Sentence and Native language.
- **Jev for Chunk and Gloss decisions**: choosing real Chunks from candidate phrases, and deciding which words need a Gloss at all (a cost lever), are designed around Jev, TypeSafe's "System One" decision model (typed yes/no and choice answers, no free text). It sits behind a small replaceable "decision step" with a Claude-and-rules fallback. Its accuracy on our six languages is unknown, so the first ticket in this area is an accuracy check (see `docs/research/jev/`).
- **Sharing rule**: Library Books are translated once per Native language and shared; Uploads and Articles are private to their Reader and never shared ([ADR 0004](../adr/0004-share-translations-only-for-public-domain.md)).
- **Languages**: Native language is pt-BR or English. Reading languages are EN, ES, FR, DE, IT and PT, minus the Reader's own Native language.
- **Audio**: device/browser text-to-speech on a word or Sentence; no synced Chapter audio.
- **Saved words**: stored per Reader with lemma or surface form, Gloss, source Sentence id and Reading language; the reader highlights matches client-side.
- **Access rules**, enforced in server functions: Library is free; one Free book up to about 100k words; everything else needs a Subscription. Entitlements come from RevenueCat (App Store, Google Play, Stripe web) via webhook into Appwrite ([ADR 0005](../adr/0005-revenuecat-for-subscriptions.md)).
- **Data model (outline)**: Reader, Text (kind: Book or Article; source: Library or Upload), Chapter, Paragraph, Sentence, Translation, Gloss, Explanation, SavedWord, ReadingPosition, Entitlement.

## Testing Decisions

- Test external behaviour at the highest seam: ingestion is tested as "EPUB/URL/text in, Chapters/Paragraphs/Sentences out" against a small set of fixture books per Reading language.
- Translation is tested against the module boundary with Claude stubbed: alignment (every Sentence gets exactly one Translation), caching (a second request makes no Claude call) and the sharing rule (an Upload is never served to another Reader).
- Access rules (Free book size, second Upload, Library always free) are tested in server functions with fake entitlements.
- Reader UI gets widget tests for the core gestures: tap to Gloss, tap to Reveal, Bilingual toggle, save word.
- No prior art exists yet; the repo is empty apart from tooling.

## Out of Scope

- LingQ-style word statuses (new, learning, known) and colouring every word.
- Flashcards, spaced repetition and Anki export.
- Synced Chapter audio and cloud voices.
- Chinese, Japanese, Korean and other languages that need special word splitting.
- Native languages other than Portuguese and English.
- PDF, MOBI and FB2 import.
- A browser extension.
- Native desktop apps (Flutter makes them possible later).
- Translation that fades as the Reader learns.
- Reader-corrected Translations.

## Further Notes

- Linga (linga.io) is the reference app for feel: calm interface, tap-to-translate, EPUB import. Matheus wants to borrow heavily from it.
- Cost: earlier estimates ($0.10 to $1.50 per novel) assumed Glosses on tap. Glossing every word with the Chapter makes each Chapter's output much larger, so re-estimate with verified model prices before fixing the Free book cap and the spending guardrails.
- The Free book cap (about 100k words) still bounds the worst case per new Reader, but not at the earlier figure of roughly $2.

## Open questions

- **What a tap selects by default.** Recommended: Chunk first, so tapping a word inside a Chunk selects the whole Chunk, with handles or a second tap to narrow it to the word. Alternatives: word first with a "part of: …" line, or both meanings stacked in the sheet.
- **What happens when a Translation looks wrong.** Recommended: a "Looks wrong?" button on a Sentence that regenerates it with the bigger model, replaces the cached one, and has a daily limit. Alternatives: report only, or nothing in the MVP.
- **Extra tickets** for the work around the features are drafted in [docs/tickets/extra-tickets-draft.md](../tickets/extra-tickets-draft.md) and wait for approval.
- **Jev access.** It needs a TypeSafe API key held by the project owner and network access to `api.typesafe.ai`; neither key nor results are in the repo.
