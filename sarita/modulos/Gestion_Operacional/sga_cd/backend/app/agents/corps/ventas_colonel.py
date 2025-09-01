import os
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable, RunnableParallel
from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app import crud

# --- Configuration ---
VECTOR_STORE_PATH = "SGA-CD-FASTAPI-BACKEND/app/agents/knowledge_base/faiss_index_sales"
DEFAULT_TONE_OF_VOICE = "Amistoso, profesional y servicial."

def get_sales_agent_executor(db: Session, inquilino_id: int):
    """
    Creates and returns the executor for the Sales Agent.
    This agent is now configured dynamically based on the tenant's Brand Profile.
    """
    # --- 1. Get Brand Profile ---
    brand_profile = crud.brand.get_brand_profile(db, inquilino_id=inquilino_id)
    tone_of_voice = brand_profile.tone_of_voice if brand_profile else DEFAULT_TONE_OF_VOICE

    # --- 2. Set up the LLM ---
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o", temperature=0)

    # --- 3. Set up the Retriever ---
    if not os.path.exists(VECTOR_STORE_PATH):
        print("ADVERTENCIA: El índice del almacén de vectores no se encontró.")
        class DummyRetriever(Runnable):
            def invoke(self, input, config=None): return []
        retriever = DummyRetriever()
    else:
        embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever()

    # --- 4. Define the Prompt Template ---
    template = """
    Eres un asistente de ventas experto para una plataforma de software llamada SGA-CD.
    Tu objetivo es responder a las preguntas de los usuarios para ayudarles a entender el producto y animarles a registrarse.

    **Instrucción de Tono de Voz:** Debes adoptar el siguiente tono en todas tus respuestas:
    ---
    {tone_of_voice}
    ---

    Utiliza la siguiente información de la documentación interna para basar tus respuestas.
    Si la información no contiene la respuesta, di amablemente que no tienes esa información.
    No inventes respuestas. Sé conciso y servicial.

    Contexto de la documentación:
    {context}

    Pregunta del usuario:
    {question}

    Respuesta del Asistente de Ventas:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # --- 5. Create the RAG Chain ---
    # This setup allows us to pass 'tone_of_voice' through to the prompt.
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
            "tone_of_voice": lambda x: tone_of_voice  # Pass the fetched tone of voice
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

# The global 'sales_agent_executor' is removed.
# It will now be created on-demand by the calling service.
