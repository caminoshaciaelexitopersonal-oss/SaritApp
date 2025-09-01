from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent

from app.core.config import settings
from app.tools.herramientas_marketing import (
    generate_post_caption,
    suggest_relevant_hashtags,
    create_content_idea,
)

# 1. Tools
# The agent will have access to the tools we defined.
tools = [generate_post_caption, suggest_relevant_hashtags, create_content_idea]

# 2. LLM
# We use a powerful model for agentic behavior.
llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model_name="gpt-4", temperature=0)

# 3. Prompt Template
# The prompt defines the agent's persona and instructions.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and creative marketing assistant, part of the 'Sarita' platform. "
            "Your name is 'Sargento de Marketing'. "
            "Your goal is to help users create excellent social media content. "
            "When asked to generate a 'post', you should first generate a caption, then suggest hashtags. "
            "If the user is looking for ideas, use the content idea tool."
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

def get_marketing_sargento_graph():
    """
    Constructs and returns the AgentExecutor graph for the Marketing Sargeant.
    """
    # 4. Agent
    # Create the agent by combining the LLM, prompt, and tools.
    agent = create_openai_tools_agent(llm, tools, prompt)

    # 5. Graph (AgentExecutor)
    # The AgentExecutor is the runtime for the agent.
    graph = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return graph
