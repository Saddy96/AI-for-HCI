import pandas as pd
import os

# -----------------------------
# File Paths
# -----------------------------

DATA_FOLDER = "data"

MEAL_FILE = os.path.join(DATA_FOLDER, "meal_history.csv")
SHOPPING_FILE = os.path.join(DATA_FOLDER, "shopping_history.csv")
RECIPE_FILE = os.path.join(DATA_FOLDER, "recipes.csv")


# -----------------------------
# Create CSV Files If Missing
# -----------------------------

def initialize_files():

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Meal History
    if not os.path.exists(MEAL_FILE):

        meals = pd.DataFrame(
            columns=[
                "Date",
                "Meal Type",
                "Dish"
            ]
        )

        meals.to_csv(MEAL_FILE, index=False)

    # Shopping History
    if not os.path.exists(SHOPPING_FILE):

        shopping = pd.DataFrame(
            columns=[
                "Date",
                "Item"
            ]
        )

        shopping.to_csv(SHOPPING_FILE, index=False)

    # Recipes
    if not os.path.exists(RECIPE_FILE):

        recipes = pd.DataFrame(
            columns=[
                "Dish",
                "Ingredients"
            ]
        )

        recipes.to_csv(RECIPE_FILE, index=False)


# -----------------------------
# Add Meal
# -----------------------------

def add_meal(date, meal_type, dish):

    meals = pd.read_csv(MEAL_FILE)

    new_row = pd.DataFrame(
        [[date, meal_type, dish]],
        columns=[
            "Date",
            "Meal Type",
            "Dish"
        ]
    )

    meals = pd.concat(
        [meals, new_row],
        ignore_index=True
    )

    meals.to_csv(
        MEAL_FILE,
        index=False
    )


# -----------------------------
# Add Shopping Item
# -----------------------------

def add_shopping_item(date, item):

    shopping = pd.read_csv(SHOPPING_FILE)

    new_row = pd.DataFrame(
        [[date, item]],
        columns=[
            "Date",
            "Item"
        ]
    )

    shopping = pd.concat(
        [shopping, new_row],
        ignore_index=True
    )

    shopping.to_csv(
        SHOPPING_FILE,
        index=False
    )


# -----------------------------
# Read Meal History
# -----------------------------

def get_meal_history():

    if os.path.exists(MEAL_FILE):

        return pd.read_csv(MEAL_FILE)

    return pd.DataFrame()


# -----------------------------
# Read Shopping History
# -----------------------------

def get_shopping_history():

    if os.path.exists(SHOPPING_FILE):

        return pd.read_csv(SHOPPING_FILE)

    return pd.DataFrame()


# -----------------------------
# Read Recipes
# -----------------------------

def get_recipes():

    if os.path.exists(RECIPE_FILE):

        return pd.read_csv(RECIPE_FILE)

    return pd.DataFrame()