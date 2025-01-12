from django.shortcuts import render
from .models import InventoryTable
from .forms import MaterialSearchForm

def search_material(request):
    form = MaterialSearchForm()
    results = None

    if request.method == 'POST':
        form = MaterialSearchForm(request.POST)
        if form.is_valid():
            material_code = form.cleaned_data['material_code']
            # Query the database for the top 10 rows matching Material Code
            results = InventoryTable.objects.filter(material_code=material_code)[:10]  
    return render(request, 'search_material.html', {'form': form, 'results': results})


import pandas as pd
from django.shortcuts import render
from .models import InventoryTable
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from nixtla import NixtlaClient

API_KEY = "nixak-fDHJF9pfGpbvHEXbPqVGTwqIgBzv6xgDt4cJzqyjkj7ZAqFVue636fBAZZ5oqM57op6szHjbdTrUxbLg"  # Replace with your TimeGPT API Key

nixtla_client = NixtlaClient(
    api_key = API_KEY
)

def forecast_material(request):
    forecast_data = []  # Initialize as an empty list for GET requests
    forecast_plot = None
    material_code = None

    if request.method == 'POST':
        material_code = request.POST.get('material_code')
        horizon = int(request.POST.get('horizon', 1))  # Default horizon is 1 if not provided

        # Fetch data for the material code
        data = InventoryTable.objects.filter(material_code=material_code).values()
        if data:
            # Convert to pandas DataFrame
            df = pd.DataFrame(list(data))

            # Rename columns
            df.rename(columns={'date': 'ds', 'material_issued': 'y'}, inplace=True)

            # Prepare the data for TimeGPT
            df['ds'] = pd.to_datetime(df['ds'])  # Ensure datetime format
            df['y'] = df['y'].astype(float)  # Ensure numerical format  
            df = df[['ds', 'y']]  # Keep only relevant columns

            # Call TimeGPT for forecasting
            # timegpt = TimeGPT()  # Initialize your TimeGPT API or library
            forecast_data = nixtla_client.forecast(df=df, h=horizon, level=[80, 90])


            buffer = BytesIO()
            nixtla_client.plot(df, forecast_data, max_insample_length=365, level=[80, 90]).savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # Encode the image to base64
            forecast_plot = base64.b64encode(image_png).decode('utf-8')

            # Rename forecast DataFrame columns
            forecast_data.rename(
                columns={
                    "TimeGPT-hi-80": "timegpt_hi_80",
                    "TimeGPT-hi-90": "timegpt_hi_90",
                    "TimeGPT-lo-80": "timegpt_lo_80",
                    "TimeGPT-lo-90": "timegpt_lo_90",
                },
                inplace=True,
            )
            forecast_data = forecast_data.to_dict('records')

    return render(request, 'forecast_material.html', {
        'forecast_data': forecast_data,
        'forecast_plot': forecast_plot,
        'material_code': material_code
    })


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Get the OpenAI API key and LangSmith API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGCHAIN_API_KEY')

if openai_api_key is None:
    raise ValueError("OpenAI API key not found in environment variables")

# Connect to your SQLite database
db_path = os.path.abspath(os.path.join(BASE_DIR, 'db', 'database.db'))
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Initialize the LLM and toolkit
llm = ChatOpenAI(model="gpt-4o-mini")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Read the custom prompt from a text file
with open(os.path.join(BASE_DIR, 'notebooks', 'conf', 'prompt.txt'), 'r') as file:
    prompt_text = file.read()

# Retrieve the base prompt template
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5) + ' ' + prompt_text

# Create the agent executor
agent_executor = create_react_agent(
    llm,
    toolkit.get_tools(),
    state_modifier=system_message
)

# Define the "Talk with Data" view
def talk_with_data(request):
    chat_history = []  # Store the chat history
    user_input = None
    bot_response = None

    if request.method == 'POST':
        # Retrieve user input from the form
        user_input = request.POST.get('user_input', '')

        # Execute the query using the LangChain agent
        events = agent_executor.stream(
            {"messages": [("user", user_input)]},
            stream_mode="values",
        )

        # Capture the final AI message
        final_message = None
        for event in events:
            final_message = event["messages"][-1]

        # Extract and save the AI's response
        if final_message:
            bot_response = final_message.content
            chat_history.append((user_input, bot_response))

    return render(request, 'talk_with_data.html', {
        'chat_history': chat_history,
        'user_input': user_input,
        'bot_response': bot_response,
    })
