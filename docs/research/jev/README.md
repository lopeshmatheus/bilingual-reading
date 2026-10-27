# Jev accuracy check (not yet run)

Jev is TypeSafe AI's "System One" decision model (announced 2026-09-15): it returns typed yes/no, choice and score answers with probabilities, and never writes text. The plan is to use it behind a replaceable decision step to pick real Chunks from candidate phrases. All published figures are the vendor's own.

`run_test.py` asks Jev, for 48 short sentences (8 each in English, Spanish, French, German, Italian and Portuguese; half real idioms or phrasal verbs, half ordinary phrases), whether a given phrase is a Chunk, and reports accuracy per language. `probe.py` makes a single call to check access.

## Status

Not run. On 2026-10-20 the session's network policy refused the connection to `api.typesafe.ai`, so no request was sent and there are no results. It needs `api.typesafe.ai` in the environment's allowed domains.

## Running it

The API key is read from the `TYPESAFE_API_KEY` environment variable and is never stored in this repo:

    TYPESAFE_API_KEY=... python3 -I docs/research/jev/run_test.py

The endpoint, model name (`jev-latest`) and request shape come from third-party articles (DataCamp, LangChain), and the `Authorization: Bearer` header is a guess; check them against TypeSafe's own documentation.
