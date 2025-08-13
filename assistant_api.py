"""
creating gpt doctor assistant using fastAPI
make memory for each user

"""
import os
from typing import Dict
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from lanchain_chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


# define env

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# start fastAPI
app = FastAPI(title = "Doctor Assistant API")


#LLM Configuration
llm = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temprature = 0.7,
    openai_api_key = api_key
)

# memory conf.

user_memories: Dict[str, ConversationBufferMemory] = {}

# request and  response  
class ChatRequest(BaseModel): # input for chat message
    name:str
    age:int
    message:str

class ChatResponse(BaseModel): # output for chat message
    response: str


# chat enpoint
@app.post("/chat", response_model = ChatResponse)
async def chat_with_doctor(request:ChatRequest):
    try:
        # bring memory if there is if not create
        if request.name not in user_memories:
            user_memories[request.name] = ConversationBufferMemory(return_messages = True)
        
        memory = user_memories[request.name]

        # create intro message
        if len(memory.chat_memory.messages) == 0:
            intro = (
                f"You are a doctor assistant. Patient's {request.name} and Age {request.age}"
                "Want to talk about health issues"
                "give and some advice"
                "call its name"
            )
            memory.chat_memory.add_user_message(intro)
        
        # make chain with llm and memory

        conversation = ConversationChain(
            llm,
            memory,
            verbose = False
        )
        bot_reply = conversation.predict(input = request.message)

        print(f"\n Memory: ")
        for idx,m in enumerate(memory.chat_memoory.messages, start =1): # start 1 index kısmı 
            print(f"{idx:02d}. {m.type.upper(): {m.content}}")
        print("-------------------------------------------------")

        return ChatResponse(request = bot_reply)
    except Exception as e:
        raise HTTPException(status_code = 500,detail = str(e))
    
    






