# Pipeline Presets

Named, reusable bundles of retrieval/generation/ingestion knobs that
configure every pipeline-aware endpoint in Trix (chat, search, memories,
graph, hierarchy, agent/consolidate, and more).

## Goal

Learn how to:

1. Set an account-level default (`agent.set_default_pipeline`)
2. Set a per-space default that beats the account default (`agent.set_space_default_pipeline`)
3. Dry-run the 3-tier resolver without firing a search (`agent.resolve_pipeline`)
4. Observe which preset applied via `X-Pipeline-Name` / `X-Pipeline-Source` response headers

## The 3-tier resolver (ADR-109a)

When any pipeline-aware endpoint serves a request:

```
caller > space > account > none (server fallback)
```

- **caller** — explicit `pipeline=<name>` on the request
- **space** — default stored on the target space
- **account** — default stored on the caller's account
- **none** — no preset applied; server uses its built-in hybrid retrieval

Explicit caller presets always win; the only way to force "no preset" is to
omit `pipeline=` AND have no space / account defaults.

## Prerequisites

- Completed `00_getting_started`
- `TRIX_API_KEY` env var set

## Built-in presets used in this example

The example uses presets shipped with the server (no CRUD required):

- `default` — baseline hybrid retrieval
- `high-recall` — broader retrieval (top_k=40, lower threshold)
- `high-precision` — narrower retrieval (top_k=10, higher threshold)

To create your own preset, use the CLI:

```bash
trix pipeline create --file=./my-preset.json
```

…or `POST /v1/pipeline-presets` with a JSON body conforming to
`pipelineSchema` (see ADR-111).

## Run

```bash
python examples/11_pipeline_presets/main.py           # Synchronous
python examples/11_pipeline_presets/async_example.py  # Asynchronous
```

## What to read next

- [`/docs/pipelines`](https://trixdb.com/docs/pipelines) — user-facing docs
- ADR-111: pipeline preset schema + registry
- ADR-109a: 3-tier resolver + account/space defaults
- ADR-112: ingestion namespace (mega_summary, scoped_fact, etc.)
