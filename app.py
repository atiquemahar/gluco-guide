import streamlit as st
import anthropic

api_key = st.secrets["claude_api_key"]

# Title of the app
st.title("GlucoGuide")

# Short description
st.write("""
**GlucoGuide** is a personalized meal planning tool designed specifically for diabetic patients.
By entering your fasting, pre-meal, and post-meal sugar levels, along with your dietary preferences,
you can receive customized meal plans that help you manage your blood sugar levels effectively.
""")

# Sidebar for inputs
st.sidebar.header("Patient Information")

# Retrieve the API key from the secrets file
api_key = st.secrets["claude"]["api_key"]

# Input fields for sugar levels and dietary preferences
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0)

# Dietary preferences as a multiselect option
dietary_preferences = st.sidebar.multiselect(
    "Dietary Preferences",
    ["Low Carb", "Low Sugar", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"]
)

# Function to generate a meal plan using Claude AI
def generate_meal_plan(api_key, fasting, pre_meal, post_meal, preferences):
    # Initialize the Anthropics API client
    client = anthropic.Anthropic(api_key=api_key)

    # Create the prompt
    prompt = (
        f"Create a customized meal plan for a diabetic patient with the following details:\n"
        f"- Fasting Sugar Level: {fasting} mg/dL\n"
        f"- Pre-Meal Sugar Level: {pre_meal} mg/dL\n"
        f"- Post-Meal Sugar Level: {post_meal} mg/dL\n"
        f"- Dietary Preferences: {', '.join(preferences)}\n"
        f"Provide a meal plan that considers these sugar levels and dietary preferences."
    )

    # Call the Claude AI model
    message = client.completions.create(
        model="claude-3-5-sonnet-20240620",  # Model version to be used
        max_tokens=1000,
        temperature=0,  # Low temperature for more deterministic results
        prompt=prompt
    )

    # Extract the meal plan from the response
    meal_plan = message.get('completion', 'Sorry, there was an error generating your meal plan. Please try again.')
    
    # Extract only the required text from the response
    return meal_plan.strip()

# Main area to display the customized meal plan
st.header("Your Customized Meal Plan")

# Generate the meal plan using the API key from the secrets file
meal_plan = generate_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
st.write(meal_plan)
 


