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

    /* Main content */
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
        background: linear-gradient(
            135deg,
            #D62828,
            #B91C1C
        );

        color: white !important;

        border: 2px solid #FF6B6B;

        border-radius: 12px;

        font-weight: 700;

        padding: 0.65rem 1rem;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #EF4444,
            #C81E1E
        );

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
        background-color: rgba(255, 255, 255, 0.10) !important;

        color: white !important;

        border: 1px solid rgba(150, 255, 245, 0.35) !important;

        border-radius: 10px;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
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
        background-color: rgba(255, 255, 255, 0.10);

        border-color: rgba(150, 255, 245, 0.35);

        color: white;
    }

    /* =========================
       CARDS / CONTAINERS
       ========================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(4, 31, 43, 0.55);

        border: 1px solid rgba(94, 234, 212, 0.20);

        border-radius: 16px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.20);
    }

    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color: rgba(94, 234, 212, 0.25);
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
       SUCCESS
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
