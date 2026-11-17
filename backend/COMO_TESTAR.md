# Como correr e testar o backend localmente

## 1. Instalar as dependências

```bash
cd backend
python -m venv venv
source venv/bin/activate      # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configurar as variáveis de ambiente

```bash
cp .env.example .env
```

Depois abre o `.env` e cola o `Account SID` e o `Auth Token` que guardaste
no Passo 4 da Etapa 1.

## 3. Correr o servidor localmente

```bash
uvicorn main:app --reload --port 8000
```

Se abrires `http://localhost:8000` no browser, deves ver:
`{"status": "ok", "mensagem": "Agente de triagem a funcionar."}`

## 4. Expor o servidor à internet com ngrok (para a Twilio conseguir chamá-lo)

A Twilio precisa de um URL público para enviar as mensagens recebidas.
Como o teu servidor está só na tua máquina, usa o ngrok para criar um túnel:

1. Instala o ngrok: https://ngrok.com/download
2. Cria conta gratuita e autentica: `ngrok config add-authtoken SEU_TOKEN`
3. Com o servidor a correr (passo 3), abre outro terminal e corre:
   ```bash
   ngrok http 8000
   ```
4. O ngrok vai mostrar um URL do tipo `https://abcd1234.ngrok-free.app`

## 5. Configurar o webhook na Twilio

1. Vai à consola da Twilio → Messaging → Try it out → WhatsApp Sandbox Settings
2. No campo "WHEN A MESSAGE COMES IN", cola:
   `https://abcd1234.ngrok-free.app/webhook`
3. Método: `HTTP POST`
4. Guarda (Save)

## 6. Testar

Envia uma mensagem pelo WhatsApp para o número do sandbox.
Deves receber a resposta fixa definida em `main.py`.

> Nota: o URL do ngrok muda sempre que reinicias o túnel (na versão
> gratuita). Sempre que isso acontecer, tens de actualizar o webhook
> na consola da Twilio outra vez.
