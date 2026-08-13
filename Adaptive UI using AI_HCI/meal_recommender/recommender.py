import pandas as pd
from datetime import datetime, timedelta

from data_manager import (
    get_meal_history,
    get_shopping_history,
    get_recipes
)


# ---------------------------------------------------
# Convert text into ingredient list
# ---------------------------------------------------

def clean_ingredients(text):

    return [
        item.strip().lower()
        for item in text.split(",")
    ]


# ---------------------------------------------------
# Find ingredients currently available
# ---------------------------------------------------

def get_available_ingredients():

    shopping = get_shopping_history()

    if shopping.empty:
        return []


    ingredients = (
        shopping["Item"]
        .str.lower()
        .str.strip()
        .tolist()
    )

    return ingredients



# ---------------------------------------------------
# Find user's favorite foods
# Based on previous meals
# ---------------------------------------------------

def get_user_preferences():

    meals = get_meal_history()

    if meals.empty:
        return []


    dishes = (
        meals["Dish"]
        .str.lower()
        .tolist()
    )


    preferences = []

    for dish in dishes:

        words = dish.split()

        for word in words:

            if word not in preferences:
                preferences.append(word)


    return preferences



# ---------------------------------------------------
# Remove recently eaten meals
# ---------------------------------------------------

def get_recent_meals(days=3):

    meals = get_meal_history()

    if meals.empty:
        return []


    meals["Date"] = pd.to_datetime(
        meals["Date"]
    )


    cutoff = (
        datetime.today()
        -
        timedelta(days=days)
    )


    recent = meals[
        meals["Date"] >= cutoff
    ]


    return (
        recent["Dish"]
        .str.lower()
        .tolist()
    )



# ---------------------------------------------------
# Calculate recipe score
# ---------------------------------------------------

def calculate_score(recipe):

    score = 0

    reasons = []


    available = get_available_ingredients()

    preferences = get_user_preferences()

    recent = get_recent_meals()



    dish = recipe["Dish"]

    ingredients = clean_ingredients(
        recipe["Ingredients"]
    )


    # -----------------------------
    # Ingredient availability
    # -----------------------------

    matching = []

    for item in ingredients:

        if item in available:

            matching.append(item)


    if matching:

        score += len(matching) * 3

        reasons.append(
            "You have these ingredients available: "
            +
            ", ".join(matching)
        )


    # -----------------------------
    # User preference learning
    # -----------------------------

    for pref in preferences:

        if pref in dish.lower():

            score += 2

            reasons.append(
                "This matches your previous eating habits"
            )


    # -----------------------------
    # Avoid repetition
    # -----------------------------

    if dish.lower() in recent:

        score -= 10

        reasons.append(
            "You ate this recently"
        )

    else:

        score += 1

        reasons.append(
            "You have not eaten this recently"
        )


    return score, reasons



# ---------------------------------------------------
# Main Recommendation Function
# ---------------------------------------------------

def recommend_meals(limit=5):


    recipes = get_recipes()


    if recipes.empty:

        return []



    recommendations = []


    for _, recipe in recipes.iterrows():

        score, reasons = calculate_score(
            recipe
        )


        recommendations.append(

            {
                "Dish": recipe["Dish"],

                "Score": score,

                "Reason": reasons
            }

        )



    # Highest score first

    recommendations = sorted(
        recommendations,
        key=lambda x: x["Score"],
        reverse=True
    )


    return recommendations[:limit]