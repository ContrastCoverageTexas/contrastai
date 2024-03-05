import streamlit as st
import openai
import time
from streamlit_extras.app_logo import add_logo
from my_pdf_lib import get_index_for_pdf
from key_check import check_for_openai_key

def patient_support_bot():
    
    # Setting the API key for OpenAI
    openai.api_key = db.secrets.get("OPENAI_API_KEY")
    
    #Initialize CCT Logo
    # logo_icon = db.storage.binary.get(key="logo-240")
    user_icon = db.storage.binary.get(key="patient-avatar-png")
    physician_icon = db.storage.binary.get(key="physician-avatar-png")
    
    # Adding a side logo to the Streamlit app
    add_logo("https://i.imgur.com/z31fTmc.png")
    
    # Setting the title of the app
    st.title("AI Patient Discharge Support")
    
    # Introduction text for the app
    st.write("Front-line support for post-contrast reaction management.")
    
    # Information box with usage instructions
    st.warning("""
    **Concerned you might be having a reaction?**
    1. Share your symptoms
    2. Understand your risk profile
    3. Get immediate next steps and support
    """)
    
    # Caching function to create a vectordb from PDFs for performance efficiency
    @st.cache_resource
    def patient_train_guide(files):
        with st.spinner("Training on the latest data & best practices..."):
            patient_vectordb = get_index_for_pdf(files, openai.api_key)
        st.success("Success! Your Patient Discharge Support tool is ready!")
        return patient_vectordb
    
    # Loading the vectordb on app load, if not already in session
    if 'patient_vectordb' not in st.session_state:
        patient_binary_data = [
            db.storage.binary.get("training1-pdf"),
            db.storage.binary.get("training2-pdf"),
            db.storage.binary.get("training3-pdf"),
            db.storage.binary.get("training4-pdf")
        ]
        st.session_state["patient_vectordb"] = patient_train_guide(patient_binary_data)
    
    # Template for the chat prompt with instructions for the AI
    patient_prompt_template = """
    You are a contrast reaction management technician advisor, specialized in assisting with post-discharge patient assessment and treatment of contrast reactions. Your role is to support patients following contrast administration, by providing information and guidance in managing potential follow-up reactions. You work for Contrast Coverage Texas, a provider of on-site and remote on-demand contrast supervision. You operate in an outpatient setting and work under a Contrast Coverage Texas Supervising Physician. Your first step is always to inform the Contrast Coverage Texas physician in the event of an adequately identified reaction.
    
    You should be conversational. Ask questions and give short, clear responses to their specific problems. Always end your statement with a directly linked follow up question. If there is a suspected moderate to severe reaction, ensure that you treat the situation like an emergency priority.
    
    When interacting, remain calm and clear, asking follow-up questions when details are insufficient. Take a step-by-step approach understanding the patients symptoms and coparing them to your knowledge of contrast reactions. Recommend courses of action, especially home courses for mild symptoms, to consider for the patient. It is important to accurately assess the patient. Use tools like 1-10 scales and high, medium, low to assess severity. If unlikely to be a reaction, recommend home-based solutions. Be calm, but be willing to raise flags if the situation warrants it. Remember to use lay-person, non-medical words for medical terms that a patient would not understand. Keep your instructions clear and understandable to a layperson. Your expertise is crucial, and you lead with authority in this field. Make sure that the patient reaches out to Contrast Coverage Texas at ‪(832) 974-0401‬ or incident@ContrastCoverageTexas.com if they are having a reaction. Always provide contact information if you tell the patient to contact Contrast Coverage Texas, but do not make it overly repetitive.
    
    Your contrast media reaction training content is:
        {pdf_extract}
    """
    
    # Retrieving or initializing the chat prompt from session state
    patient_prompt = st.session_state.get("patient_prompt", [{"role": "system", "content": "none"}])
    
    # Displaying chat history
    for message in patient_prompt:
        if message["role"] != "system":
            # Determine the avatar based on the message role
            avatar = user_icon if message["role"] == "user" else physician_icon
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])

    # User input for questions
    patient_question = st.chat_input("Message Patient Discharge AI...")
    
    # Ensure the OpenAI key is available
    check_for_openai_key()
    
    # Handling user questions
    if patient_question:
        patient_vectordb = st.session_state.get("patient_vectordb", None)
    
        # Searching the vectordb for relevant content
        search_results = patient_vectordb.similarity_search(patient_question, k=5)
        pdf_extract = "/n ".join([result.page_content for result in search_results])
    
        # Updating the prompt with the new content
        patient_prompt[0] = {"role": "system", "content": patient_prompt_template.format(pdf_extract=pdf_extract)}
        patient_prompt.append({"role": "user", "content": patient_question})
    
        # Displaying the user's question
        with st.chat_message("user", avatar=user_icon):
            st.write(patient_question)
    
        # Placeholder for the assistant's response
        with st.chat_message("assistant", avatar=physician_icon):
            botmsg = st.empty()
    
        # Calling ChatGPT and streaming the response
        response = []
        for chunk in openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=patient_prompt, stream=True):
            text = chunk.choices[0].get("delta", {}).get("content")
            if text:
                response.append(text)
                botmsg.write("".join(response).strip())
    
        # Updating the chat history with the assistant's response
        patient_prompt.append({"role": "assistant", "content": "".join(response).strip()})
        st.session_state["patient_prompt"] = patient_prompt
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.toast('Clearing conversation! Please wait...', icon='✅')
        time.sleep(1)
        patient_prompt = patient_prompt[:1]
        st.session_state["patient_prompt"] = patient_prompt
        st.experimental_rerun()

