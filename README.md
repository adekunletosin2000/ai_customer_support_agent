✅ PRODUCT REQUIREMENTS DOCUMENT (PRD)

Project Name: AICare – Multi-Agent AI Customer Service System
Team: Tosin Adekunle, Royson Salis, Saurav Pandey, Vatsal Patel
Hackathon Goal: Build a working demo in 2 days.

1. Problem Statement

Businesses struggle with:

Slow customer support response times

High cost of support agents

Inconsistent answers

No 24/7 availability

Difficulty handling repeated questions

Users want fast, accurate, friendly responses to their issues without waiting for a human.

2. Solution Summary

Create a multi-agent AI system that automatically:

Understands user complaints

Looks up answers in knowledge base

Troubleshoots issues

Detects sentiment

Generates natural responses

Escalates when needed

Gives analytics

The system runs through 11 specialized agents controlled by an Orchestrator Agent.

Frontend: Chat UI
Backend: FastAPI
Knowledge Base: JSON + embeddings (FAISS/Pinecone)

3. Target Users
Business Admins

Reduce support cost

Faster customer resolution

Automatically answer FAQs

Customers

Quick help

Simple conversations

No waiting

4. Project Scope (Hackathon Version)
IN SCOPE (Must Deliver)

✔ Basic chat interface
✔ Orchestrator + 11 agents
✔ Knowledge base search
✔ Response generator
✔ Sentiment detection
✔ Troubleshooting flow
✔ Escalation message
✔ Working end-to-end demo

OUT OF SCOPE (Future)

✖ Admin dashboard
✖ API for businesses
✖ Voice support
✖ Role-based admin system

5. User Journey

User sends a message

Orchestrator receives it

Classifier identifies type (billing, tech, account)

Knowledge Search agent fetches relevant answer

Troubleshooting agent provides steps

Sentiment agent checks user frustration

Response generator creates final message

Summarization agent records interaction

Escalation agent triggers if needed

6. System Requirements
Functional Requirements

FR1: System must respond within 3–6s

FR2: Agents must run in sequence

FR3: Orchestrator must connect all agents

FR4: Frontend must show “agent processing steps”

FR5: Knowledge base must support similarity search

Non-Functional Requirements

NFR1: Clean, intuitive UI

NFR2: Low latency

NFR3: Readable code

NFR4: Easy to extend

7. The 11 Agents

Classifier Agent

Intent Agent

Knowledge Search Agent

Response Generator Agent

Sentiment Agent

Troubleshooting Agent

Summarization Agent

Escalation Agent

User Profile Agent

Analytics Agent

Orchestrator Agent

8. Success Criteria

Working demo

Judges see multi-agent collaboration

Smooth UI

Clean architecture

Clear pitch

9. Team Responsibilities
🟦 Vatsal Patel – Architect + Frontend + Orchestrator

UI/UX

Orchestrator

Integration

Architecture diagram

🟩 Royson Salis – Backend + API Routing + DevOps

FastAPI endpoints

Routing engine

Knowledge base setup

Deployment

🟨 Saurav Pandey – AI Agents Developer

All 11 agents

Prompt engineering

Agent chaining logic

🟧 Tosin Adekunle – Testing + Demo + Pitch

End-to-end validation

Demo scripts

Pitch deck

UX polish
