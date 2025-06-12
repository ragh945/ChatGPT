# voicebot/views.py

import re
from django.shortcuts import render
from .rag_pdf import build_pdf_vectorstore
from .voice_handler import voice_to_text, speak_text

rag_chain = None

# Clean RAG responses: remove markdown, format bullets

def clean_response(text):
    if isinstance(text, dict) and "result" in text:
        text = text["result"]
    text = re.sub(r"\*{1,2}", "", text)
    lines = text.strip().split("\n")
    bullet_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("-") or line.startswith("•") or re.match(r"^[\d]+\.", line):
            content = line.lstrip("-•0123456789. ").strip()
            bullet_lines.append(f"<li>{content}</li>")
        else:
            bullet_lines.append(f"<p>{line}</p>")

    if bullet_lines:
        return "<ul>" + "".join(bullet_lines) + "</ul>"
    return text

def chatbot_home(request):
    global rag_chain
    name = request.session.get("name")
    api_key = request.session.get("api_key")
    user_input = ""
    response = ""

    if request.method == "POST":
        # Step 1: Enter name
        if "name" in request.POST:
            name = request.POST.get("name").strip()
            if name:
                request.session["name"] = name
                response = f"Hi {name}, please enter your Groq API key."
                speak_text(response)

        # Step 2: Enter API key
        elif "api_key" in request.POST:
            api_key = request.POST.get("api_key").strip()
            if api_key:
                request.session["api_key"] = api_key
                response = f"API key saved! Now upload your PDF."
                speak_text(response)

        # Step 3: Upload PDF
        elif "pdf" in request.FILES:
            pdf_file = request.FILES["pdf"]
            try:
                rag_chain = build_pdf_vectorstore(pdf_file, api_key)
                response = "PDF uploaded successfully. Ask your question now."
                speak_text(response)
            except Exception as e:
                response = f"Failed to process PDF: {str(e)}"
                speak_text(response)

        # Step 4: Ask a voice question
        elif "ask" in request.POST:
            if not rag_chain:
                response = "Please upload a PDF first."
                speak_text(response)
            else:
                user_input = voice_to_text()
                if user_input.strip():
                    try:
                        raw_response = rag_chain.invoke(user_input)
                        response = clean_response(raw_response)
                        speak_text(response)
                    except Exception as e:
                        response = f"Error answering your question: {str(e)}"
                        speak_text(response)
                else:
                    response = "Sorry, I couldn't understand your voice."

    return render(request, "voicebot/home.html", {
        "name": name,
        "api_key": api_key,
        "user_input": user_input,
        "response": response,
    })
