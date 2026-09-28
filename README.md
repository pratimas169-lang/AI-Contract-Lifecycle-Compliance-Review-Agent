# AI Contract Lifecycle & Compliance Review Agent

An Agentic AI system for contract compliance review using RAG, Gemini, n8n, Streamlit, Python, FAISS and SQL Server.

1. Project Overview

This project is an AI-powered contract review agent that understands contract clauses, retrieves relevant company policies and supporting documents, identifies potential compliance deviations, and recommends the next step for human review.

The system combines Retrieval-Augmented Generation (RAG), LLM-based analysis, agent decision logic, workflow orchestration and human-in-the-loop approval.

2. Business Problem

Contract reviews often require manual comparison of contract clauses against company policies and approved requirements.

This can result in:

- Time-consuming document review
- Difficulty identifying policy deviations
- Inconsistent review processes
- Manual evidence gathering
- Limited auditability of review decisions

 3. Business Objective

The objective is to automate and support contract compliance review by:

- Understanding contract clauses
- Retrieving relevant policies and documents
- Comparing contract terms against approved requirements
- Identifying potential deviations
- Generating evidence-grounded review summaries
- Routing decisions for human approval
- Maintaining an audit trail

 4. Solution Architecture

```text
Contract / Review Request
          ↓
      Streamlit
          ↓
     n8n Workflow
          ↓
 Python RAG Pipeline
          ↓
 FAISS + Embeddings
          ↓
 Retrieve Contract & Policy Evidence
          ↓
       Gemini LLM
          ↓
    Agent Decision
          ↓
   Human Review
          ↓
    Workflow Action
          ↓
      SQL Server
     Audit Record


5. Agentic Workflow
The agent follows a multi-step workflow:
Intake
Understand
Retrieve
Analyze
Summarize
Recommend
Human Review
Workflow Update
Audit Logging


6. RAG Approach

The system uses Retrieval-Augmented Generation (RAG).
Relevant contract and policy sections are converted into embeddings using Sentence Transformers and stored in FAISS indexes.
For a review request, relevant evidence is retrieved and provided to Gemini before generating the review.
This helps ground the generated review in the available contract and policy evidence.


7. Human-in-the-Loop

The AI agent does not make the final business/legal decision independently.
When a policy deviation is identified, the workflow routes the case for human review.
Available decisions include:

APPROVE_EXCEPTION
REQUEST_FURTHER_REVIEW
REJECT_EXCEPTION
The human decision is then used to determine the workflow status and is recorded in SQL Server.

8.Technology Stack
Python
Jupyter Notebook
Gemini
Google GenAI SDK
Sentence Transformers
FAISS
n8n
Streamlit
SQL Server
SSMS
GitHub


9. Project Files
File / Folder	Purpose
AI_Contract_Review_Agent.ipynb	RAG, embeddings and contract review development
contract_review_runner.py	Python agent service
app.py	Streamlit application
SQL/	SQL Server database and audit queries
.gitignore	Prevents sensitive/local files from being committed

10. Example Review Scenario
The sample contract contains a 90-day payment term.
The approved payment policy specifies a standard payment period of 30 calendar days.
The agent identifies the difference, generates an evidence-grounded review, recommends human review, and routes the decision through the workflow.

11. Audit Trail
The system records review information in SQL Server, including:
Review timestamp
Review question
Agent decision
Recommended next step
Reviewer
Reviewer decision
Workflow action
Workflow status
Contract evidence
Policy evidence
Agent review

12. Key Project Outcome
The project demonstrates an end-to-end Agentic AI workflow combining:
RAG + LLM + Agent Decision Logic + Human Approval + Workflow Orchestration + Database Audit

13. Future Scope
Support additional contract types
Expand policy and clause libraries
Add more compliance checks
Add document upload processing for multiple formats
Add analytics and review dashboards
Improve automated evaluation and monitoring
