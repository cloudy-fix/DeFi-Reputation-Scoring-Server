# DeFi Reputation Scoring Server Architecture

## Purpose

Event-driven DeFi wallet reputation scoring microservice.

## Stack

Python, FastAPI, Kafka, Docker, Pandas, Pydantic

## System Context

```mermaid
flowchart LR
    User["Wallet transaction events"] --> App["FastAPI service, Kafka service, AI scoring model"]
    App --> Data["Kafka topics, transaction payloads, scoring features"]
    App --> Output["Success/failure scoring events and API response"]
    Data --> Output
```
## Runtime Workflow

```mermaid
flowchart TD
    S1["Receive wallet event"] --> S2["Validate payload"]
    S2["Validate payload"] --> S3["Compute reputation score"]
    S3["Compute reputation score"] --> S4["Publish success or failure event"]
    S4["Publish success or failure event"] --> S5["Expose API health/result endpoints"]
```
## Production Readiness Notes

- Keep secrets in environment variables and commit only .env.example templates.
- Keep generated files, dependency folders, caches, and local databases out of version control.
- Run the GitHub Actions workflow before presenting or deploying changes.
- Update this document when the source layout, dependencies, or deployment model changes.

## Review Checklist

- Architecture diagram matches current source files.
- Workflow diagram matches the main user or data path.
- README links to this architecture document.
- CI workflow validates the project on every push and pull request.

