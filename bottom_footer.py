import streamlit as st

# Define the footer
def footer():
    """Create a simple footer using Markdown."""
    
    footer = """
    <style>
    footer {
        visibility: hidden;
    }
    
    footer:after {
        content:'goodbye'; 
        visibility: visible;
        display: block;
        position: fixed;
        background-color: rgba(240, 240, 246, 1);
        height 30px;
        padding: 5px;
        top: 2px;
    }
    
    a:link , a:visited {
        color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness */
        background-color: rgba(240, 240, 246, 1);
        text-decoration: none;
        text-align: center;
    }
    
    a:hover, a:active {
        color: #0283C3; /* theme's primary color */
        background-color: rgba(240, 240, 246, 1);
        text-decoration: underline;
        text-align: center;
    }
    </style>
    
    <p style="text-align: center; bottom: 0; left: 0; background: rgba(240, 240, 246, 1); position: fixed; width: 100%; height: 30px; margin-bottom: 0; padding-top: 5px; padding-bottom: 40px; color: grey; box-sizing: border-box;">
        Built by <a href="https://contrastcoveragetexas.com/" target="_blank">Contrast Coverage Texas</a>
    </p>
    """
    st.markdown(footer, unsafe_allow_html=True)
