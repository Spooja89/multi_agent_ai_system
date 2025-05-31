# Multi-Agent AI System

## 🚀 Overview

This project is a lightweight multi-agent AI system that accepts inputs in **PDF**, **JSON**, or **Email (text)** formats. It classifies the file format and user intent (Invoice, RFQ, Complaint, etc.), then routes the input to the appropriate processing agent.

Each agent extracts structured data and stores it in a shared memory for traceability and chaining.

---

## 🧠 Agents

### 1. Classifier Agent
- Identifies the **file type** and **intent** using simple rules (or optionally LLM).
- Routes the input to the correct agent.
- Logs metadata into shared memory.

### 2. JSON Agent
- Processes structured JSON documents.
- Extracts and validates required fields.
- Logs any anomalies or missing data.

### 3. Email Agent
- Processes email text files.
- Extracts sender, urgency, and content intent.
- Outputs data in a CRM-ready format.

### 4. PDF Agent *(Bonus)*
- Extracts text from PDF documents using `pdfplumber`.
- Provides summaries or stats (e.g., word count).

---

## 🗃️ Shared Memory

A lightweight **SQLite memory store** that keeps:
- Entry ID
- Filepath
- File type & intent
- Metadata (e.g., raw data, extracted values)
- Timestamp

Used across agents to ensure shared context and traceability.

---

## 📁 Folder Structure

