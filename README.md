# 🔊 ChatGPT Voice Bot (Django + RAG + Groq + HuggingFace)

ChatGPT Voice Bot is a Django-based AI voice assistant that answers user queries using **voice input/output**, **RAG (Retrieval-Augmented Generation)**, **Groq API**, and **HuggingFace Embeddings**. It retrieves information from uploaded PDFs and speaks the answers in your preferred language.

---

## ✅ Features

- 🎤 Voice input from the user
- 📢 Voice output using gTTS or Azure
- 📄 RAG using PDF documents
- 🤖 LLM-powered answers using Groq + HuggingFace
- 🌐 Django web interface
- 🗣️ Multilingual greeting (e.g., Telugu)
- 🧠 Smart response using similarity + keyword matching
- 💬 Rolling chat-style UI

---

## ⚙️ Requirements

```bash
python>=3.8
Django>=4.0
transformers
sentence-transformers
faiss-cpu
PyMuPDF
gTTS
pygame
SpeechRecognition
pyaudio
langchain
groq
