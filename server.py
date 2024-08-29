from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from my_agent.agent import AgenticRAG

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        agent = AgenticRAG()
        user_query = request.form.get('user_query', '')
        response = agent.run({"user_query": user_query, "steps": []})
        #return render_template('index.html', final_response=response["final_response"], user_query=user_query)
        
        # Extract sub-questions and sub-answers from the response
        sub_questions = response.get("sub_questions", [])
        sub_answers = response.get("sub_answers", [])
        
        return render_template('index.html', 
                               final_response=response["final_response"], 
                               user_query=user_query,
                               sub_questions=sub_questions,
                               sub_answers=sub_answers)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)