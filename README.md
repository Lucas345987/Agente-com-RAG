Agente com RAG
===============

Projeto de agente com Recuperação Aumentada por Geração (RAG) usando Agno, Groq e ChromaDB. O agente lê o PDF `smc.pdf`, indexa o conteúdo e expõe uma API (via FastAPI/Uvicorn). Uma interface em Streamlit consome a API para chat.

Sumário
------
- Visão Geral
- Requisitos
- Instalação
- Configuração (.env)
- Executando a API
- Executando a Interface (Streamlit)
- Estrutura do Projeto

Visão Geral
-----------
- Vetoriza e consulta o PDF `smc.pdf` via `ChromaDb` em `tmp/chromadb`.
- Serve a API em `http://localhost:7777` (conforme utilizado pela interface Streamlit).
- Usa o modelo Groq `openai/gpt-oss-120b` (configure a chave `GROQ_KEY_API`).

Requisitos
----------
- Python >= 3.13
- Git
- (Opcional) Virtualenv/Uv ou sua ferramenta de ambiente preferida

Instalação
----------
1. Clone ou baixe o repositório localmente.
2. (Opcional) Crie e ative um ambiente virtual.
3. Instale as dependências definidas em `pyproject.toml`.

Configuração (.env)
-------------------
Crie um arquivo `.env` na raiz do projeto com:

```
GROQ_KEY_API=SEU_TOKEN_DA_GROQ
```

Executando a API
----------------
Você pode iniciar a API simplesmente executando:

```
python api_agent.py
```

No primeiro start, o PDF `smc.pdf` será lido e indexado (se ainda não existir índice em `tmp/chromadb`). A API será servida por Uvicorn através do Agno AgentOS.

Executando a Interface (Streamlit)
----------------------------------
Em outro terminal, rode a interface de chat:

```
streamlit run servido_tela.py
```

A interface irá se conectar ao endpoint configurado em `servido_tela.py` (por padrão `http://localhost:7777/agents/Agents_de_SMC/runs`).

Estrutura do Projeto
--------------------
- `api_agent.py`: inicializa Agente, Knowledge/Chroma e serve a API.
- `servido_tela.py`: interface Streamlit para chat com o agente.
- `smc.pdf`: fonte de conhecimento a ser indexada.
- `tmp/`: dados persistentes (Chroma e SQLite do Agno).
- `pyproject.toml`: dependências e metadados do projeto.

Licença
-------
Projeto público. Ajuste a licença conforme necessário.


