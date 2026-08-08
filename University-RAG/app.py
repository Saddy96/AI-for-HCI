"""
app.py

Gradio user interface for
University Information Assistant
"""


import gradio as gr

from rag import ask_question

from config import (
    APP_TITLE,
    APP_DESCRIPTION
)



##################################################
# Chat Function
##################################################

def chat(message, history):


    result = ask_question(message)


    answer = result["answer"]


    sources = result["sources"]



    if sources:

        answer += "\n\nSources:\n"

        for source in sources:

            answer += f"- {source}\n"



    history.append(

        {

            "role":"user",

            "content":message

        }

    )


    history.append(

        {

            "role":"assistant",

            "content":answer

        }

    )


    return "", history


##################################################
# Clear Chat
##################################################

def clear_chat():

    return []



##################################################
# Gradio Interface
##################################################

with gr.Blocks(

    title=APP_TITLE

) as demo:



    gr.Markdown(

        f"""

# 🎓 {APP_TITLE}


{APP_DESCRIPTION}


Ask questions about:

- Registration
- Academic policies
- Financial aid
- Graduation requirements
- Student services
- Technology support


"""

    )



    chatbot = gr.Chatbot(

    height=500,

    type="messages"

)



    message = gr.Textbox(

        placeholder=

        "Ask a university question...",

        label="Question"

    )



    with gr.Row():

        submit = gr.Button(

            "Ask"

        )


        clear = gr.Button(

            "Clear"

        )



    submit.click(

        chat,

        inputs=[

            message,

            chatbot

        ],

        outputs=[

            message,

            chatbot

        ]

    )



    message.submit(

        chat,

        inputs=[

            message,

            chatbot

        ],

        outputs=[

            message,

            chatbot

        ]

    )



    clear.click(

        clear_chat,

        outputs=chatbot

    )



##################################################
# Launch Application
##################################################

if __name__ == "__main__":


    demo.launch(

        server_name="127.0.0.1",

        server_port=7860,

        share=False

    )