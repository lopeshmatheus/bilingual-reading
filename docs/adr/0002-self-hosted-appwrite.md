# Self-hosted Appwrite as the backend

Accounts, Texts, Translations, Saved words and sync run on a self-hosted Appwrite instance (auth, database, file storage, realtime and Dart functions). Appwrite was chosen over PocketBase and Supabase because it has an official Flutter SDK, server functions in Dart (one language end to end), and room to grow beyond a single machine, while still letting us host it ourselves for now. Calls to Claude happen only inside Appwrite functions, so the API key never ships in the app.

## Considered Options

- **PocketBase**: simpler (one binary, SQLite), but limited to one machine.
- **Supabase** (hosted or self-hosted): Postgres and a good Flutter SDK; the hosted version is the easy fallback if running Appwrite becomes a burden.
- **Split services** (for example Firebase Auth + Neon): rejected because every database rule would have to trust tokens from another vendor.
