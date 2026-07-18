from flask import Flask, render_template, request, jsonify

from chatbot import get_response



app = Flask(__name__)




@app.route("/")
def home():

    return render_template(
        "index.html"
    )





@app.route("/chat", methods=["POST"])
def chat():


    user_message = request.json["message"]



    response, sentiment, confidence = get_response(
        user_message
    )



    return jsonify(

        {
            "response": response,
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        }

    )





if __name__ == "__main__":

    app.run(
        debug=True
    )