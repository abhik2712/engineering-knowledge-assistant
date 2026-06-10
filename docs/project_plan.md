# Engineering Knowledge Assistant: Project Plan

## Project Name
Engineering Knowledge Assistant over Code, Design Docs, Logs, and Incidents

## Objective
Build a production-style RAG system that helps engineers answer technical questions by retrieving relevant information from a real codebase, design documents, operational logs, and incident reports.

The initial corpus is based on the open-source Prometheus repository, along with synthetic design docs, logs, and incident reports created for RAG experimentation.

## Target Users
- Backend engineers
- SREs
- Platform engineers
- New team members onboarding to a codebase
- Engineers debugging production incidents

## Supported Question Types
1. Code understanding
   - Which file or package handles a feature?
   - Where is a specific component implemented?

2. Architecture understanding
   - How does scraping work?
   - How does service discovery connect to scraping?
   - How does local TSDB storage work?

3. Debugging and incident analysis
   - Why did a scrape target fail?
   - Why did Prometheus fail to reload config?
   - Why were remote write samples dropped?

4. Source-grounded explanations
   - Explain the issue using retrieved logs, incident reports, and design docs.

## Data Sources
| Source Type | Path | Purpose |
|---|---|---|
| Code repo | `data/code_repo/prometheus` | Real production-grade source code and docs |
| Design docs | `data/design_docs` | Self-written architecture summaries |
| Logs | `data/logs` | Synthetic operational failure logs |
| Incidents | `data/incidents` | Synthetic postmortem-style incident reports |

## Non-Goals
- Do not modify Prometheus source code.
- Do not use confidential company documents.
- Do not build a generic PDF chatbot.
- Do not focus only on UI before retrieval quality is evaluated.

## Final Expected Features
- Multi-source ingestion
- Source-aware chunking
- Metadata-based retrieval
- Hybrid dense + keyword search
- Reranking
- Source citations
- Evaluation using golden questions
- Basic API or UI
- Dockerized deployment

## Success Criteria
The project is successful if the assistant can:
1. Retrieve relevant chunks from multiple source types.
2. Answer with citations.
3. Explain why a source was used.
4. Handle missing context gracefully.
5. Show measurable improvement from baseline retrieval to hybrid retrieval.
