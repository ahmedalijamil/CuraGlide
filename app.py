import urllib.parse
import streamlit as st

from core.case_lab import (
    answer_student_question,
    generate_case,
    review_reasoning,
)
from core.hospital_finder import find_hospitals
from core.patient_mode import render_patient_mode


# =================================================
# PAGE CONFIG
# =================================================

st.set_page_config(
    page_title="CuraGlide",
    page_icon="🏥",
    layout="wide",
)


# =================================================
# CURAGLIDE GLOBAL THEME
# =================================================

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

    color: #FFFFFF !important;

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

    color: #FFFFFF !important;

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(255, 80, 80, 0.35);
}

.stButton > button:active {
    transform: translateY(0);
}


/* =========================
   HOSPITAL DIRECTIONS BUTTON
   ========================= */

.stLinkButton > a {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 2px solid #5EEAD4 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

.stLinkButton > a:hover {
    background-color: #111111 !important;
    color: #FFFFFF !important;
}


/* =========================
   INPUT BOXES
   ========================= */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #000000 !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    border:
        1px solid rgba(150, 255, 245, 0.35) !important;

    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    background-color: #000000 !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    border: 2px solid #5EEAD4 !important;

    box-shadow:
        0 0 12px rgba(94, 234, 212, 0.25);
}


/* Placeholder */

::placeholder {
    color: #B7D8D8 !important;
    opacity: 0.8 !important;
}


/* =========================
   SELECT BOXES
   ========================= */

div[data-baseweb="select"] > div {
    background-color:
        rgba(255, 255, 255, 0.10) !important;

    border-color:
        rgba(150, 255, 245, 0.35) !important;

    color: #FFFFFF !important;
}


/* =========================
   CARDS / CONTAINERS
   ========================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        rgba(4, 31, 43, 0.55);

    border:
        1px solid rgba(94, 234, 212, 0.20);

    border-radius: 16px;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.20);
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
   ALERTS
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


# =================================================
# SESSION STATE
# =================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "case" not in st.session_state:
    st.session_state.case = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "review" not in st.session_state:
    st.session_state.review = None


# =================================================
# NAVIGATION
# =================================================

def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()


# =================================================
# SIDEBAR
# =================================================

with st.sidebar:

    st.markdown("# 🏥 CuraGlide")

    st.caption(
        "Your well-being in every step."
    )

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True,
    ):
        navigate("Home")

    if st.button(
        "👤 Patient Mode",
        use_container_width=True,
    ):
        navigate("Patient Mode")

    if st.button(
        "🏥 Hospital Finder",
        use_container_width=True,
    ):
        navigate("Hospital Finder")

    if st.button(
        "🧪 Case Lab",
        use_container_width=True,
    ):
        navigate("Case Lab")

    st.divider()

    st.caption(
        "Health information and education only — "
        "not a replacement for professional medical care."
    )


# =================================================
# HOME
# =================================================

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
            "AI-generated health-information guidance."
        )

        if st.button(
            "Open Patient Mode →",
            use_container_width=True,
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
            use_container_width=True,
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
            use_container_width=True,
        ):
            navigate("Case Lab")

    with col4:

        st.markdown("### 💙 About CuraGlide")

        st.write(
            "CuraGlide provides educational health information and "
            "does not replace a qualified healthcare professional."
        )


# =================================================
# PATIENT MODE
# =================================================

elif st.session_state.page == "Patient Mode":

    render_patient_mode()


# =================================================
# HOSPITAL FINDER
# =================================================

elif st.session_state.page == "Hospital Finder":

    st.title("🏥 Hospital Finder")

    st.write(
        "Enter a location to search for nearby hospitals."
    )

    location = st.text_input(
        "Location",
        placeholder="Enter city, area, or location",
    )

    if st.button(
        "🔎 Find Hospitals",
        use_container_width=True,
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
                    [],
                )

                if hospitals:

                    st.success(
                        f"Found {len(hospitals)} hospital(s)."
                    )

                    for hospital in hospitals:

                        with st.container(border=True):

                            name = hospital.get(
                                "name",
                                "Hospital",
                            )

                            address = hospital.get(
                                "address",
                                "Address unavailable",
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
                                    "🧭 Open directions",
                                    maps_url,
                                    use_container_width=True,
                                )

                else:

                    st.info(
                        "No hospitals were found for this location."
                    )

            else:

                st.error(
                    result.get(
                        "error",
                        "Unable to find hospitals.",
                    )
                )


# =================================================
# CASE LAB
# =================================================

elif st.session_state.page == "Case Lab":

    st.title("🧪 Case Lab")

    st.warning(
        "⚠️ Educational use only. "
        "Cases are fictional and not clinical advice."
    )

    # =============================================
    # CREATE CASE
    # =============================================

    if st.session_state.case is None:

        st.subheader("Create a Case")

        col1, col2 = st.columns(2)

        with col1:

            topic = st.text_input(
                "Topic",
                placeholder=(
                    "Neurology, cardiology, respiratory..."
                ),
            )

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                ],
            )

        with col2:

            case_type = st.selectbox(
                "Case type",
                [
                    "Diagnostic mystery",
                    "Emergency presentation",
                    "Patient interview",
                    "Clinical reasoning challenge",
                    "Differential diagnosis",
                ],
            )

            custom_request = st.text_area(
                "Optional custom request",
                placeholder=(
                    "Add any specific scenario or learning goal..."
                ),
            )

        if st.button(
            "🚀 Generate New Case",
            type="primary",
            use_container_width=True,
        ):

            if not topic.strip():

                st.warning(
                    "Please enter a topic."
                )

            else:

                with st.spinner(
                    "Generating fictional case..."
                ):

                    result = generate_case(
                        topic,
                        difficulty,
                        case_type,
                        custom_request,
                    )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.session_state.case = result.get(
                        "case"
                    )

                    st.session_state.conversation = []

                    st.session_state.review = None

                    st.rerun()


    # =============================================
    # DISPLAY CASE — CLEAN VERSION
    # =============================================

    else:

        case = st.session_state.case

        st.divider()

        st.subheader(
            case.get(
                "title",
                "Fictional Case",
            )
        )


        # Professor introduction

        professor_intro = case.get(
            "professor_intro",
            "",
        )

        if professor_intro:

            st.info(
                professor_intro
            )


        # Patient

        patient = case.get(
            "patient",
            {},
        )

        if patient:

            st.markdown(
                "### 👤 Patient"
            )

            description = patient.get(
                "description",
                "",
            )

            if description:

                st.markdown(
                    f"**Patient:** {description}"
                )

            opening_presentation = patient.get(
                "opening_presentation",
                "",
            )

            if opening_presentation:

                st.write(
                    opening_presentation
                )


        # Initial information

        initial_information = case.get(
            "initial_information",
            [],
        )

        if initial_information:

            st.markdown(
                "### 📋 Initial Information"
            )

            for item in initial_information:

                st.write(
                    f"• {item}"
                )


        # Possible explanations

        possible_explanations = case.get(
            "possible_explanations",
            [],
        )

        if possible_explanations:

            st.markdown(
                "### 🔍 Possible Explanations"
            )

            for item in possible_explanations:

                st.write(
                    f"• {item}"
                )


        # Warning signs

        warning_signs = case.get(
            "warning_signs",
            [],
        )

        if warning_signs:

            st.markdown(
                "### ⚠️ Important Warning Signs"
            )

            for item in warning_signs:

                st.write(
                    f"• {item}"
                )


        # Professor hints

        professor_hints = case.get(
            "professor_hints",
            [],
        )

        if professor_hints:

            with st.expander(
                "💡 Professor Hints"
            ):

                for item in professor_hints:

                    st.write(
                        f"• {item}"
                    )


        # =========================================
        # CONVERSATION HISTORY
        # =========================================

        if st.session_state.conversation:

            st.divider()

            st.subheader(
                "💬 Conversation"
            )

            for item in st.session_state.conversation:

                st.markdown(
                    f"**You:** {item.get('q', '')}"
                )

                st.write(
                    "**Professor:** "
                    + item.get(
                        "a",
                        "",
                    )
                )

                teaching_point = item.get(
                    "teaching_point",
                    "",
                )

                if teaching_point:

                    st.info(
                        f"💡 Teaching point: "
                        f"{teaching_point}"
                    )

                st.divider()


        # =========================================
        # ASK PROFESSOR
        # =========================================

        st.subheader(
            "💬 Ask the Professor"
        )

        question = st.text_input(
            "Ask the professor a question",
            key="case_question",
        )

        if (
            st.button(
                "Ask Question",
                use_container_width=True,
            )
            and question.strip()
        ):

            with st.spinner(
                "Professor is responding..."
            ):

                answer = answer_student_question(
                    case,
                    question,
                    st.session_state.conversation,
                )

            if isinstance(answer, dict) and "error" in answer:

                st.error(
                    answer["error"]
                )

            else:

                if isinstance(answer, dict):

                    answer_text = answer.get(
                        "answer",
                        "",
                    )

                    teaching_point = answer.get(
                        "teaching_point",
                        "",
                    )

                else:

                    answer_text = str(answer)

                    teaching_point = ""

                st.session_state.conversation.append(
                    {
                        "q": question,
                        "a": answer_text,
                        "teaching_point": teaching_point,
                    }
                )

                st.rerun()


        # =========================================
        # REASONING REVIEW
        # =========================================

        st.divider()

        st.subheader(
            "🧠 Review Your Reasoning"
        )

        reasoning = st.text_area(
            "Your clinical reasoning / final thoughts",
            placeholder=(
                "Explain what you think is happening "
                "and why..."
            ),
            key="reasoning_input",
        )

        if st.button(
            "🎓 Get Professor Review",
            use_container_width=True,
        ):

            if not reasoning.strip():

                st.warning(
                    "Please enter your reasoning first."
                )

            else:

                with st.spinner(
                    "Reviewing reasoning..."
                ):

                    review_result = review_reasoning(
                        case,
                        reasoning,
                        st.session_state.conversation,
                    )

                if (
                    isinstance(review_result, dict)
                    and "error" in review_result
                ):

                    st.error(
                        review_result["error"]
                    )

                else:

                    if isinstance(review_result, dict):

                        st.session_state.review = (
                            review_result.get(
                                "review",
                                review_result,
                            )
                        )

                    else:

                        st.session_state.review = (
                            review_result
                        )

                    st.rerun()


        # =========================================
        # DISPLAY REVIEW — CLEAN VERSION
        # =========================================

        if st.session_state.review:

            st.divider()

            st.subheader(
                "🎓 Professor Review"
            )

            review = st.session_state.review

            if isinstance(review, dict):

                overall_feedback = review.get(
                    "overall_feedback",
                    "",
                )

                if overall_feedback:

                    st.write(
                        overall_feedback
                    )


                sections = [
                    (
                        "✅ What Went Well",
                        "what_went_well",
                    ),
                    (
                        "📝 What Was Missed",
                        "what_was_missed",
                    ),
                    (
                        "⚠️ Important Warning Signs",
                        "important_warning_signs",
                    ),
                ]

                for title, key in sections:

                    items = review.get(
                        key,
                        [],
                    )

                    if items:

                        st.markdown(
                            f"### {title}"
                        )

                        for item in items:

                            st.write(
                                f"• {item}"
                            )


                key_lesson = review.get(
                    "key_lesson",
                    "",
                )

                if key_lesson:

                    st.info(
                        f"💡 Key lesson: "
                        f"{key_lesson}"
                    )

            else:

                st.write(
                    str(review)
                )


        # =========================================
        # START NEW CASE
        # =========================================

        st.divider()

        if st.button(
            "🔄 Start New Case",
            use_container_width=True,
        ):

            st.session_state.case = None

            st.session_state.conversation = []

            st.session_state.review = None

            st.rerun()
