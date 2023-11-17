import streamlit as st
import os
import json
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

# Function to initialize your chatbot
def initialize_chatbot():
    # Set API keys (already set in your environment)
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["SERPAPI_API_KEY"] = ""

    # Step 2: Create a JSON 'weather_agent.json' with the following metadata
    weather_agent = {
      "load_from_llm_and_tools": True,
      "_type": "conversational-react-description",
      "prefix": "Assistant is a large language model trained for forecasting weather.\n\nAssistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives.\nAssistant should only obtain knowledge and take actions from using tools and never on your own.\nTOOLS:\n------\n\nAssistant has access to the following tools: ",
      "suffix": "Please make decisions based on the following policy: \n- If the user is asking for a weather forecast use the Weather Forecast tool\n- If the user does not provide a location, ask before checking for weather\n- Apologize if the user is angry or showing frustration\n- Answer with a friendly and professional tone.\n- Always end a response with a follow up question like 'what else can i help you with?', unless the user shows gratitude.\nBegin!\n\nPrevious conversation history:\n{chat_history}\n\nNew input: {input}\n{agent_scratchpad}",
      "ai_prefix": "AI Agent",
      "human_prefix": "Human"
    }

    # Define the path to the local file where you want to save the JSON data
    file_path = r"C:\Users\307164\Desktop\Weather Chat Bot\weather_agent.json"

    # Write the JSON data to the file
    with open(file_path, "w") as json_file:
        json.dump(weather_agent, json_file, indent=2)

    print(f"JSON data has been saved to {file_path}")

    # Initialize tools and memory
    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="Weather Forecaster",
            func=search.run,
            description="useful for answering weather forecast questions"
        ),
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = OpenAI(temperature=0)
    agent_chain = initialize_agent(tools, llm=llm, verbose=True,
                                   agent_path=file_path,
                                   memory=memory)
    return agent_chain

# Streamlit App
def main():
    st.title("Weather Forecast Chatbot")

    # Initialize chatbot
    agent_chain = initialize_chatbot()

    # User input
    user_input = st.text_input("Ask a question about the weather:")

    if user_input:
        # Here, integrate your chatbot logic
        response = agent_chain.run(input=user_input)
        st.write(response)

if __name__ == "__main__":
    main()
