# Autonomous Multi-Agent Market Intelligence System

An autonomous AI-powered market intelligence platform that researches markets, companies, and emerging trends using specialized AI agents, real-time web research, evidence validation, automated re-research, and RAG-powered memory.

The system transforms a natural-language business question into a structured, evidence-backed intelligence report through a multi-stage agentic workflow.

---

## Overview

Traditional market research requires manually searching multiple sources, collecting information, validating findings, and synthesizing the results.

This project automates that workflow using a multi-agent architecture.

A user provides a market intelligence question such as:

> "Analyze the electric vehicle market in India in 2025."

The system then:

1. Retrieves relevant historical knowledge from RAG memory.
2. Creates a research plan using a Planner Agent.
3. Assigns specialized tasks to Market, Company, and Trend Agents.
4. Performs web research using Tavily.
5. Converts raw research into structured findings.
6. Validates findings using a Critic Agent.
7. Automatically re-researches invalid findings.
8. Aggregates validated evidence.
9. Generates analytical insights using an Analyst Agent.
10. Produces a structured final intelligence report.
11. Stores the generated report in vector memory for future retrieval.

---

## Key Features

### 🤖 Multi-Agent Research

The system uses specialized agents for different research dimensions:

- **Planner Agent** — converts the user query into research tasks.
- **Market Agent** — researches market size, growth, segmentation, geography, and market dynamics.
- **Company Agent** — researches relevant companies, competitive positioning, and company-level information.
- **Trend Agent** — identifies emerging trends, technologies, adoption patterns, and market developments.
- **Critic Agent** — evaluates the quality and reliability of research findings.
- **Analyst Agent** — synthesizes validated evidence into strategic insights.
- **Report Generator Agent** — converts analytical insights into a structured market intelligence report.

---

### 🔎 Web Research

The system performs real-time web research using **Tavily**.

Research tasks are executed against external sources and converted into structured findings before entering the validation stage.

The research pipeline considers:

- Relevance
- Evidence quality
- Quantitative accuracy
- Completeness
- Source quality

---

### 🛡️ Evidence Validation

A dedicated Critic Agent evaluates every research finding before it is used for analysis.

The critic checks:

- Whether the finding answers the assigned research task
- Whether sufficient evidence supports the claim
- Whether quantitative information is properly supported
- Whether important information is missing
- Whether the source quality is appropriate

Findings that fail validation can be sent back through an automated re-research loop.

---

### 🔄 Automated Re-Research

The system is not a simple linear pipeline.

When a finding is considered invalid, the workflow can:

```text
Research
   ↓
Critic
   ↓
Invalid
   ↓
Re-Research
   ↓
Critic Again
