from flask import Flask, jsonify, request, render_template, session
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = init_chat_model("google_genai:gemini-2.5-flash-lite", api_key=api_key)


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")

@app.route("/")
def home():
    if "chatHistory" not in session:
        session["chatHistory"] = []
    print(session)
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")

    if not message:
        return jsonify({"Error": "Message not found"})
    
    if "chatHistory" not in session:
        session["chatHistory"] = []

    messageChain = [
        SystemMessage("You are helpful chatbot."),
    ]

    for chat in session["chatHistory"]:
        if chat["role"] == "user":
            messageChain.append(HumanMessage(chat["content"]))
        else:
            messageChain.append(AIMessage(chat["content"]))

    messageChain.append(HumanMessage(message))

    response = model.invoke(messageChain)
    session["chatHistory"].append({"role": "user", "content": message})
    session["chatHistory"].append({"role": "AI", "content": response.content})

    session.modified = True
    print(session)

    return jsonify({"Reply": response.content})

@app.route("/clear", methods=["POST"])
def clear():
    session["chatHistory"] = []
    session.modified = True

    return jsonify({"Message": "Chat Cleared"})


if __name__ == '__main__':
    app.run(debug=True)