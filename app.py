import os
import streamlit as st
import ollama

from rag import (
    add_pdf_to_database,
    search_documents,
    get_document_count
)

from crop_recommendation import recommend_crops


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KisanAI",
    page_icon="🌾",
    layout="wide"
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "style.css"
    )

    if os.path.exists(css_path):

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ============================================================
# AI MODEL
# ============================================================

TEXT_MODEL = "llama3.2:3b"


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOCUMENT_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "farming_documents"
)

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(question, context=""):

    try:

        system_prompt = """
You are KisanAI, an AI farming assistant.

Your job is to help farmers understand agriculture
in simple and practical language.

Give clear answers about:

- crops
- soil
- irrigation
- fertilizers
- pests
- diseases
- farming practices
- harvesting
- crop management
- weather-related farming risks

Use simple language that farmers can understand.

Do not claim that an AI answer is a confirmed
laboratory diagnosis.

If information is uncertain, clearly say that the farmer
should consult a local agricultural expert or agriculture
officer.

Avoid dangerous or unsupported pesticide dosages.
"""


        if context:

            user_prompt = f"""
Use the following farming document information to answer
the farmer's question.

FARMING DOCUMENT CONTEXT:

{context}

FARMER QUESTION:

{question}

Answer using the document information wherever relevant.

If the document does not contain the answer, say so clearly.
"""

        else:

            user_prompt = question


        response = ollama.chat(

            model=TEXT_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ]

        )


        return response["message"]["content"]


    except Exception as e:

        return f"""
⚠️ AI Error

{str(e)}

Please make sure Ollama is running and
the model {TEXT_MODEL} is available.
"""


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌾 KisanAI")

st.sidebar.write(
    "Smart AI Farming Assistant"
)

st.sidebar.markdown("---")


option = st.sidebar.radio(

    "Choose a feature",

    [
        "🏠 Home",
        "🤖 AI Farming Chat",
        "🌱 Crop Recommendation",
        "🩺 Crop Doctor",
        "📄 Ask Your PDF",
        "🌦️ Weather & Risk",
        "💰 Profit Estimator",
        "🚜 Farm Tracker",
        "📊 Dashboard"
    ]

)


st.sidebar.markdown("---")


st.sidebar.info(
    "KisanAI helps farmers with AI-powered "
    "farming information and decision support."
)


# ============================================================
# HOME
# ============================================================

if option == "🏠 Home":

    st.title("🌾 Welcome to KisanAI")

    st.subheader(
        "Your AI-powered smart farming assistant"
    )

    st.write(
        """
        KisanAI is designed to help farmers get
        useful agricultural information in one place.
        """
    )

    st.markdown("---")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            ### 🤖 AI Farming Chat

            Ask agriculture-related questions
            and get AI-powered answers.
            """
        )


    with col2:

        st.markdown(
            """
            ### 🌱 Crop Recommendation

            Get crop suggestions based on
            soil and climate conditions.
            """
        )


    with col3:

        st.markdown(
            """
            ### 🩺 Crop Doctor

            Ask questions about crop diseases,
            pests and plant problems.
            """
        )


    st.markdown("---")


    col4, col5, col6 = st.columns(3)


    with col4:

        st.markdown(
            """
            ### 📄 Ask Your PDF

            Upload farming documents and
            ask questions from them.
            """
        )


    with col5:

        st.markdown(
            """
            ### 🌦️ Weather & Risk

            Understand weather conditions
            and farming risks.
            """
        )


    with col6:

        st.markdown(
            """
            ### 💰 Profit Estimator

            Estimate farming expenses,
            revenue and profit.
            """
        )


# ============================================================
# AI FARMING CHAT
# ============================================================

elif option == "🤖 AI Farming Chat":

    st.title("🤖 AI Farming Chat")

    st.write(
        "Ask KisanAI any agriculture-related question."
    )


    if "chat_messages" not in st.session_state:

        st.session_state.chat_messages = []


    # Display previous messages

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # User question

    question = st.chat_input(
        "Ask your farming question..."
    )


    if question:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):

            st.markdown(question)


        with st.chat_message("assistant"):

            with st.spinner(
                "🌾 KisanAI is thinking..."
            ):

                answer = ask_ai(question)


            st.markdown(answer)


        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    if st.button(
        "🗑️ Clear Chat"
    ):

        st.session_state.chat_messages = []

        st.rerun()


# ============================================================
# CROP RECOMMENDATION
# ============================================================

elif option == "🌱 Crop Recommendation":

    st.title("🌱 Crop Recommendation")

    st.write(
        "Enter your soil and climate information "
        "to get suitable crop suggestions."
    )


    col1, col2 = st.columns(2)


    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=200.0,
            value=50.0
        )


        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=200.0,
            value=50.0
        )


        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=200.0,
            value=50.0
        )


        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10.0,
            max_value=60.0,
            value=25.0
        )


    with col2:

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0
        )


        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=5000.0,
            value=100.0
        )


        soil_type = st.selectbox(
            "Soil Type",
            [
                "Black Soil",
                "Alluvial Soil",
                "Red Soil",
                "Sandy Soil",
                "Clay Soil",
                "Loamy Soil"
            ]
        )


    st.markdown("---")


    if st.button(
        "🌱 Recommend Crops",
        use_container_width=True
    ):

        recommendations = recommend_crops(

            nitrogen,

            phosphorus,

            potassium,

            temperature,

            humidity,

            rainfall,

            soil_type

        )


        if recommendations:

            st.success(
                "Recommended crops based on your inputs:"
            )


            for crop, reason in recommendations:

                st.subheader(
                    f"🌾 {crop}"
                )

                st.write(reason)


        else:

            st.warning(
                "No strong recommendation found "
                "for the given conditions."
            )


# ============================================================
# CROP DOCTOR
# ============================================================

elif option == "🩺 Crop Doctor":

    st.title("🩺 Crop Doctor")

    st.write(
        "Ask KisanAI about crop diseases, pests, "
        "plant problems and farming solutions."
    )


    st.markdown("---")


    crop_question = st.text_area(

        "🌱 Ask your crop-related question",

        placeholder=(
            "Example: My rice leaves are turning "
            "yellow. What could be the reason?"
        ),

        height=120

    )


    if st.button(
        "🔍 Get Crop Advice",
        use_container_width=True
    ):


        if crop_question.strip():


            crop_prompt = f"""
You are KisanAI Crop Doctor.

Answer the farmer's question in simple language.

IMPORTANT:
Give the answer in MAXIMUM 4 short lines.

Include:
1. Possible reason
2. What the farmer can do
3. One prevention tip if useful

Do not give dangerous pesticide dosages.
Do not claim a confirmed diagnosis.

Farmer's question:

{crop_question}
"""


            with st.spinner(
                "🩺 KisanAI is checking..."
            ):

                answer = ask_ai(
                    crop_prompt
                )


            # Keep only 4 lines

            lines = [

                line.strip()

                for line in answer.splitlines()

                if line.strip()

            ]


            short_answer = "\n".join(
                lines[:4]
            )


            st.success(
                "🌱 Crop Advice"
            )


            st.write(
                short_answer
            )


        else:

            st.warning(
                "Please enter your crop-related question."
            )


# ============================================================
# ASK YOUR PDF
# ============================================================

elif option == "📄 Ask Your PDF":

    st.title("📄 Ask Your Farming PDF")

    st.write(
        "Upload a farming PDF and ask questions "
        "from its content."
    )


    uploaded_pdf = st.file_uploader(
        "Upload farming PDF",
        type=["pdf"]
    )


    if uploaded_pdf:

        st.success(
            f"PDF selected: {uploaded_pdf.name}"
        )


        if st.button(
            "📚 Add PDF to KisanAI",
            use_container_width=True
        ):

            try:

                safe_name = os.path.basename(
                    uploaded_pdf.name
                )


                save_path = os.path.join(
                    DOCUMENT_FOLDER,
                    safe_name
                )


                with open(
                    save_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_pdf.getbuffer()
                    )


                chunks = add_pdf_to_database(
                    save_path
                )


                if chunks > 0:

                    st.success(
                        f"PDF added successfully! "
                        f"{chunks} text chunks stored."
                    )

                else:

                    st.warning(
                        "Could not extract useful text "
                        "from this PDF."
                    )


            except Exception as e:

                st.error(
                    f"PDF processing error: {str(e)}"
                )


    st.markdown("---")


    st.subheader(
        "📚 Ask a Question"
    )


    pdf_question = st.text_input(
        "Enter your question about the farming documents"
    )


    if st.button(
        "🔎 Search PDF",
        use_container_width=True
    ):


        if pdf_question.strip():

            with st.spinner(
                "Searching farming documents..."
            ):

                documents = search_documents(
                    pdf_question,
                    n_results=4
                )


            if documents:

                context = "\n\n".join(
                    documents
                )


                with st.spinner(
                    "🤖 Generating answer..."
                ):

                    answer = ask_ai(
                        pdf_question,
                        context
                    )


                st.subheader(
                    "🤖 KisanAI Answer"
                )

                st.write(answer)


                with st.expander(
                    "📖 View Retrieved Information"
                ):


                    for i, document in enumerate(
                        documents,
                        start=1
                    ):

                        st.markdown(
                            f"### Source {i}"
                        )

                        st.write(
                            document
                        )


            else:

                st.warning(
                    "No relevant information was found "
                    "in the farming documents."
                )


        else:

            st.warning(
                "Please enter a question."
            )


# ============================================================
# WEATHER & RISK
# ============================================================

elif option == "🌦️ Weather & Risk":

    st.title("🌦️ Weather & Farming Risk")

    st.write(
        "Enter weather conditions to understand "
        "basic farming risks."
    )


    col1, col2 = st.columns(2)


    with col1:

        weather_temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10.0,
            max_value=60.0,
            value=28.0,
            key="weather_temperature"
        )


        weather_humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=65.0,
            key="weather_humidity"
        )


    with col2:

        weather_rainfall = st.number_input(
            "Expected Rainfall (mm)",
            min_value=0.0,
            max_value=1000.0,
            value=50.0,
            key="weather_rainfall"
        )


        wind_speed = st.number_input(
            "Wind Speed (km/h)",
            min_value=0.0,
            max_value=200.0,
            value=10.0
        )


    if st.button(
        "🌦️ Check Risk",
        use_container_width=True
    ):


        risks = []


        if weather_temperature > 40:

            risks.append(
                "🔥 High temperature risk"
            )


        if weather_humidity > 85:

            risks.append(
                "💧 High humidity may increase "
                "fungal disease risk"
            )


        if weather_rainfall > 150:

            risks.append(
                "🌧️ Heavy rainfall risk"
            )


        if wind_speed > 40:

            risks.append(
                "💨 Strong wind risk"
            )


        if risks:

            st.warning(
                "Potential farming risks:"
            )


            for risk in risks:

                st.write(
                    f"- {risk}"
                )


        else:

            st.success(
                "✅ No major risk detected from "
                "these basic conditions."
            )


# ============================================================
# PROFIT ESTIMATOR
# ============================================================

elif option == "💰 Profit Estimator":

    st.title("💰 Farm Profit Estimator")

    st.write(
        "Estimate your farming cost, revenue and profit."
    )


    col1, col2 = st.columns(2)


    with col1:

        land_area = st.number_input(
            "Land Area (acres)",
            min_value=0.1,
            value=1.0
        )


        yield_per_acre = st.number_input(
            "Expected Yield per Acre (kg)",
            min_value=0.0,
            value=2500.0
        )


        selling_price = st.number_input(
            "Selling Price per kg (₹)",
            min_value=0.0,
            value=25.0
        )


    with col2:

        seed_cost = st.number_input(
            "Seed Cost (₹)",
            min_value=0.0,
            value=5000.0
        )


        fertilizer_cost = st.number_input(
            "Fertilizer Cost (₹)",
            min_value=0.0,
            value=8000.0
        )


        labor_cost = st.number_input(
            "Labor Cost (₹)",
            min_value=0.0,
            value=10000.0
        )


        other_cost = st.number_input(
            "Other Costs (₹)",
            min_value=0.0,
            value=5000.0
        )


    if st.button(
        "💰 Calculate Profit",
        use_container_width=True
    ):


        total_yield = (
            land_area *
            yield_per_acre
        )


        revenue = (
            total_yield *
            selling_price
        )


        total_cost = (
            seed_cost +
            fertilizer_cost +
            labor_cost +
            other_cost
        )


        profit = (
            revenue -
            total_cost
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Expected Revenue",
                f"₹{revenue:,.2f}"
            )


        with col2:

            st.metric(
                "Total Cost",
                f"₹{total_cost:,.2f}"
            )


        with col3:

            st.metric(
                "Estimated Profit",
                f"₹{profit:,.2f}"
            )


        if profit > 0:

            st.success(
                "🎉 Estimated farming operation "
                "is profitable."
            )


        elif profit == 0:

            st.info(
                "The estimated revenue and cost "
                "are approximately equal."
            )


        else:

            st.error(
                "⚠️ Estimated operation may result "
                "in a loss."
            )


# ============================================================
# FARM TRACKER
# ============================================================

elif option == "🚜 Farm Tracker":

    st.title("🚜 Farm Tracker")

    st.write(
        "Keep basic information about your farm."
    )


    farm_name = st.text_input(
        "Farm Name"
    )


    crop_name = st.text_input(
        "Crop Name"
    )


    sowing_date = st.date_input(
        "Sowing Date"
    )


    area = st.number_input(
        "Farm Area (acres)",
        min_value=0.1,
        value=1.0
    )


    if st.button(
        "💾 Save Farm Information",
        use_container_width=True
    ):


        st.session_state["farm_name"] = (
            farm_name
        )


        st.session_state["crop_name"] = (
            crop_name
        )


        st.session_state["sowing_date"] = (
            str(sowing_date)
        )


        st.session_state["farm_area"] = (
            area
        )


        st.success(
            "✅ Farm information saved!"
        )


    if "farm_name" in st.session_state:

        st.markdown("---")

        st.subheader(
            "🌾 Current Farm"
        )


        st.write(
            f"**Farm:** "
            f"{st.session_state['farm_name']}"
        )


        st.write(
            f"**Crop:** "
            f"{st.session_state['crop_name']}"
        )


        st.write(
            f"**Sowing Date:** "
            f"{st.session_state['sowing_date']}"
        )


        st.write(
            f"**Area:** "
            f"{st.session_state['farm_area']} acres"
        )


# ============================================================
# DASHBOARD
# ============================================================

elif option == "📊 Dashboard":

    st.title("📊 KisanAI Dashboard")


    document_count = get_document_count()


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📄 Document Chunks",
            document_count
        )


    with col2:

        st.metric(
            "🌱 Crop Tools",
            "1"
        )


    with col3:

        st.metric(
            "🤖 AI Assistant",
            "Active"
        )


    with col4:

        st.metric(
            "🌾 Platform",
            "KisanAI"
        )


    st.markdown("---")


    st.subheader(
        "🚜 KisanAI Features"
    )


    features = [

        "🤖 AI Farming Chat",

        "🌱 Crop Recommendation",

        "🩺 Crop Doctor",

        "📄 Ask Your PDF",

        "🌦️ Weather & Risk",

        "💰 Profit Estimator",

        "🚜 Farm Tracker"

    ]


    for feature in features:

        st.write(
            f"✅ {feature}"
        )


    st.markdown("---")


    st.info(
        """
        🌾 KisanAI is designed as a digital farming
        assistant that brings multiple agricultural
        support features into one platform.
        """
    )