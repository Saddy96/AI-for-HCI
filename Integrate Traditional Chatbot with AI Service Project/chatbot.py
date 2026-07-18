from sentiment import analyze_sentiment

def get_response(message):
    text = message.lower()
    # ---------------------------
    # Traditional chatbot rules
    # ---------------------------

    if "hello" in text or "hi" in text:

        response = (
            "Hello! Welcome to the College Assistant chatbot."
        )

    elif "how are you" in text:

        response = (
            "I am doing great! "
            "I am here to help you with university information."
        )
    elif "help" in text:

        response = (
            "I can help you with:\n"
            "- Courses\n"
            "- Admissions\n"
            "- Library information\n"
            "- University services"
        )

    elif "course" in text or "program" in text:

        response = (
            "The available programs include "
            "Artificial Intelligence, Data Science, "
            "and Cybersecurity."
        )

    elif "admission" in text:

        response = (
            "Admission information can be found "
            "through the university admission portal."
        )

    elif "library" in text:

        response = (
            "The library provides academic resources "
            "and online research materials."
        )

    elif "contact" in text:

        response = (
            "You can contact the university support "
            "team through the official website."
        )

    elif "love" in text or "like" in text:

        response = (
            "Thank you for sharing your positive feedback "
            "about the university."
        )

    elif "hate" in text or "bad" in text:

        response = (
            "I understand your concern. "
            "I will try to provide helpful information."
        )

    else:

        response = (
            "Sorry, I do not understand your question. "
            "Please type help to see available options."
        )

    # ---------------------------
    # Hugging Face AI Analysis
    # ---------------------------
    sentiment, confidence = analyze_sentiment(
        message
    )

    # AI response
    if sentiment == "Positive":
        response += (
            "\n\nAI Analysis: "
            "Your message has a positive tone."
        )

    elif sentiment == "Negative":

        response += (
            "\n\nAI Analysis: "
            "Your message has a negative tone."
        )
    else:

        response += (
            "\n\nAI Analysis: "
            "Your message appears neutral."
        )
    return response, sentiment, confidence