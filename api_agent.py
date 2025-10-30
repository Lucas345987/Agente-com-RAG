import asyncio
import os
from pyexpat import model

from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.os import AgentOS

from dotenv import load_dotenv
load_dotenv()

knowledge= Knowledge(vector_db=ChromaDb(collection="pdf_agents", path="tmp/chromadb", persistent_client=True))


db = SqliteDb(db_file="tmp/agno.db")

agent = Agent(
    id="Agents_de_SMC",
    instructions="Voce deve chamar o usuario de senhor e buscar informações no pdf.",
    model=Groq(
        id="openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_KEY_API")),
    db=db,
    enable_user_memories=True,
    knowledge=knowledge,
    markdown=True,
    num_history_runs=5,
    debug_mode=True,
)

agent_os = AgentOS(
    name="Professor de SMC",
    agents=[agent]
)

app = agent_os.get_app()

if __name__ == "__main__":
    pdf_reader = PDFReader()
    knowledge.add_content(
        name="Smart Money",
        path="smc.pdf",
        skip_if_exists=True,
        reader=pdf_reader,
    )
    agent_os.serve(app="api_agent:app",reload=True)

    