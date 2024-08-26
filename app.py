import streamlit as st
import anthropic
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()


# Retrieve the API key from the environment variable
api_key = os.getenv("claude_api_key")

# Function to generate a meal plan using Claude AI
def generate_meal_plan(api_key, fasting, pre_meal, post_meal, preferences):
    # Initialize the Anthropics API client
    client = anthropic.Anthropic(api_key=api_key)

    # Create the system and user messages
    prompt = (
        f"My Fasting Sugar Level is {fasting} mg/dL, "
        f"my Pre-Meal Sugar Level is {pre_meal} mg/dL, "
        f"and my Post-Meal Sugar Level is {post_meal} mg/dL, "
        f"My Dietary Preferences are {dietary_preferences}. "
        "Please provide a personalized meal plan that can help my blood sugar levels effectively."
        )

    # Call the Claude AI model using the messages API
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class nutritionist who specializes in diabets mangement.",
        messages=[
            {
                "role": "user",
                "content": prompt 
            }
        ]
    )

    # Extract the content from the list of messages
    raw_content = response.content
    itinerary = raw_content[0].text
    return itinerary

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

# Input fields for sugar levels and dietary preferences
fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Level (mg/dL)", min_value=0)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Level (mg/dL)", min_value=0)

# Dietary preferences as a multiselect option
dietary_preferences = st.sidebar.text_input("Dietary Preferences (mg/dL) (e.g., vegetarian, low-carb)")

# Display the meal plan in a nicely formatted way
if st.sidebar.button("Generate Meal Plan"):    
    meal_plan = generate_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
    st.write("Based on your sugar level and dietary preferences, here is your personalized meal plan:")
    st.markdown(meal_plan)
 


