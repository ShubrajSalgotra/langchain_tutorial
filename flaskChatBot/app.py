from flask import Flask, jsonify, request, render_template
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os


load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

model = init_chat_model("gemini-3.5-flash")


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