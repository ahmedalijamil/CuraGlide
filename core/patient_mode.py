import streamlit as st
from core.model import analyze_patient
from core.safety import quick_safety_check

def render_patient_mode():
st.title("👤 Patient Mode")
st.caption("Provide only information you are comfortable sharing.")

```
with st.form("patient_form"):
    c1, c2 = st.columns(2)

    age = c1.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=18
    )

    gender = c2.text_input(
        "Sex or gender (optional)"
    )

    weight = c1.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=500.0,
        value=60.0
    )

    height = c2.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=300.0,
        value=170.0
    )

    conditions = st.text_input(
        "Existing medical conditions"
    )

    medications = st.text_input(
        "Current/recent medications"
    )

    allergies = st.text_input(
        "Allergies"
    )

    history = st.text_area(
        "Important medical history"
    )

    symptoms = st.text_area(
        "What symptoms or concerns are you experiencing?"
    )

    duration = st.text_input(
        "How long have you had them?"
    )

    submitted = st.form_submit_button(
        "Analyze",
        type="primary"
    )

if submitted:
    if not symptoms.strip():
        st.warning(
            "Please describe your symptoms or concerns."
        )
        return

    patient_data = {
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "conditions": conditions,
        "medications": medications,
        "allergies": allergies,
        "history": history,
        "symptoms": symptoms,
        "duration": duration
    }

    safety = quick_safety_check(symptoms)

    st.subheader("🚦 Safety guidance")

    if safety.get("level") == "URGENT ATTENTION":
        st.warning(
            safety.get(
                "message",
                "Your symptoms may require urgent medical attention."
            )
        )
    else:
        st.info(
            safety.get(
                "message",
                "Please consult a healthcare professional for medical advice."
            )
        )

    with st.spinner(
        "CuraGlide is reviewing the information..."
    ):
        result = analyze_patient(patient_data)

    if result.get("success"):
        st.subheader("🩺 CuraGlide Health Information")
        st.markdown(result.get("analysis", "No analysis returned."))
    else:
        st.error(
            result.get(
                "error",
                "Unable to analyze the information."
            )
        )

st.divider()

st.caption(
    "⚠️ CuraGlide provides health information only and does not "
    "replace professional medical advice, diagnosis, or emergency care."
)
```
