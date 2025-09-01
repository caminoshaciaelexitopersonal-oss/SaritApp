from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from app.core.config import settings

# Initialize the language model
# We can adjust temperature for more creative responses
llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model_name="gpt-4", temperature=0.7)

class ContentGenerationInput(BaseModel):
    """Input for content generation tools."""
    topic: str = Field(description="The main topic or theme for the content to be generated.")

@tool("generate_post_caption", args_schema=ContentGenerationInput, return_direct=False)
def generate_post_caption(topic: str) -> str:
    """
    Generates a compelling and engaging marketing caption for a social media post
    based on a given topic.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert social media marketer. Your task is to write a captivating post caption."),
        ("human", "Please generate a short, engaging caption for a social media post about: '{topic}'. The caption should be friendly, professional, and include a call to action if appropriate.")
    ])
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return response.content

@tool("suggest_relevant_hashtags", args_schema=ContentGenerationInput, return_direct=False)
def suggest_relevant_hashtags(topic: str) -> list[str]:
    """
    Suggests a list of relevant and trending hashtags for a social media post
    based on a given topic. Returns a comma-separated string of hashtags.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media strategy expert. Your task is to identify the best hashtags for a post."),
        ("human", "Please suggest 5 to 7 relevant and popular hashtags for a post about: '{topic}'. Return them as a single, comma-separated string without the '#' symbol. For example: technology,ai,future,innovation.")
    ])
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    # Clean up the response and return a list of strings
    hashtags = [tag.strip() for tag in response.content.replace("#", "").split(',')]
    return hashtags

@tool("create_content_idea", args_schema=ContentGenerationInput, return_direct=False)
def create_content_idea(topic: str) -> str:
    """
    Generates a creative and unique content idea or angle for a social media post
    based on a given topic.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative content strategist. Your task is to brainstorm a unique idea for a social media post."),
        ("human", "Please generate one creative and specific content idea for a post about: '{topic}'. Describe the idea in one or two sentences.")
    ])
    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return response.content
