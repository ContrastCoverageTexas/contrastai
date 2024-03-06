import streamlit as st
import openai
import time
from my_pdf_lib import get_index_for_pdf
from key_check import check_for_openai_key
from streamlit_extras.stylable_container import stylable_container
from streamlit_pills import pills
import pdfplumber
import requests
import os
import io


# Template for the chat prompt with instructions for the AI
prompt_template = """
You are a contrast reaction management technician advisor, specialized in assisting with the assessment and treatment of contrast reactions. Your role is to support physicians, patients, and technicians by providing up-to-date information, guidance, and leadership in managing these reactions. You work for Contrast Coverage Texas, a provider of on-site and remote on-demand contrast supervision. You operate in an outpatient setting and work under a Contrast Coverage Texas Supervising Physician. Your first step is always to inform the Contrast Coverage Texas physician in the event of a reaction.

You should be conversational. Ask questions and give short, clear responses to their specific problems. Always end your statement with a directly linked follow up question. If there is a suspected reaction, ensure that you treat the situation like an emergency priority.

When interacting, remain calm and clear, asking follow-up questions when details are insufficient. Offer reminders and tips relevant to the situation, and take a step-by-step approach to management. Recommend courses of action and relevant medications to consider. Your expertise is crucial, and you lead with authority in this field.

Your contrast media reaction training content is:
    {pdf_extract}
"""

def get_file_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download file from {url}. Status code: {response.status_code}")
        return None

# URLs to the GitHub-hosted files
logo_icon_url = 'https://github.com/ContrastCoverageTexas/contrastai/blob/main/Files/logo-240.png?raw=true'
# user_icon_url = 'https://github.com/ContrastCoverageTexas/contrastai/blob/main/Files/patient-avatar.png?raw=true'
physician_icon_url = 'https://github.com/ContrastCoverageTexas/contrastai/blob/main/Files/physician-avatar.png?raw=true'

# Initialize CCT Logo
logo_icon = get_file_from_github(logo_icon_url)
# Initialize User Icon
# user_icon = get_file_from_github(user_icon_url)
# Initialize Physician Icon
physician_icon = get_file_from_github(physician_icon_url)

def guide_bot():
    # Setting the API key for OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Setting the title of the app
    st.title("AI Contrast Care Guide")

    # Introduction text for the app
    st.write(
        "Your Contrast Media Companion: Empowering Technicians & Patients for Safe Imaging."
    )

    # Initialize 'is_expanded' in session state for expander control
    if 'is_expanded' not in st.session_state:
        st.session_state['is_expanded'] = True

    # Initialize session state for 'selected'
    if 'selected' not in st.session_state:
        st.session_state['selected'] = None

    # Initialize session state for 'clear_flag'
    if 'clear_flag' not in st.session_state:
        st.session_state['clear_flag'] = False

    if 'prompt' not in st.session_state:
        st.session_state['prompt'] = [{"role": "system", "content": "none"}]

    if is_selected_in_prompt(st.session_state['selected'], st.session_state['prompt']):
        st.session_state['selected'] = None
        st.session_state['clear_flag'] = True
    
    # Information box with usage instructions

    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                # background-color: rgba(26, 149, 179, 0.33);
            }
            """,
    ):
        with st.expander(
            "**Curious where to start? Choose a prompt to get started ↓**", expanded=st.session_state['is_expanded']
        ):
            # st.info("""
            # 1. Prepare a patient for contrast administration
            # 2. Review the symptoms of anaphylaxis
            # 3. Get immediate response steps for a suspected incident
            # 4. Review follow-up steps once a patient is stabilized
            # """)
            selected_temp = pills(
                "Choose a prompt to get started",
                options=[
                    "Prepare a patient for contrast administration",
                    "Review the symptoms of anaphylaxis",
                    "Give me the immediate response steps for a suspected incident",
                    "Review follow-up steps once a patient is stabilized",
                ],
                clearable=True,
                index=None,
                label_visibility="collapsed",
            )
            if selected_temp:
                st.session_state['selected'] = selected_temp
                st.session_state['is_expanded'] = False


# Caching function to create a vectordb from PDFs for performance efficiency
@st.cache_resource
def train_guide(files):
    with st.spinner("Training on the latest data & best practices..."):
        vectordb = get_index_for_pdf(files, openai.api_key)
    st.success("Success! Contrast Care Guide is ready!")
    return vectordb

# Function to download and read PDF files from GitHub using pdfplumber
def read_pdf_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with io.BytesIO(response.content) as pdf_bytes:
                with pdfplumber.open(pdf_bytes) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()
            return text
        else:
            st.error(f"Failed to download file from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred while downloading and reading the PDF file: {e}")
        return None

# List of GitHub URLs for PDF files
pdf_urls = [
    "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training1.pdf",
    "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training2.pdf",
    "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training3.pdf",
    "https://raw.githubusercontent.com/ContrastCoverageTexas/contrastai/main/Files/Training4.pdf"
]

# Loading the vectordb on app load, if not already in session
if "vectordb" not in st.session_state:
    binary_data = [read_pdf_from_github(url) for url in pdf_urls]
    st.session_state["vectordb"] = train_guide(binary_data)


    # Retrieving or initializing the chat prompt from session state
    prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

    # Displaying chat history
    for message in prompt:
        if message["role"] != "system":
            # Determine the avatar based on the message role
            avatar = physician_icon if message["role"] == "user" else logo_icon
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])

    # User input for questions
    question = st.chat_input("Message Contrast Care Guide...")

    # Ensure the OpenAI key is available
    check_for_openai_key()

    if question:
        st.session_state['selected'] = None
        st.session_state['is_expanded'] = False
        handle_user_question(question)
        # vectordb = st.session_state.get("vectordb", None)

        # # Searching the vectordb for relevant content
        # search_results = vectordb.similarity_search(question, k=5)
        # pdf_extract = "/n ".join([result.page_content for result in search_results])

        # # Updating the prompt with the new content
        # prompt[0] = {
        #     "role": "system",
        #     "content": prompt_template.format(pdf_extract=pdf_extract),
        # }
        # prompt.append({"role": "user", "content": question})

        # # Displaying the user's question
        # with st.chat_message("user", avatar=physician_icon):
        #     st.write(question)

        # # Placeholder for the assistant's response
        # with st.chat_message("assistant", avatar=logo_icon):
        #     botmsg = st.empty()

        # # Calling ChatGPT and streaming the response
        # response = []
        # for chunk in openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo-1106", messages=prompt, stream=True
        # ):
        #     text = chunk.choices[0].get("delta", {}).get("content")
        #     if text:
        #         response.append(text)
        #         botmsg.write("".join(response).strip())

        # # Updating the chat history with the assistant's response
        # prompt.append({"role": "assistant", "content": "".join(response).strip()})
        # st.session_state["prompt"] = prompt

    if st.session_state['selected'] and not st.session_state['clear_flag'] and not is_selected_in_prompt(st.session_state['selected'], st.session_state['prompt']):
        st.session_state['is_expanded'] = False
        handle_user_question(st.session_state['selected'])
        st.session_state['selected'] = None

    # Clear conversation button
    if st.button("Clear Conversation"):
        clear_conversation()
        st.session_state['selected'] = None
        st.session_state['clear_flag'] = True 

    if st.session_state['clear_flag']:
        st.session_state['selected'] = None
        st.session_state['clear_flag'] = False  # Reset the flag after handling clear conversation


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

def is_selected_in_prompt(selected, prompt):
    """
    Check if the selected string is already present in the prompt.

    Args:
    selected (str): The selected string to be checked.
    prompt (list): The list of prompt messages, each a dictionary.

    Returns:
    bool: True if selected is in prompt, False otherwise.
    """
    return any(message.get('content') == selected for message in prompt)
 
