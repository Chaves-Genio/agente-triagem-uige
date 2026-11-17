"""
Backend do Agente de Triagem de Sintomas - Uige
Projecto de Inteligencia Artificial I - UNIKIVI

Este ficheiro contem apenas a ligacao ao WhatsApp via Twilio.
A logica de triagem (regras + LLM) sera adicionada na Etapa 4.
"""

import os
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

load_dotenv()  # le as variaveis do ficheiro .env

app = FastAPI(title="Agente de Triagem - Uige")


@app.get("/")
def health_check():
    """Endpoint simples para confirmar que o servidor esta no ar."""
    return {"status": "ok", "mensagem": "Agente de triagem a funcionar."}


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Endpoint que a Twilio chama sempre que alguem envia uma mensagem
    de WhatsApp para o numero do sandbox.

    A Twilio envia os dados como form-data (nao JSON), por isso usamos
    request.form() em vez de request.json().
    """
    form_data = await request.form()

    numero_remetente = form_data.get("From", "")        # ex: "whatsapp:+244..."
    mensagem_recebida = form_data.get("Body", "").strip()

    print(f"[DEBUG] Mensagem de {numero_remetente}: {mensagem_recebida}")

    # --- Por agora, resposta fixa de confirmacao ---
    # Na Etapa 4 isto vai ser substituido pela logica de triagem.
    resposta_texto = (
        "Ola! Sou o agente de triagem do Uige. "
        "Recebi a tua mensagem: \"" + mensagem_recebida + "\". "
        "Em breve vou poder ajudar-te a perceber se os teus sintomas "
        "precisam de atencao urgente."
    )

    # A Twilio espera uma resposta em formato TwiML (XML simples)
    twiml_resposta = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{resposta_texto}</Message>
</Response>"""

    return Response(content=twiml_resposta, media_type="application/xml")
