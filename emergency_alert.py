import streamlit as st
import numpy as np
import io
import base64
import time
import soundfile as sf
import json
import os
from slack import send_to_slack
import streamlit_antd_components as sac

import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stylable_container import stylable_container 
from streamlit_lottie import st_lottie


# Constants for sound generation
SAMPLE_RATE = 44100  # Sample rate in Hz
SOUND_DURATION = 3   # Duration of the sound in seconds
FREQUENCY_LA = 440   # Frequency of the sound in Hz

# Path to the shared state file
STATE_FILE = 'shared_state.json'

# Function to read the shared state from a file
def read_shared_state():
    """Read the current shared state from a JSON file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return json.load(file).get('alarm_triggered', False)
    return False

# Function to update the shared state in a file
def update_shared_state(alarm_status):
    """Update the shared state in a JSON file with the given alarm status."""
    with open(STATE_FILE, 'w') as file:
        json.dump({'alarm_triggered': alarm_status}, file)

# Function to generate a 440 Hz sine wave
def generate_sound():
    """Generate a 440 Hz sine wave for the alarm sound."""
    t = np.linspace(0, SOUND_DURATION, int(SAMPLE_RATE * SOUND_DURATION), False)
    note_la = np.sin(FREQUENCY_LA * t * 2 * np.pi)
    return note_la, SAMPLE_RATE

# Function to autoplay sound in the Streamlit app
def autoplay_sound(sound_data, sample_rate):
    """Autoplay a sound in the Streamlit app."""
    virtual_file = io.BytesIO()
    sf.write(virtual_file, sound_data, sample_rate, format='OGG')
    virtual_file.seek(0)
    media_bytes = virtual_file.read()
    media_str = f"data:audio/ogg;base64,{base64.b64encode(media_bytes).decode()}"
    media_html = (
        '<audio autoplay class="stAudio">'
        '<source src="' + media_str + '" type="audio/ogg">'
        'Your browser does not support the audio element.'
        '</audio>'
    )

    media_placeholder = st.empty()
    media_placeholder.empty()
    time.sleep(0.1)
    media_placeholder.markdown(media_html, unsafe_allow_html=True)

# Streamlit Interface Setup
def setup_streamlit_ui():
    
    """Set up the Streamlit User Interface for the Emergency Physician Alert System."""
    add_logo("https://i.imgur.com/z31fTmc.png")
    st.title('Emergency Physician Alert')

    current_state = read_shared_state()

    if not current_state:
        st.write("Get help immediately. Your emergency is our emergency.")
        st.warning("""
        **Having an emergency? We're here to help:**
        
        Click the 'Trigger Alarm' button below to alert all on-call physicians and a physician will be in contact within seconds
        """, icon="🚨")

    st_autorefresh(interval=1500, key="autorefresh")

    if not current_state and st.button('Trigger Alarm', type="primary", use_container_width=True):
        update_shared_state(True)
        send_to_slack(message="Emergency alarm triggered!")
        st.toast('Alarm is being triggered! Please wait...', icon='✅')
        st.experimental_rerun()

    if current_state:
        sac.alert(label='Emergency in progress', description='Emergency occurring! Please check your CCT Zoom console immediately!', color='red', radius='lg', banner=sac.Banner(play=True, direction='right', speed=100))

        if st.button("Reset Alarm", type="primary", use_container_width=True):
            update_shared_state(False)
            send_to_slack(message="Emergency resolved!")
            st.toast('Alarm is being reset! Please wait...', icon='✅')
            time.sleep(.5)
            st.toast('Check your CCT Zoom immediately', icon='🚨')            
            st.experimental_rerun()
            
        # with stylable_container(
        #     key="lottie-container",
        #     css_styles="""
        #         {
        #             margin: auto; 
        #             max-width: 500px;
        #         }
        #         """,
        # ):
        #     st_lottie("https://lottie.host/45d0253a-991e-4f4e-84fb-3da1e0c39b45/tQxpYzj73L.json", key="lottie")
        
        components.html(
            """
            <style>
                .centered {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                }
            </style>
            <div class="centered">
                <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
                <dotlottie-player src="https://lottie.host/dcbf42cd-ac70-4538-ace1-f536c079840d/qCoiARmqQr.json" background="transparent" speed="1" style="width: 500px; height: 500px" direction="1" mode="normal" loop autoplay></dotlottie-player>
            </div>
            """,
            height=500,
        )
        sound_data, sample_rate = generate_sound()
        autoplay_sound(sound_data, sample_rate)
    else:
        st.success('Alarm not triggered.')
        st.session_state['alarm_triggered'] = False 

if __name__ == '__main__':
    setup_streamlit_ui()
