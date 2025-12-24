
# Multimodal Healthcare Prior Authorization System

## Overview
This system combines Vision-Language Models (VLMs), RAG, and Agentic Workflows to automate prior authorization.

## Components
1. **Vision Agent:** OCRs and structures medical images.
2. **Librarian Agent:** Retrieves policy rules from vector DB.
3. **Decider Agent:** Reasons between patient data and policy rules.
4. **Writer Agent:** Drafts approvals or appeals.

## Setup
1. `python -m venv venv`
2. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` (and add your API keys)

