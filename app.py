```python
import urllib.parse

import streamlit as st

from core.case_lab import (
    answer_student_question,
    generate_case,
    review_reasoning,
)
from core.hospital_finder import find_hospitals
from core.patient_mode import render_patient_mode


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CuraGlide",
    page_icon="🏥",
    layout="wide",
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "case" not in st.session_state:
    st.session_state.case = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "review" not in st.session_state:
    st.session_state.review = None


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

def nav(page_name):
    st.session_state.page = page_name


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🏥 CuraGlide")
    st.caption(
        "Your well-being in every step — accessed from a single touch."
    )

    pages = [
        ("Home", "🏠"),
        ("Patient Mode", "👤"),
        ("Hospital Finder", "📍"),
        ("Case Lab", "🧪"),
    ]

    for name, icon in pages:
        if st.button(
            f"{icon} {name}",
            use_container_width=True,
        ):
            nav(name)
            st.rerun()

    st.divider()

    st.caption(
        "Health information and education only — "
        "not a replacement for professional medical care."
    )


# --------------------------------------------------
# HOME
# --------------------------------------------------

if st.session_state.page == "Home":

    st.title("🏥 CuraGlide")

    st.subheader(
        "Your well-being in every step — accessed from a single touch."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 👤 Patient Mode")
        st.write(
            "Share symptoms and receive cautious "
            "AI-powered health-information guidance."
        )

        if st.button(
            "Start Patient Mode",
            use_container_width=True,
        ):
            nav("Patient Mode")
            st.rerun()

    with col2:
        st.markdown("### 📍 Hospital Finder")
        st.write(
            "Search for hospitals near a city or area "
            "and open directions."
        )

        if st.button(
            "Find Hospitals",
            use_container_width=True,
        ):
            nav("Hospital Finder")
            st.rerun()

    with col3:
        st.markdown("### 🧪 Case Lab")
        st.write(
            "Practice clinical reasoning using "
            "fictional educational cases."
        )

        if st.button(
            "Open Case Lab",
            use_container_width=True,
        ):
            nav("Case Lab")
            st.rerun()

    st.divider()

    st.info(
        "CuraGlide does not provide confirmed diagnoses "
        "or emergency services."
    )


# --------------------------------------------------
# PATIENT MODE
# --------------------------------------------------

elif st.session_state.page == "Patient Mode":

    render_patient_mode()


# --------------------------------------------------
# HOSPITAL FINDER
# --------------------------------------------------

elif st.session_state.page == "Hospital Finder":

    st.title("📍 Hospital Finder")

    st.caption(
        "Searches public OpenStreetMap/Nominatim data. "
        "Results may be incomplete or unavailable."
    )

    location = st.text_input(
        "Enter a city or area",
        placeholder="Example: Lahore, Pakistan",
    )

    if st.button(
        "Search hospitals",
        type="primary",
    ):

        if not location.strip():
            st.warning("Please enter a city or area.")
        else:

            with st.spinner("Searching..."):
                result = find_hospitals(location)

            if not result.get("success"):

                st.error(
                    result.get(
                        "error",
                        "Unable to search for hospitals.",
                    )
                )

            else:

                origin = result.get("origin", {})

                st.success(
                    "Showing hospitals near "
                    + origin.get("display_name", location)
                )

                hospitals = result.get("hospitals", [])

                if not hospitals:
                    st.info(
                        "No hospitals were found for this location."
                    )

                for hospital in hospitals:

                    st.markdown(
                        f"### 🏥 {hospital.get('name', 'Hospital')}"
                    )

                    st.write(
                        hospital.get(
                            "address",
                            "Address unavailable",
                        )
                    )

                    if hospital.get("distance"):
                        st.caption(hospital["distance"])

                    latitude = hospital.get("latitude")
                    longitude = hospital.get("longitude")

                    if latitude is not None and longitude is not None:

                        query = urllib.parse.quote_plus(
                            f"{latitude},{longitude}"
                        )

                        st.link_button(
                            "Open directions",
                            (
                                "https://www.google.com/maps/"
                                f"search/?api=1&query={query}"
                            ),
                        )

                    st.divider()


# --------------------------------------------------
# CASE LAB
# --------------------------------------------------

elif st.session_state.page == "Case Lab":

    st.title("🧪 Case Lab")

    st.warning(
        "⚠️ Educational use only. "
        "Cases are fictional and not clinical advice."
    )

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

        custom = st.text_area(
            "Optional custom request"
        )

    if st.button(
        "🚀 Generate New Case",
        type="primary",
    ):

        if not topic.strip():

            st.warning("Please enter a topic.")

        else:

            with st.spinner(
                "Generating fictional case..."
            ):

                result = generate_case(
                    topic,
                    difficulty,
                    case_type,
                    custom,
                )

            if "error" in result:

                st.error(result["error"])

            else:

                st.session_state.case = result.get(
                    "case"
                )

                st.session_state.conversation = []

                st.session_state.review = None

                st.rerun()

    # ----------------------------------------------
    # DISPLAY CASE
    # ----------------------------------------------

    case = st.session_state.case

    if case:

        st.divider()

        st.subheader(
            case.get(
                "title",
                "Fictional Case",
            )
        )

        st.info(
            case.get(
                "professor_intro",
                "",
            )
        )

        patient = case.get(
            "patient",
            {},
        )

        st.markdown(
            "**Patient:** "
            + patient.get(
                "description",
                "",
            )
        )

        st.write(
            patient.get(
                "opening_presentation",
                "",
            )
        )

        st.markdown(
            "### Initial information"
        )

        initial_information = case.get(
            "initial_information",
            [],
        )

        for item in initial_information:
            st.write(
                "• " + str(item)
            )

        # ------------------------------------------
        # CONVERSATION
        # ------------------------------------------

        for item in st.session_state.conversation:

            st.markdown(
                f"**You:** {item.get('q', '')}"
            )

            st.write(
                "**Professor:** "
                + item.get("a", "")
            )

        # ------------------------------------------
        # ASK PROFESSOR
        # ------------------------------------------

        question = st.text_input(
            "Ask the professor a question",
            key="case_question",
        )

        if st.button(
            "Ask question"
        ) and question.strip():

            with st.spinner(
                "Professor is responding..."
            ):

                answer = answer_student_question(
                    case,
                    question,
                    st.session_state.conversation,
                )

            if "error" in answer:

                st.error(answer["error"])

            else:

                st.session_state.conversation.append(
                    {
                        "q": question,
                        "a": answer.get(
                            "answer",
                            "",
                        ),
                        "teaching_point": answer.get(
                            "teaching_point",
                            "",
                        ),
                    }
                )

                st.rerun()

        # ------------------------------------------
        # REASONING REVIEW
        # ------------------------------------------

        reasoning = st.text_area(
            "Your clinical reasoning / final thoughts"
        )

        if st.button(
            "🎓 Get Professor Review"
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

                if "error" in review_result:

                    st.error(
                        review_result["error"]
                    )

                else:

                    st.session_state.review = (
                        review_result.get(
                            "review"
                        )
                    )

        # ------------------------------------------
        # DISPLAY REVIEW
        # ------------------------------------------

        if st.session_state.review:

            review = st.session_state.review

            st.subheader(
                "🎓 Professor Review"
            )

            st.write(
                review.get(
                    "overall_feedback",
                    "",
                )
            )

            sections = [
                (
                    "What went well",
                    "what_went_well",
                ),
                (
                    "What was missed",
                    "what_was_missed",
                ),
                (
                    "Important warning signs",
                    "important_warning_signs",
                ),
            ]

            for title, key in sections:

                st.markdown(
                    f"**{title}**"
                )

                items = review.get(
                    key,
                    [],
                )

                for item in items:

                    st.write(
                        "• " + str(item)
                    )

            st.markdown(
                "**Key lesson:** "
                + str(
                    review.get(
                        "key_lesson",
                        "",
                    )
                )
            )
```

### One important thing

This `app.py` **still requires**:

```text
core/patient_mode.py
```

with:

```python
render_patient_mode()
```

So **don't delete `patient_mode.py`**. Your previous crash was because that file was malformed, not because this `app.py` structure was wrong.

Also, I removed the unused imports:

```python
from core.model import analyze_patient
from core.safety import quick_safety_check
```

because `app.py` doesn't directly use them; Patient Mode should handle those internally.

**Next step:** replace your current `app.py` with the version above, commit it, and then we'll fix `patient_mode.py` if Streamlit throws an error.
