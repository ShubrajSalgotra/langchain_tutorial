from flask import Flask, jsonify, request, render_template
from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = init_chat_model("google_genai:gemini-2.5-flash-lite", api_key=api_key)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")

    if not message:
        return jsonify({"Error": "Message not found"})
    
    messageChain = [
        SystemMessage("You are helpful chatbot."),
        HumanMessage(message),
    ]

    response = model.invoke(messageChain)

    return jsonify({"Reply": response.content})

if __name__ == '__main__':
    app.run(debug=True)