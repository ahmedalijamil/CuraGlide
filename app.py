import urllib.parse
import streamlit as st

from core.case_lab import (
    answer_student_question,
    generate_case,
    review_reasoning,
)

from core.hospital_finder import find_hospitals
from core.patient_mode import render_patient_mode


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="CuraGlide",
    page_icon="🏥",
    layout="wide",
)


# ==============================
# CURAGLIDE GLOBAL THEME
# ==============================

st.markdown("""
<style>

    /* =========================
       MAIN BACKGROUND
       ========================= */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #061A2B 0%,
                #073B4C 45%,
                #075E54 100%
            );
        color: #F5FFFF;
    }

    .main {
        background: transparent;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #041725 0%,
                #063B45 55%,
                #075E54 100%
            );
    }

    section[data-testid="stSidebar"] * {
        color: #F5FFFF !important;
    }


    /* =========================
       HEADINGS
       ========================= */

    h1, h2, h3 {
        color: #F5FFFF !important;
        font-weight: 700;
    }

    p, label, span {
        color: #E8FFFF;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #D62828,
                #B91C1C
            ) !important;

        color: white !important;

        border: 2px solid #FF6B6B !important;

        border-radius: 12px !important;

        font-weight: 700 !important;

        padding: 0.65rem 1rem;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #EF4444,
                #C81E1E
            ) !important;

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px rgba(255, 80, 80, 0.35);
    }

    .stButton > button:active {
        transform: translateY(0);
    }


    /* =========================
       INPUT BOXES
       ========================= */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {

        /* ACTUAL TEXT TYPED BY USER */
        color: #38BDF8 !important;

        -webkit-text-fill-color: #38BDF8 !important;

        background-color:
            rgba(255, 255, 255, 0.10) !important;

        border:
            1px solid
            rgba(150, 255, 245, 0.35) !important;

        border-radius: 10px;
    }


    /* Input while typing */

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {

        color: #38BDF8 !important;

        -webkit-text-fill-color: #38BDF8 !important;

        border:
            2px solid
            #5EEAD4 !important;

        box-shadow:
            0 0 12px
            rgba(94, 234, 212, 0.25);
    }


    /* Placeholder */

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    .stNumberInput input::placeholder {

        color: #94A3B8 !important;

        opacity: 1 !important;
    }


    /* =========================
       SELECT BOXES
       ========================= */

    div[data-baseweb="select"] > div {
        background-color:
            rgba(255, 255, 255, 0.10);

        border-color:
            rgba(150, 255, 245, 0.35);

        color: white;
    }


    /* =========================
       CARDS / CONTAINERS
       ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(4, 31, 43, 0.55);

        border:
            1px solid
            rgba(94, 234, 212, 0.20);

        border-radius: 16px;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.20);
    }


    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color:
            rgba(94, 234, 212, 0.25);
    }


    /* =========================
       PROGRESS BAR
       ========================= */

    div[data-testid="stProgress"] > div > div {
        background:
            linear-gradient(
                90deg,
                #14B8A6,
                #5EEAD4
            );
    }


    /* =========================
       SUCCESS / ALERTS
       ========================= */

    div[data-testid="stAlert"][data-baseweb="notification"] {
        border-radius: 12px;
    }


    /* =========================
       LINKS
       ========================= */

    a {
        color: #5EEAD4 !important;
    }


    /* =========================
       CODE / MONOSPACE
       ========================= */

    code {
        color: #99F6E4;
    }

</style>
""", unsafe_allow_html=True)


# ==============================
# SESSION STATE
# ==============================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "case" not in st.session_state:
    st.session_state.case = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "review" not in st.session_state:
    st.session_state.review = None


# ==============================
# NAVIGATION
# ==============================

def navigate(page):
    st.session_state.page = page
    st.rerun()


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown("# 🏥 CuraGlide")

    st.caption(
        "Your well-being in every step."
    )

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        navigate("Home")

    if st.button(
        "👤 Patient Mode",
        use_container_width=True
    ):
        navigate("Patient Mode")

    if st.button(
        "🏥 Hospital Finder",
        use_container_width=True
    ):
        navigate("Hospital Finder")

    if st.button(
        "🧪 Case Lab",
        use_container_width=True
    ):
        navigate("Case Lab")


# ==============================
# HOME
# ==============================

if st.session_state.page == "Home":

    st.title("🏥 CuraGlide")

    st.subheader(
        "Your well-being in every step — accessed from a single touch."
    )

    st.write(
        "CuraGlide is a health-information and learning platform "
        "designed to help users understand health concerns, find "
        "nearby hospitals, and explore clinical-style cases."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 👤 Patient Mode")

        st.write(
            "Answer simple questions about your health and receive "
            "an AI-generated health-information analysis."
        )

        if st.button(
            "Open Patient Mode →",
            use_container_width=True
        ):
            navigate("Patient Mode")

    with col2:

        st.markdown("### 🏥 Hospital Finder")

        st.write(
            "Find hospitals based on a location and open directions "
            "through Google Maps."
        )

        if st.button(
            "Open Hospital Finder →",
            use_container_width=True
        ):
            navigate("Hospital Finder")

    st.write("")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### 🧪 Case Lab")

        st.write(
            "Generate clinical-style educational cases and practice "
            "reasoning through them."
        )

        if st.button(
            "Open Case Lab →",
            use_container_width=True
        ):
            navigate("Case Lab")

    with col4:

        st.markdown("### 💙 About CuraGlide")

        st.write(
            "CuraGlide provides educational health information and "
            "does not replace a qualified healthcare professional."
        )


# ==============================
# PATIENT MODE
# ==============================

elif st.session_state.page == "Patient Mode":

    render_patient_mode()


# ==============================
# HOSPITAL FINDER
# ==============================

elif st.session_state.page == "Hospital Finder":

    st.title("🏥 Hospital Finder")

    st.write(
        "Enter a location to search for nearby hospitals."
    )

    location = st.text_input(
        "Location",
        placeholder="Enter city, area, or location"
    )

    if st.button(
        "🔎 Find Hospitals",
        use_container_width=True
    ):

        if not location.strip():

            st.warning(
                "Please enter a location first."
            )

        else:

            with st.spinner(
                "Searching for hospitals..."
            ):

                result = find_hospitals(location)

            if result.get("success"):

                hospitals = result.get(
                    "hospitals",
                    []
                )

                if hospitals:

                    st.success(
                        f"Found {len(hospitals)} hospital(s)."
                    )

                    for hospital in hospitals:

                        with st.container(border=True):

                            name = hospital.get(
                                "name",
                                "Hospital"
                            )

                            address = hospital.get(
                                "address",
                                "Address unavailable"
                            )

                            latitude = hospital.get(
                                "latitude"
                            )

                            longitude = hospital.get(
                                "longitude"
                            )

                            st.markdown(
                                f"### 🏥 {name}"
                            )

                            st.write(address)

                            if (
                                latitude is not None
                                and longitude is not None
                            ):

                                query = urllib.parse.quote_plus(
                                    f"{latitude},{longitude}"
                                )

                                maps_url = (
                                    "https://www.google.com/maps/"
                                    f"search/?api=1&query={query}"
                                )

                                st.link_button(
                                    "Open directions",
                                    maps_url
                                )

                else:

                    st.info(
                        "No hospitals were found for this location."
                    )

            else:

                st.error(
                    result.get(
                        "error",
