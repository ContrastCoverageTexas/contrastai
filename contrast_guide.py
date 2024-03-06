import streamlit as st
import openai
import time
import requests
import os
import io
import pdfplumber
from my_pdf_lib import get_index_for_pdf
from key_check import check_for_openai_key
from streamlit_extras.stylable_container import stylable_container
from streamlit_pills import pills

# Template for the chat prompt with instructions for the AI
prompt_template = """
You are a contrast reaction management technician advisor, specialized in assisting with the assessment and treatment of contrast reactions. Your role is to support physicians, patients, and technicians by providing up-to-date information, guidance, and leadership in managing these reactions. You work for Contrast Coverage Texas, a provider of on-site and remote on-demand contrast supervision. You operate in an outpatient setting and work under a Contrast Coverage Texas Supervising Physician. Your first step is always to inform the Contrast Coverage Texas physician in the event of a reaction.

You should be conversational. Ask questions and give short, clear responses to their specific problems. Always end your statement with a directly linked follow-up question. If there is a suspected reaction, ensure that you treat the situation like an emergency priority.

When interacting, remain calm and clear, asking follow-up questions when details are insufficient. Offer reminders and tips relevant to the situation, and take a step-by-step approach to management. Recommend courses of action and relevant medications to consider. Your expertise is crucial, and you lead with authority in this field.

Your contrast media reaction training content is:
    {pdf_extract}
"""

def download_pdf_binary(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the response status is OK (200)
        if response.status_code == 200:
            # Return the binary content of the PDF
            return response.content
        else:
            # Display an error in Streamlit if the file couldn't be downloaded
            st.error(f"Failed to download file from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Display an error in Streamlit if any exception occurred during the process
        st.error(f"An error occurred while downloading the PDF file: {e}")
        return None
        
# Caching function to create a vectordb from PDFs for performance efficiency
@st.cache_resource
def train_guide(files):
    with st.spinner("Training on the latest data & best practices..."):
        vectordb = get_index_for_pdf(files, openai.api_key)  # Ensure this function is defined to handle bytes-like objects correctly
    st.success("Success! Contrast Care Guide is ready!")
    return vectordb

def setup_app():
    # URLs to the GitHub-hosted files
    pdf_urls = [
        "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training1.pdf",
        "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training2.pdf",
        "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training3.pdf",
        "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training4.pdf"
    ]

    if "vectordb" not in st.session_state:
        binary_data = [download_pdf_binary(url) for url in pdf_urls]
        st.session_state["vectordb"] = train_guide(binary_data)

def is_selected_in_prompt(selected, prompt):
    return any(item.get('content') == selected for item in prompt)

def guide_bot():
    openai.api_key = "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"
    st.title("AI Contrast Care Guide")
    st.write("Your Contrast Media Companion: Empowering Technicians & Patients for Safe Imaging.")

    if 'is_expanded' not in st.session_state:
        st.session_state['is_expanded'] = True

    if 'selected' not in st.session_state:
        st.session_state['selected'] = None

    if 'clear_flag' not in st.session_state:
        st.session_state['clear_flag'] = False

    if 'prompt' not in st.session_state:
        st.session_state['prompt'] = [{"role": "system", "content": "none"}]

    if is_selected_in_prompt(st.session_state['selected'], st.session_state['prompt']):
        st.session_state['selected'] = None
        st.session_state['clear_flag'] = True

    with stylable_container(key="container_with_border", css_styles="{background-color: rgba(26, 149, 179, 0.33);}"):
        with st.expander("**Curious where to start? Choose a prompt to get started ↓**", expanded=st.session_state['is_expanded']):
            selected_temp = pills("Choose a prompt to get started", options=[
                "Prepare a patient for contrast administration",
                "Review the symptoms of anaphylaxis",
                "Give me the immediate response steps for a suspected incident",
                "Review follow-up steps once a patient is stabilized",
            ], clearable=True, index=None, label_visibility="collapsed")
            if selected_temp:
                st.session_state['selected'] = selected_temp
                st.session_state['is_expanded'] = False

def clear_conversation():
    """
    Clears the conversation in the chat, resets the relevant session state, and reloads the prompt template.
    """
    st.toast("Clearing conversation! Please wait...", icon="✅")
    st.session_state['clear_flag'] = True  # Set a flag to indicate conversation is being cleared
    st.session_state["prompt"] = [{"role": "system", "content": "none"}]
    st.session_state['selected'] = None

    time.sleep(1)
    st.experimental_rerun()

def handle_user_question(question):
    vectordb = st.session_state.get("vectordb", None)

    # Searching the vectordb for relevant content
    search_results = vectordb.similarity_search(question, k=5)
    pdf_extract = "\n".join([result.page_content for result in search_results])

    # Updating the prompt with the new content
    prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(pdf_extract=pdf_extract),
    }
    prompt.append({"role": "user", "content": question})

    # Displaying the user's question
    with st.chat_message("user", avatar=physician_icon):
        st.write(question)

    # Placeholder for the assistant's response
    with st.chat_message("assistant", avatar=logo_icon):
        botmsg = st.empty()

    # Calling ChatGPT and streaming the response
    response = []
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106", messages=prompt, stream=True
    ):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text:
            response.append(text)
            botmsg.write("".join(response).strip())

    # Updating the chat history with the assistant's response
    prompt.append({"role": "assistant", "content": "".join(response).strip()})
    st.session_state['selected'] = None
    st.session_state["prompt"] = prompt
    
setup_app()
 
