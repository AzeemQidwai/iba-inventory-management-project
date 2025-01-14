import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv('../.env')

# Get the OpenAI API key from the environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    st.error("OpenAI API key not found in environment variables.")
    st.stop()

# Initialize the database
db = SQLDatabase.from_uri("sqlite:///../db/database.db")

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Initialize the SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Read the prompt from a text file
with open('../notebooks/conf/prompt.txt', 'r') as file:
    prompt_text = file.read()

# Retrieve and format the prompt template
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5) + ' ' + prompt_text

# Create the agent executor
agent_executor = create_react_agent(
    llm,
    toolkit.get_tools(),
    state_modifier=system_message
)

# Streamlit Chat UI
st.title("SQL Database Chat")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for chat
if user_input := st.chat_input("Ask a question about the database..."):
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the user's input
    with st.chat_message("assistant"):
        try:
            processing_placeholder = st.empty()
            processing_placeholder.markdown("Processing...")
            events = agent_executor.stream(
                {"messages": [("user", user_input)]},
                stream_mode="values",
            )
            
            # Capture the response dynamically
            final_message_content = ""
            for event in events:
                final_message_content = event["messages"][-1].content
                #st.markdown(final_message_content)

            if final_message_content:
                processing_placeholder.markdown(final_message_content)

            if final_message_content == "":
                final_message_content = "I'm sorry, I couldn't understand your query."
            
            # Save assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": final_message_content})

        except Exception as e:
            st.markdown(f"An error occurred: {e}")
