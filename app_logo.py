import streamlit as st

def add_logo(logo_url: str, height: int = 300):
    """
    Add a logo (from logo_url) on the top of the navigation page of a multipage app.

    Args:
        logo_url (str): URL/local path of the logo
        height (int): Height of the logo in pixels
        on_click (function): Function to execute on click event
    """

    logo = f"url({logo_url})"

    # Add background image to sidebar
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height-500}px;
                background-position: 20px 20px;
                background-size: {height}px; /* Set the size of the logo */
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
