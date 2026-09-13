import streamlit as st

from core.model import analyze_patient


# =================================================
# PATIENT QUESTIONS
# =================================================

PATIENT_QUESTIONS = [
    {
        "key": "age",
        "question": "Hi there! 👋 Let's get you well and fit! 😊 First off, what's your age? 🎂",
        "placeholder": "Enter your age",
        "type": "number",
        "min_value": 1,
        "max_value": 120,
        "step": 1
    },
    {
        "key": "gender",
        "question": "Thanks! 😊 What is your sex or gender?",
        "placeholder": "For example: Male, Female, Another identity, or Prefer not to say",
        "type": "text"
    },
    {
        "key": "weight",
        "question": "Got it! ⚖️ How much do you weigh?",
        "placeholder": "Enter your weight in kg",
        "type": "number",
        "min_value": 1.0,
        "max_value": 500.0,
        "step": 0.1
    },
    {
        "key": "height",
        "question": "And what's your height? 📏",
        "placeholder": "Enter your height in cm",
        "type": "number",
        "min_value": 30.0,
        "max_value": 300.0,
        "step": 0.1
    },
    {
        "key": "conditions",
        "question": "Do you have any existing medical conditions I should know about? 🏥",
        "placeholder": "For example: asthma, diabetes, high blood pressure, or None",
        "type": "text"
    },
    {
        "key": "medications",
        "question": "Are you currently taking, or have you recently taken, any medications? 💊",
        "placeholder": "Include prescription or over-the-counter medicines, or type None",
        "type": "text"
    },
    {
        "key": "allergies",
        "question": "Do you have any allergies I should know about? ⚠️",
        "placeholder": "For example: medicine allergies, food allergies, or None",
        "type": "text"
    },
    {
        "key": "medical_history",
        "question": "Have you had any important illnesses, hospitalizations, or surgeries before? 🏥",
        "placeholder": "Briefly describe them, or type None",
        "type": "text"
    },
    {
        "key": "symptoms",
        "question": "Now tell me how you're feeling today. 💬 What symptoms, pain, or concerns are you experiencing?",
        "placeholder": "Describe everything you think might be important",
        "type": "text"
    },
    {
        "key": "duration",
        "question": "How long have you been experiencing these symptoms? ⏱️",
        "placeholder": "For example: 2 hours, 3 days, or 2 weeks",
        "type": "text"
    }
]


# =================================================
# SESSION STATE
# =================================================

def initialize_patient_session():

    defaults = {
        "patient_step": 0,
        "patient_answers": {},
        "patient_completed": False,
        "patient_analysis": None,
        "patient_analysis_error": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def reset_patient_mode():

    st.session_state.patient_step = 0
    st.session_state.patient_answers = {}
    st.session_state.patient_completed = False
    st.session_state.patient_analysis = None
    st.session_state.patient_analysis_error = None


# =================================================
# VALIDATION
# =================================================

def validate_answer(question, answer):

    if question["type"] == "number":

        if answer is None:
            return False, "Please enter a value."

        if (
            answer < question["min_value"]
            or answer > question["max_value"]
        ):
            return (
                False,
                f"Please enter a value between "
                f"{question['min_value']} and "
                f"{question['max_value']}."
            )

        return True, ""

    if not str(answer).strip():

        return (
            False,
            "Please enter an answer before continuing."
        )

    return True, ""


# =================================================
# PATIENT MODE
# =================================================

def render_patient_mode():

    initialize_patient_session()

    st.title("🏥 CuraGlide")

    st.caption(
        "Your well-being in every step — accessed from a single touch."
    )

    st.divider()

    # =================================================
    # ANALYSIS RESULT
    # =================================================

    if st.session_state.patient_analysis:

        st.success("✅ CuraGlide analysis complete!")

        st.markdown("## 🧠 AI Health Analysis")

        st.markdown(
            st.session_state.patient_analysis
        )

        st.warning(
            "⚠️ CuraGlide provides health information, "
            "not a confirmed medical diagnosis."
        )

        if st.button(
            "🔄 Start New Health Check",
            use_container_width=True
        ):

            reset_patient_mode()
            st.rerun()

        return

    # =================================================
    # ANALYSIS ERROR
    # =================================================

    if st.session_state.patient_analysis_error:

        st.error(
            st.session_state.patient_analysis_error
        )

        if st.button(
            "🔄 Try Analysis Again",
            use_container_width=True
        ):

            st.session_state.patient_analysis_error = None
            st.rerun()

        return

    # =================================================
    # RUN AI ANALYSIS
    # =================================================

    if st.session_state.patient_completed:

        st.success(
            "✅ Thank you! I've collected your information."
        )

        st.markdown("## 🧠 Analyzing your information...")

        with st.spinner("CuraGlide is analyzing..."):

            result = analyze_patient(
                st.session_state.patient_answers
            )

        if result.get("success"):

            st.session_state.patient_analysis = (
                result.get(
                    "analysis",
                    "No analysis returned."
                )
            )

        else:

            st.session_state.patient_analysis_error = (
                result.get(
                    "error",
                    "Unable to analyze your information."
                )
            )

        st.rerun()

        return

    # =================================================
    # CURRENT QUESTION
    # =================================================

    step = st.session_state.patient_step

    total_questions = len(PATIENT_QUESTIONS)

    question_data = PATIENT_QUESTIONS[step]

    progress = (step + 1) / total_questions

    st.progress(progress)

    st.caption(
        f"Question {step + 1} of {total_questions}"
    )

    st.markdown(
        f"## {question_data['question']}"
    )

    # =================================================
    # QUESTION FORM
    # =================================================

    with st.form(
        key=f"patient_form_{step}",
        clear_on_submit=False
    ):

        existing_answer = (
            st.session_state.patient_answers.get(
                question_data["key"]
            )
        )

        if question_data["type"] == "number":

            if existing_answer is None:
                default_value = question_data["min_value"]
            else:
                default_value = existing_answer

            user_answer = st.number_input(
                "Your answer",
                min_value=question_data["min_value"],
                max_value=question_data["max_value"],
                value=default_value,
                step=question_data["step"]
            )

        else:

            user_answer = st.text_area(
                "Your answer",
                value=existing_answer or "",
                placeholder=question_data["placeholder"],
                height=120
            )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            previous_clicked = False

            if step > 0:

                previous_clicked = st.form_submit_button(
                    "← Previous",
                    use_container_width=True
                )

        with col2:

            if step == total_questions - 1:

                next_clicked = st.form_submit_button(
                    "Analyze →",
                    type="primary",
                    use_container_width=True
                )

            else:

                next_clicked = st.form_submit_button(
                    "Continue →",
                    type="primary",
                    use_container_width=True
                )

    # =================================================
    # HANDLE PREVIOUS
    # =================================================

    if previous_clicked:

        st.session_state.patient_step -= 1
        st.rerun()

    # =================================================
    # HANDLE NEXT
    # =================================================

    if next_clicked:

        valid, message = validate_answer(
            question_data,
            user_answer
        )

        if not valid:

            st.warning(message)

        else:

            st.session_state.patient_answers[
                question_data["key"]
            ] = user_answer

            if step == total_questions - 1:

                st.session_state.patient_completed = True

            else:

                st.session_state.patient_step += 1

            st.rerun()

    # =================================================
    # RESTART
    # =================================================

    st.write("")

    if st.button(
        "🔄 Restart health check",
        use_container_width=True
    ):

        reset_patient_mode()
        st.rerun()
