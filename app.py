import streamlit as st
import os
import google.generativeai as genai
from google.api_core import exceptions # Import the exceptions module

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define your preferred models in order of fallback
# We'll put Gemini 1.5 Flash first as it often has higher free tier limits due to its efficiency
# and then Gemini 1.5 Pro as a powerful alternative.
# You can adjust this list based on your actual availability and preferences.
AVAILABLE_MODELS = [
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro',
    # You could add more here if needed, e.g., 'models/gemini-1.5-flash-8b'
]

# ... (rest of your imports and setup) ...

def generate_birthday_message(recipient_first_name, recipient_last_name, birth_year, relationship, details):
    prompt = (
        f"Write a personalized, heartfelt, and **beautifully poetic** birthday greeting for {recipient_first_name} {recipient_last_name}, "
        f"who was born in {birth_year}. The recipient is related to me this way: {relationship}. "
        f"Here are some details to **inspire and weave into** the message (use them creatively, not necessarily verbatim): {details}. "
        "Make the message warm, meaningful, and memorable. "
        "**Crucially, prioritize strong, natural poetic flow and elegant. Embrace half-rhymes or internal rhymes if they improve the overall poem's quality.** "
        "Aim for around 5-10 lines, allowing for slight variation if it enhances the poem's artistry. "
        "**Format the output as a poem with distinct lines and stanzas, using newline characters (`\\n`) for clear breaks.** "
        "Return only the final, **rhyming and poetic birthday message**."
    )

    # ... (rest of your model fallback logic) ...

    generated_message = None
    used_model = None

    for model_name in AVAILABLE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            st.info(f"Attempting to generate message with model: {model_name}...")
            response = model.generate_content(prompt)
            generated_message = response.text
            used_model = model_name
            break # If successful, break out of the loop
        except exceptions.ResourceExhausted as e:
            st.warning(f"Quota exceeded for {model_name}. Trying next available model if any. Error: {e}")
        except exceptions.NotFound as e:
            st.warning(f"Model {model_name} not found or unavailable. Trying next available model if any. Error: {e}")
        except Exception as e: # Catch any other unexpected errors
            st.error(f"An unexpected error occurred with {model_name}. Trying next available model if any. Error: {e}")

    if generated_message:
        return generated_message, used_model # Return both message and the model that worked
    else:
        return "Sorry, I couldn't generate a birthday message at this time. All available models failed due to quotas or unavailability. Please try again later.", None

st.title("Birthday AI App")

recipient_first_name = st.text_input("Recipient First Name")
recipient_last_name = st.text_input("Recipient Last Name")
birth_year = st.text_input("Birth Year")
relationship = st.text_input("Relationship to You")
details = st.text_input("Additional Details (hobbies, memories, etc.)")

if st.button("Generate Birthday Message"):
    if not recipient_first_name or not recipient_last_name or not birth_year or not relationship or not details:
        st.warning("Please fill in ALL the fields to generate a message!")
    else:
        with st.spinner("Crafting your personalized message..."):
            birthday_message, used_model = generate_birthday_message(
                recipient_first_name,
                recipient_last_name,
                birth_year,
                relationship,
                details
            )
        if used_model:
            st.success(f"Message Generated using {used_model}!")
            st.text(birthday_message)
            st.info("Copy the message above!")
        else:
            st.error(birthday_message) # Display the error message returned from the function