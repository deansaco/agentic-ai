from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from my_agent.agent import AgenticRAG
from flask import Response
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        agent = AgenticRAG()
        user_query = request.form.get('user_query', '')
        
        def generate():
            for chunk in agent.run({"user_query": user_query, "steps": []}):
                if isinstance(chunk, dict):
                    yield f"data: {json.dumps(chunk)}\n\n"
                else:
                    yield f"data: {json.dumps({'text': str(chunk)})}\n\n"
            yield "data: [DONE]\n\n"

        return Response(generate(), mimetype='text/event-stream')
    
    return render_template('index.html')


# @app.route('/stream', methods=['POST'])
# def stream():
#     agent = AgenticRAG()
#     user_query = request.json.get('user_query', '')

#     def generate():
#         for chunk in agent.run({"user_query": user_query, "steps": []}):
#             yield f"data: {json.dumps(chunk)}\n\n"

#     return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)\

