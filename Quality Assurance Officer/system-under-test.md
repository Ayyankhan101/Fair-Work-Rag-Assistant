# System under test

## Scope

The release target is the application in the repository root. `System Under Test (SUT)/Discard` is reference material and is not executable release evidence.

Mandatory source scope:

- 122 industry and occupation Awards from the Fair Work Ombudsman A-Z list;
- National Employment Standards content current for the release date;
- source identity, amendment date, and checksum for every ingested file.

Enterprise and public-sector awards may be indexed, but they must be labelled as an additional corpus. They cannot replace a missing mandatory Award.

## Runtime components

| Component | File | Responsibility | Main failure mode |
|---|---|---|---|
| UI | `src/app.py` | Gradio chat, input checks, route display | startup or provider errors |
| Router | `src/router.py` | select CAG, RAG, or combined path | wrong context path |
| Award/topic detection | `src/config.py` | deterministic aliases and topics | false match or missed Award |
| CAG cache | `src/cag.py` | load NES text for NES questions | stale, empty, or damaged text |
| Ingestion | `src/ingest.py` | parse PDFs and NES into chunks | lost clauses or wrong metadata |
| Semantic store | `src/vectorstore.py` | TurboVec build, load, and search | stale or duplicated index |
| BM25 | `src/bm25_retriever.py` | lexical retrieval | tokenization misses |
| Filtered retrieval | `src/filtered_retriever.py` | Award and topic filtering | empty or contaminated result set |
| Hybrid retrieval | `src/hybrid_retriever.py` | reciprocal-rank fusion | wrong rank or unstable identity |
| Answer chain | `src/rag.py` | context assembly and Groq call | unsupported answer or citation |
| Store builder | `build_store.py` | cache and resumable store build | duplicate or irreproducible store |

## Request flow

1. `src/app.py` rejects empty input and input over 2,000 characters.
2. `route_question()` returns CAG, RAG, or combined.
3. CAG uses the NES cache only.
4. RAG uses filtered retrieval when an Award or topic is detected. Other questions use BM25 plus semantic retrieval.
5. Combined routing supplies NES cache content and Award retrieval.
6. `src/rag.py` formats up to 4,000 retrieved characters and calls Groq.
7. The answer must contain Answer, Award/NES Reference, Clause/Section, Explanation, and Note fields.

## Persisted state inspected on 2026-07-27

| Item | Value |
|---|---:|
| Chunks | 16,692 |
| Award chunks | 16,665 |
| NES chunks | 27 |
| Distinct `source_file` values | 131 |
| Distinct `award_name` values | 129 |
| Exact-text duplicate groups | 388 |
| Extra chunks in duplicate groups | 1,251 |
| Mandatory Award IDs missing | MA000095, MA000121 |

`MA000002` occurs in chunk text, but its chunks are labelled `Workplace Relations Act 1996`, not `Clerks - Private Sector Award`. This is a corpus identity failure.

## External dependencies

| Boundary | Data sent or loaded | Required QA |
|---|---|---|
| Fair Work Ombudsman and Commission | Award and NES source material | date, ID, checksum, and update checks |
| Groq | user question and retrieved context | secret handling, timeout, rate limit, model identity |
| FastEmbed | questions and chunks locally | deterministic model version and dimensions |
| TurboVec | embeddings and metadata | store count and version agreement |
| Git LFS | store and document-cache artifacts | materialization and checksum checks |
| Gradio | user questions and answers | input limits, error handling, binding policy |

## Trust boundaries

- User questions are untrusted.
- Retrieved text is untrusted data, not model instructions.
- `.env` and `GROQ_API_KEY` are secrets.
- Pickle files can execute code while loading. `data/docs_cache.pkl` is trusted only when its repository origin and checksum are verified.
- Persisted evaluation JSON is evidence only when it names the commit, corpus, model, prompt, and run time.
