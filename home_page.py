import databutton as db
import streamlit as st
import streamlit_antd_components as sac
from streamlit_extras.add_vertical_space import add_vertical_space 
from streamlit_extras.stylable_container import stylable_container 
import streamlit.components.v1 as components
import extra_streamlit_components as stx


def add_rounded_image(image_url, width="100%", height=400, radius=20):
    """Add an image with rounded corners to a Streamlit app.

    Args:
        image_url (str): URL of the image.
        width (str, optional): Width of the image. Defaults to "100%".
        height (str, optional): Height of the image. Defaults to "auto".
        radius (int, optional): Radius of the rounded corners. Defaults to 20.
    """
    st.markdown(
        f"""
        <style>
            .rounded-image {{
                background-image: url({image_url});
                width: {width}px;
                height: {height}px;
                background-size: contain;
                border-radius: {radius}px;
            }}
        </style>
        <div class="rounded-image"></div>
        """,
        unsafe_allow_html=True
    )


def redirect(index=0):
    st.session_state['index'] = index


def home():
    
    
    # user = db.user.get()
    # name = user.name if user.name else "you"

    image_url = "https://i.imgur.com/Wde1wB2.png"
    
    # HTML and CSS for responsive image with fade-in effect, max width, and centering
    fade_in_image_html = f"""
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            .fade-in-image-container {{
                text-align: center; /* Center the image container */
            }}
            .fade-in-image {{
                animation: fadeIn 3s ease-in-out forwards; /* Fade-in effect */
                opacity: 0;  /* Start with the image invisible */
                max-width: 550px; /* Maximum width */
                width: 100%; /* Responsive width */
                height: auto; /* Maintain aspect ratio */
                margin: 0 auto; /* Center the image */
            }}
        </style>
        <div class="fade-in-image-container">
            <img src="{image_url}" alt="Responsive image" class="fade-in-image">
        </div>
    """
    
    st.markdown(fade_in_image_html, unsafe_allow_html=True)

    add_vertical_space(3)
    # st.title(f"Hello, {name}!")

    sac.divider(label='Features & Tools', icon='lightning-charge-fill', align='center')

    col1, col2 = st.columns([1,1])    
    
    with col1:
        # html_lottie_content = """
        # <style>
        #     .centered {
        #         display: flex;
        #         justify-content: center;
        #         align-items: center;
        #         width: 100%;  /* Fill the width */
        #         height: 100%;
        #         padding-top: 0px;
        #         padding-bottom: 0px;
        #         flex-direction: column;
        #         overflow: hidden;
        #     }
        
        #     /* Style for rounded borders on the dotLottie player */
        #     dotlottie-player {
        #         border-radius: 15px; /* Rounded corners */
        #         overflow: hidden; /* Ensure the corners remain rounded */
        #         box-shadow: 0px 0px 10px rgba(0,0,0,0.5); /* Optional: Adds a shadow for depth */
        #     }
        # </style>
        # <div class="centered">
        #     <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
        #     <dotlottie-player src="https://lottie.host/9723cf13-81ed-425b-ab89-6e1c9b5f36e3/1ni6plGRVA.json" background="transparent" speed="1" style="width: 600px; height: 300px;" loop autoplay></dotlottie-player>
        # </div>
        # """
        
        # # Display the HTML content in Streamlit
        # components.html(html_lottie_content, height=300)  # Adjust height as needed
        
        step = sac.steps(
            items=[
                sac.StepsItem(title='Trigger immediate emegency requests', description='Our redundant, failsafe alarm system ensures an immediate response and top notch patient care'),
                sac.StepsItem(title='Get AI-assisted contrast reaction assistance', description='Provide physicians & technicians with real-time support based on the latest leading practices & research'),
                sac.StepsItem(title='Comfort your patients 24/7', description='Our post-reaction tool makes sure no customer question goes unanswered, even after they leave your facility'),
                sac.StepsItem(title='Document effortlessly', description='Our priorietary, HIPAA compliant incident writer ensures that all patient details are captured and securely stored '),
            ], placement='vertical', dot=True, direction='vertical'
        )
    with col2:
        if f'{step}' == 'Trigger immediate emegency requests':
            add_rounded_image("https://i.imgur.com/WubNHgP.png", height=400, radius=30)
        if f'{step}' == 'Get AI-assisted contrast reaction assistance':
            add_rounded_image("https://i.imgur.com/r1PLtll.png", height=400, radius=30)
        if f'{step}' == 'Comfort your patients 24/7':
            add_rounded_image("https://i.imgur.com/oH1H2by.png", height=400, radius=30)
        # st.write(f'{step}')
 


    add_vertical_space(5)
    sac.divider(label='Have questions?', icon='patch-question', align='center')

    sac.tags([
    sac.Tag(label='ContrastCoverageTexas.com', icon='gear', color='geekblue', link='https://contrastcoveragetexas.com'),
    sac.Tag(label='‪(832) 974-0401', icon='google', color='geekblue', link='tel:18329740401'),
    sac.Tag(label='info@ContrastCoverageTexas.com', icon='twitter', color='geekblue', link='mailto:info@contrastcoveragetexas.com'),
    sac.Tag(label='@ContrastTexas', icon='twitter', color='geekblue', link='https://twitter.com/ContrastTexas'),
], align='center', direction='horizontal')
    
    # sac.buttons([
    #     sac.ButtonsItem(label='google', icon='google', color='#25C3B0', href='https://ant.design/components/button')
    # ], format_func='title', align='center', shape='round', type='dashed')
