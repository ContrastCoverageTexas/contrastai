import time
from emergency_alert import setup_streamlit_ui as alertpage
from emergency_alert import read_shared_state
import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
from streamlit_extras.add_vertical_space import add_vertical_space
from overviewtest import overview
from home_page import home
from app_logo import add_logo
from bottom_footer import footer
from contrast_guide import guide_bot
from patient_assistant import patient_support_bot


# Set up the main configuration of the Streamlit app
st.set_page_config(
    layout="wide", page_title="Contrast Coverage Texas", page_icon="👨‍⚕️"
)

# st.button("clear", on_click=st.cache_resource.clear())


# Function to initialize the navigation index based on URL query parameters
def initialize_navigation_index():
    query_params = st.experimental_get_query_params()
    # Define a mapping from URL routes to index values
    url_to_index = {
        "/home": 0,
        "/emergency-alert": 2,
        "physician-contrast-guide": 3,
        "patient-assistant": 4,
    }

    # Check if 'nav' parameter is in the query and set index accordingly
    if "nav" in query_params and query_params["nav"][0] in url_to_index:
        return url_to_index[query_params["nav"][0]]
    else:
        return 0  # Default to home page


# callback to update query param on selectbox change


def update_params():
    # Assuming 'menu' variable holds the current selection from sac.menu
    route_mapping = {
        "home": "home",
        "emergency alert": "emergency-alert",
        "physician contrast guide": "physician-contrast-guide",
        "patient assistant": "patient-assistant",
    }
    new_route_mapping = "/" + route_mapping.get(st.session_state["menu_selection"])
    st.session_state["stx_router_route"] = new_route_mapping
    st.experimental_set_query_params(nav=new_route_mapping)
    time.sleep(0.1)  # Needed for URL param refresh

    index_mapping = {
        "home": 0,
        "emergency alert": 2,
        "physician contrast guide": 3,
        "patient assistant": 4,
    }
    new_index_mapping = index_mapping.get(st.session_state["menu_selection"])
    st.session_state["index"] = new_index_mapping


def navigate_home():
    with st.container():
        home()
        update_params()


def navigate_alert():
    with st.container():
        alertpage()
        update_params()


def navigate_guide():
    with st.container():
        guide_bot()
        update_params()


def navigate_patient_bot():
    with st.container():
        patient_support_bot()
        update_params()


# Set up router details
@st.cache_resource(hash_funcs={"_thread.RLock": lambda _: None})
def init_router():
    return stx.Router(
        {
            "/": navigate_home,
            "/home": navigate_home,
            "/emergency-alert": navigate_alert,
            "/physician-contrast-guide": navigate_guide,
            "/patient-assistant": navigate_patient_bot,
        }
    )


router = init_router()

# Custom CSS for styling the Streamlit app
st.markdown(
    """
    <style>
    .stApp .main .block-container {
        padding-top: 30px;
    }
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2) {
        padding-top: 70px;
    }
    iframe {
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize session state for navigation index
if "index" not in st.session_state:
    st.session_state["index"] = initialize_navigation_index()

# # Initialize session state for navigation index
# if "index" not in st.session_state:
#     st.session_state["index"] = 3
#     update_params_via_url()

emergency_color = "green"
emergency_text = "Off"

# Update the emergency color based on the session state
emergency_color = "green" if read_shared_state() == False else "red"
emergency_text = "Off" if read_shared_state() == False else "On"


# Sidebar content and navigation
with st.sidebar.container():
    # Adding the logo to the sidebar
    add_logo(
        "https://i.imgur.com/FyRgZES.png",
        # height=225,
    )

    # Tags for menu items
    modified = sac.Tag("Modified", color="blue", bordered=False)
    new = sac.Tag("New", color="green", bordered=False)
    deprecated = sac.Tag("Deprecated", color="orange", bordered=False)

    # Sidebar title
    st.markdown("")
    st.subheader("ContrastAI")

    menu = sac.menu(
        items = [
            sac.MenuItem(label="home", icon="house-fill"),
            sac.MenuItem(
                "products",
                icon="box-fill",
                children=[
                    sac.MenuItem(
                        "emergency alert",
                        icon="megaphone-fill",
                        tag=sac.Tag(emergency_text, emergency_color, bordered=False),
                    ),
                    sac.MenuItem("physician contrast guide", icon="heart-pulse-fill"),
                    sac.MenuItem("patient assistant", icon="wechat"),
                    sac.MenuItem("incident writer", icon="stars", disabled=True),
                ],
            ),
            sac.MenuItem(type="divider"),
            sac.MenuItem(
                "Guides",
                type="group",
                children=[
                    sac.MenuItem(
                        "Physician Onboarding Guide",
                        icon="person-check",
                        disabled=True,
                        href="https://contrastcoveragetexas.com",
                    ),
                    sac.MenuItem(
                        "Imaging Center Onboarding Guide",
                        icon="hospital",
                        disabled=True,
                        href="https://contrastcoveragetexas.com/",
                    ),
                ],
            ),
            sac.MenuItem(type="divider"),
            sac.MenuItem(
                "reference",
                type="group",
                children=[
                    sac.MenuItem(
                        "Visit our website",
                        icon="window",
                        href="https://contrastcoveragetexas.com",
                    ),
                    sac.MenuItem(
                        "Terms & Conditions",
                        icon="clipboard2-check-fill",
                        href="https://www.contrastcoveragetexas.com/terms-and-conditions",
                    ),
                    sac.MenuItem(
                        "Privacy Policy",
                        icon="clipboard2-check-fill",
                        href="https://www.contrastcoveragetexas.com/privacy-policy",
                    ),
                ],
            ),
        ],
        format_func="title",
        size="small",
        key="menu_selection",
        # Update router with new params
        on_change=update_params,
        index=st.session_state["index"],
        open_all=True,
    )

router.show_route_view()

add_vertical_space(3)

# st.button("clear", on_click=st.cache_resource.clear())
# c1, c2, c3 = st.columns(3)

# with c1:
#     st.header("Current route")
#     current_route = router.get_url_route()
#     st.write(f"{current_route}")
# with c2:
#     st.header("Set route")
#     new_route = st.text_input("route")
#     if st.button("Route now!"):
#         router.route(new_route)
# with c3:
#     st.header("Session state")
#     st.write(st.session_state)

# Adding the footer to the app
footer()

