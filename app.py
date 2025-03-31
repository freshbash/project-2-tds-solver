import asyncio
from flask import Flask, request, jsonify

from parse_question import query_openai
from get_solution import get_solution

app = Flask(__name__)

@app.route("/api/", methods=["POST"])
def solve_assignment():
    question = request.form.get("question")
    file = request.files.get("file")
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    qid=asyncio.run(query_openai(question))

    print(qid)

    result = get_solution(qid, question, file)

    return jsonify({
        "answer": result
    })

if __name__ == "__main__":
    app.run(debug=True)
