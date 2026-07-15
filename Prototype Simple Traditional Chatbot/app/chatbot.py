def get_response(message):

    message = message.lower().strip()

    if message in ["hello", "hi", "hey"]:
        return "Hello! Welcome to my chatbot."

    elif "help" in message:
        return """
        I can help you with:
        - admissions
        - courses
        - library
        - contact
        """

    elif "admission" in message:
        return "Admissions are open for Fall and Spring semesters."

    elif "course" in message:
        return "Available programs include AI, Data Science, and Cybersecurity."

    elif "library" in message:
        return "Library hours are Monday-Friday 8 AM to 8 PM."

    elif "contact" in message:
        return "You can contact student services through the university portal."

    elif message in ["bye", "exit", "Thank", "thanks"]:
        return "Goodbye! Have a great day."

    else:
        return "Sorry, I did not understand. Type 'help' to see options."