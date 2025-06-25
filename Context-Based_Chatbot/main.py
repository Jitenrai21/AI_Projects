from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
import uuid

from dotenv import load_dotenv
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# In-memory sessions
chat_sessions = {}

# Custom app-level API key
PROGRAM_API_KEY = os.getenv("PROGRAM_API_KEY")

# Available personas
persona_options = {
    "Isaac Newton": "Mathematician and physicist",
    "Marie Curie": "Pioneering scientist in radioactivity",
    "William Shakespeare": "English playwright and poet",
    "Adam Smith": "Father of modern economics",
    "Alan Turing": "Father of computer science"
}

# FastAPI app
app = FastAPI()

# JSON request schema
class ChatRequest(BaseModel):
    persona: str
    message: str

@app.post("/chat")
async def chat(req: Request, data: ChatRequest, authorization: str = Header(None)):
    # 1. Validate API key
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    if token != PROGRAM_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized API key.")

    # 2. Validate persona
    if data.persona not in persona_options:
        raise HTTPException(status_code=400, detail="Invalid persona.")

    # 3. Auto-generate session ID per client (example using IP)
    client_ip = req.client.host
    session_id = f"{client_ip}-{data.persona}"
    
    # 4. Use or create a Gemini session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])

    # 5. Build prompt
    with open('prompt_template.txt', 'r') as file:
            prompt_template = file.read().strip()

    # Format the prompt with persona details
    persona_instruction = prompt_template.format(
            persona_name=data.persona,
            persona_description=persona_options[data.persona]
        )
    prompt = persona_instruction + "\n\nUser: " + data.message

    # persona_instruction = (
    #     f"You are {data.persona}, a {persona_options[data.persona]}. "
    #     f"Please respond in their style and voice, as if you are them."
    # )
    # prompt = f"{persona_instruction}\n\nUser: {data.message}"

    try:
        response = chat_sessions[session_id].send_message(prompt)
        return JSONResponse(content={"response": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# uvicorn main:app --reload