import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size:40px;
        font-weight:bold;
        color:#1f77b4;
        text-align:center;
    }
    .career-card {
        background-color:#f8f9fa;
        padding:20px;
        border-radius:15px;
        margin-bottom:20px;
        border-left:6px solid #1f77b4;
    }
    .match {
        font-size:25px;
        font-weight:bold;
        color:#28a745;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("careers.csv")
    required_columns = [
        "Career",
        "Skills",
        "Description",
        "Salary",
        "WorkStyle",
        "Experience",
        "Learning"
    ]

    missing = set(required_columns) - set(df.columns)
    if missing:
        st.error(
            f"Missing columns in careers.csv: {missing}"
        )
        st.stop()

    df["Salary"] = pd.to_numeric(
        df["Salary"],
        errors="coerce"
    )
    return df

careers = load_data()

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="main-title">
    🎓 AI Career Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    This intelligent recommendation system uses 
    Natural Language Processing (NLP), TF-IDF,
    and cosine similarity to recommend careers
    based on user skills and preferences.
    """
)


# -----------------------------
# Dashboard Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Available Careers",
        len(careers)
    )
with col2:
    total_skills = len(
        set(
            skill.strip()
            for skills in careers["Skills"]
            for skill in skills.split()
        )
    )
    st.metric(
        "Available Skills",
        total_skills
    )

with col3:
    st.metric(
        "Average Salary",
        f"${int(careers['Salary'].mean()):,}"
    )

with col4:
    st.metric(
        "Work Options",
        careers["WorkStyle"].nunique()
    )

st.divider()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header(
    "⚙ Career Preferences"
)

salary_filter = st.sidebar.slider(
    "Minimum Salary",
    50000,
    150000,
    80000,
    step=5000
)

work_filter = st.sidebar.selectbox(
    "Preferred Work Style",
    [
        "Any",
        "Remote",
        "Hybrid",
        "On-site"
    ]
)

experience_filter = st.sidebar.selectbox(
    "Experience Level",
    [
        "Any",
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

number_results = st.sidebar.slider(
    "Number of Recommendations",
    3,
    10,
    5
)

# -----------------------------
# Skill Categories
# -----------------------------
st.subheader(
    "🧠 Select Your Skills"
)

skill_categories = {
    "Programming": [
        "python",
        "java",
        "javascript",
        "c++",
        "sql"
    ],
    "Artificial Intelligence": [
        "ai",
        "machine",
        "learning",
        "deep",
        "nlp",
        "tensorflow"
    ],
    "Data": [
        "statistics",
        "analysis",
        "excel",
        "tableau",
        "powerbi"
    ],
    "Cloud & IT": [
        "aws",
        "azure",
        "docker",
        "linux",
        "networking"
    ],
    "Design": [
        "figma",
        "ux",
        "ui",
        "photoshop",
        "creativity"
    ],
    "Business": [
        "leadership",
        "communication",
        "marketing",
        "strategy"
    ]
}

selected_skills = []

for category, skills in skill_categories.items():
    with st.expander(category):
        selected = st.multiselect(
            f"Choose {category} skills",
            skills
        )
        selected_skills.extend(selected)

# -----------------------------
# Custom Skill Input
# -----------------------------
custom_skills = st.text_input(
    "✍ Additional skills (comma separated)"
)

if custom_skills:
    selected_skills.extend(
        custom_skills.lower().split(",")
    )

# -----------------------------
# Recommendation Button
# -----------------------------
recommend_button = st.button(
    "🚀 Recommend Careers",
    use_container_width=True
)

# -----------------------------
# Filtering Dataset
# -----------------------------
filtered = careers.copy()

filtered = filtered[
    filtered["Salary"] >= salary_filter
]

if work_filter != "Any":

    filtered = filtered[
        filtered["WorkStyle"]
        ==
        work_filter
    ]

if experience_filter != "Any":

    filtered = filtered[
        filtered["Experience"]
        ==
        experience_filter
    ]

# -----------------------------
# AI Recommendation Engine
# -----------------------------
if recommend_button:
    if len(selected_skills) == 0:
        st.warning(
            "Please select or enter at least one skill."
        )

    elif filtered.empty:
        st.error(
            "No careers match your selected preferences. Try changing filters."
        )

    else:
        # Combine skills
        user_profile = " ".join(
            [
                skill.strip().lower()
                for skill in selected_skills
            ]
        )

        # -----------------------------
        # TF-IDF Vectorization
        # -----------------------------
        vectorizer = TfidfVectorizer()

        career_vectors = vectorizer.fit_transform(
            filtered["Skills"]
        )

        user_vector = vectorizer.transform(
            [user_profile]
        )

        # -----------------------------
        # Cosine Similarity
        # -----------------------------
        similarity_scores = cosine_similarity(
            user_vector,
            career_vectors
        )[0]

        results = filtered.copy()
        results["Match Score"] = (
            similarity_scores * 100
        )
        recommendations = (
            results
            .sort_values(
                by="Match Score",
                ascending=False
            )
            .head(number_results)
        )

        st.divider()

        st.subheader(
            "🏆 Recommended Careers"
        )

        # -----------------------------
        # Display Career Cards
        # -----------------------------
        for _, career in recommendations.iterrows():
            career_skills = set(
                career["Skills"]
                .lower()
                .split()
            )

            user_skills = set(
                user_profile
                .lower()
                .split()
            )

            matched_skills = (
                career_skills
                &
                user_skills
            )

            missing_skills = (
                career_skills
                -
                user_skills
            )

            match_percentage = (
                career["Match Score"]
                /
                100
            )

            st.markdown(
                f"""
                <div class="career-card">

                <h2>💼 {career['Career']}</h2>

                <div class="match">
                {career['Match Score']:.1f}% Match
                </div>

                <br>

                <b>📝 Description:</b>
                <p>
                {career['Description']}
                </p>


                <b>💰 Average Salary:</b>
                ${career['Salary']:,}

                <br><br>

                <b>🏢 Work Style:</b>
                {career['WorkStyle']}

                <br><br>

                <b>📈 Experience Level:</b>
                {career['Experience']}

                <br><br>

                <b>📚 Learning Resource:</b>
                <br>
                {career['Learning']}

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                float(match_percentage)
            )

            # -----------------------------
            # Explanation Section
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.success(
                    "✅ Matched Skills"
                )
                if matched_skills:
                    for skill in matched_skills:
                        st.write(
                            f"✔ {skill}"
                        )
                else:
                    st.write(
                        "No direct skill match found."
                    )

            with col2:
                st.info(
                    "📌 Skills To Improve"
                )
                if missing_skills:

                    for skill in list(missing_skills)[:5]:

                        st.write(
                            f"• {skill}"
                        )
                else:

                    st.write(
                        "You already match most required skills."
                    )

            st.divider()

        # -----------------------------
        # Recommendation Chart
        # -----------------------------
        st.subheader(
            "📊 Recommendation Score Comparison"
        )

        chart = px.bar(
            recommendations,
            x="Career",
            y="Match Score",
            color="Match Score",
            text="Match Score",
            color_continuous_scale="Blues",
            title="Career Similarity Scores"
        )

        chart.update_layout(
            yaxis_title="Match Percentage",
            xaxis_title="Career",
            yaxis_range=[
                0,
                100
            ]
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

        # -----------------------------
        # Salary Comparison Chart
        # -----------------------------
        st.subheader(
            "💰 Salary Comparison"
        )

        salary_chart = px.bar(
            recommendations,
            x="Career",
            y="Salary",
            color="Salary",
            title="Average Career Salary",
            color_continuous_scale="Greens"
        )

        st.plotly_chart(
            salary_chart,
            use_container_width=True
        )

        # -----------------------------
        # Download Results
        # -----------------------------
        st.subheader(
            "⬇ Download Recommendations"
        )

        download_data = recommendations[
            [
                "Career",
                "Match Score",
                "Salary",
                "WorkStyle",
                "Experience",
                "Learning"
            ]
        ]

        csv = download_data.to_csv(
            index=False
        )

        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name=
            "career_recommendations.csv",
            mime=
            "text/csv"
        )

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    """
    AI Career Recommendation System
    | Built using Python, Streamlit,
    TF-IDF, and Cosine Similarity
    """
)
