from os import execlpe
from pandas.io.xml import preprocess_data
import requests
# from pprint import pprint
import json
import streamlit as st


AGENT_ID="Agents_de_SMC"
ENDPOINT = f"https://agente-com-rag.onrender.com/agents/{AGENT_ID}/runs"

def get_response_stream(message: str):
    response = requests.post(
        url=ENDPOINT,
        data={
            "message":message,
            "stream":True
        },
        stream=True
    )
    for line in response.iter_lines():
        if line:
            if line.startswith(b"data: "):
                data = line[6:]
                try:
                    event = json.loads(data)
                    yield event
                except json.JSONDecodeError:
                    continue




st.set_page_config(page_title="Agente SMC")

st.title("Chat Smart Money Concpts")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("process"):
            with st.expander(lobel="process", expanded=False):
                st.json(msg["process"])

        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem!"):
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placerholder = st.empty()
        full_response = ""
    
    for event in get_response_stream(prompt):
        event_type = event.get("event", "")
        
        if event_type == "ToolCallStarted":
            tool_name = event.get("tool", {}).get("tool_name")
            with st.status(f"Executando: {tool_name} ...", expanded=True):
                st.json(event.get("tool",{}).get("tool_args",{}))

        elif event_type == "RunContent":
            content = event.get("content", "")
            if content:
                full_response += content
                response_placerholder.markdown(full_response + "")
    
    response_placerholder.markdown(full_response)
    # Salvar a resposta do assistente (full_response) e o histórico na session_state
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
    })





# def get_streaming_response(message: str):
#     for event in get_response_stream(message):
#         event_type = event.get("event", "")

#         if event_type== "RunStarted":
#             print("Execução iniciada!")
#             print("-"*50)
        
#         elif event_type == "RunContent":
#             content = event.get("content", "")
#             if content:
#                 print(content, end="", flush=True)
        
#         elif event_type == "ToolCallStarted":
#             tool = event.get("tool",{})
#             tool_name = tool.get("tool_name", "Unknown")
#             tool_args = tool.get("tool_args", {})
#             print(f"TOOL INICIADA:{tool_name}")
#             print(f"ARGUMENTOS:{json.dumps(tool_args, indent=2)}")

#             print("_"*50)

#         elif event_type == "RunCompleted":
#             print("Execução Concluida!")
#             metrics = event.get("metrics", {})
#             if metrics:
#                 print(f"METRICAR: {json.dumps("metrics", indent=2)}")
#                 print("_"*50)




# if __name__ == "__main__":
#     message = input("Digite uma mensagem!")
#     get_streaming_response(message)
#     # while True:
#     #     message = input("Digite uma mensagem!")
#     #     get_streaming_response(message)


# """
# RunStarted
# RunContent
# ToolCallStarted
# ToolCallCompleted
# RunContent
# RunContentCompleted
# MemoryUpdateStarted
# MemoryUpdateCompleted
# RunCompleted

# """
