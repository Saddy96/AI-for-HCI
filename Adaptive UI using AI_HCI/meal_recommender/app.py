import streamlit as st
import pandas as pd

from data_manager import (
    initialize_files,
    add_meal,
    add_shopping_item,
    get_meal_history,
    get_shopping_history
)

from recommender import recommend_meals

# --------------------------
# Initial Setup
# --------------------------

initialize_files()

st.set_page_config(
    page_title="Personalized Meal Recommendation System",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Personalized Meal Recommendation System")
st.markdown(
    """
This application learns your eating habits and grocery purchases to
recommend meals for today.
"""
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Record Meal",
        "Shopping",
        "Meal History",
        "Shopping History"
    ]
)

# ==========================================================
# HOME PAGE
# ==========================================================

if menu == "Home":

    st.header("Today's Meal Recommendation")

    recommendations = recommend_meals()

    if len(recommendations) == 0:

        st.warning("No recommendations available.")

    else:

        for recipe in recommendations:

            with st.container():

                st.subheader(recipe["Dish"])

                st.write("**Reason**")

                for reason in recipe["Reason"]:
                    st.write("✅", reason)

                st.divider()

# ==========================================================
# RECORD MEAL
# ==========================================================

elif menu == "Record Meal":

    st.header("Record Today's Meal")

    date = st.date_input("Date")

    meal_type = st.selectbox(
        "Meal Type",
        [
            "Breakfast",
            "Lunch",
            "Dinner"
        ]
    )

    dish = st.text_input("Dish Name")

    if st.button("Save Meal"):

        if dish.strip() == "":

            st.error("Please enter dish name.")

        else:

            add_meal(
                str(date),
                meal_type,
                dish
            )

            st.success("Meal saved successfully!")

# ==========================================================
# SHOPPING
# ==========================================================

elif menu == "Shopping":

    st.header("Record Grocery Shopping")

    date = st.date_input("Purchase Date")

    item = st.text_input("Item Purchased")

    if st.button("Save Item"):

        if item.strip() == "":

            st.error("Enter item name.")

        else:

            add_shopping_item(
                str(date),
                item
            )

            st.success("Shopping item added.")

# ==========================================================
# MEAL HISTORY
# ==========================================================

elif menu == "Meal History":

    st.header("Meal History")

    meals = get_meal_history()

    if meals.empty:

        st.info("No meal history found.")

    else:

        st.dataframe(
            meals,
            use_container_width=True
        )

# ==========================================================
# SHOPPING HISTORY
# ==========================================================

elif menu == "Shopping History":

    st.header("Shopping History")

    shopping = get_shopping_history()

    if shopping.empty:

        st.info("No shopping history found.")

    else:

        st.dataframe(
            shopping,
            use_container_width=True
        )