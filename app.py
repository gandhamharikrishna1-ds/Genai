
import streamlit as st
from google import genai

st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 CareerPath AI")
st.subheader("Career Guidance for Rural Students")
st.write(
    "Discover career opportunities based on your education, "
    "interests, skills, and goals."
)

with st.sidebar:
    st.header("About CareerPath AI")
    st.write(
        "An AI-powered career guidance platform designed "
        "to help students explore career paths and learning opportunities."
    )
    st.caption("Prototype version 1.0")

st.header("Tell us about yourself")

with st.form("career_form"):
    education = st.selectbox(
        "Your current education",
        [
            "10th standard",
            "12th standard",
            "Diploma",
            "Undergraduate",
            "Postgraduate"
        ]
    )

    stream = st.text_input(
        "Your course or academic stream",
        placeholder="e.g. B.Tech Computer Science"
    )

    interests = st.text_input(
        "Your interests",
        placeholder="e.g. technology, teaching, agriculture"
    )

    skills = st.text_input(
        "Your skills",
        placeholder="e.g. communication, Python, problem-solving"
    )

    budget = st.selectbox(
        "Preferred learning budget",
        [
            "Free resources only",
            "Low-cost resources",
            "Flexible budget"
        ]
    )

    goals = st.text_area(
        "Your career goals",
        placeholder="Describe what you would like to achieve."
    )

    submitted = st.form_submit_button(
        "✨ Discover My Career Paths",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not interests.strip() or not goals.strip():
        st.warning("Please enter your interests and career goals.")
    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            prompt = f"""
You are a careful and supportive career guidance assistant
for students, especially those from rural communities.

Recommend realistic career paths based on this student profile.

Education: {education}
Course or stream: {stream or "Not provided"}
Interests: {interests}
Skills: {skills or "Not provided"}
Learning budget: {budget}
Career goals: {goals}

Provide:
1. Three suitable career paths with reasons.
2. Skills required for each path.
3. A beginner-friendly 30-day learning roadmap.
4. Free or low-cost learning resources.
5. Possible next educational steps and eligibility considerations.

Do not invent scholarships, official eligibility rules, salaries,
or application deadlines. Clearly state when information needs
verification from an official source.

Use clear, encouraging language suitable for a student.
Explain that these are suggestions, not guaranteed career outcomes.
"""

            with st.spinner("AI is exploring suitable career paths..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.success("Your career guidance is ready!")
            st.markdown(response.text or "No response was generated.")

        except Exception as error:
            st.error(
                "We couldn't generate your recommendations. "
                "Check your API key, internet connection, and model access."
            )
            st.caption(f"Technical details: {error}")
