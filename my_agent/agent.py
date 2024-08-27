from utils.nodes import transform_query, CRAG_loop, consolidate
from utils.state import GraphState
from langgraph.graph import START, END, StateGraph
from IPython.display import Image, display
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

nested_CRAG = StateGraph(GraphState)
nested_CRAG.add_node("transform_query", transform_query)  # retrieve
nested_CRAG.add_node("CRAG_loop",CRAG_loop)
nested_CRAG.add_node("consolidate",consolidate)
nested_CRAG.set_entry_point("transform_query")
nested_CRAG.add_edge("transform_query", "CRAG_loop")
nested_CRAG.add_edge("CRAG_loop", "consolidate")
nested_CRAG.add_edge("consolidate", END)

agentic_rag = nested_CRAG.compile()

display(Image(agentic_rag.get_graph(xray=True).draw_mermaid_png()))

#test_question = "Is the combined age of Justin Beiber and Bradd Pitt greater than Sidney Crosby's Jersey Number?"

#response = agentic_rag.invoke({"user_query": test_question, "steps": []})

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_agentic_rag():
    data = request.json
    user_query = data.get('user_query', '')
    response = agentic_rag.invoke({"user_query": user_query, "steps": []})
    
    # Print the response object for debugging
    print(response)
    sub_answers = response.get("sub_answers", [])
    sub_questions = response.get("sub_questions", [])
    question_answers = list(zip(sub_questions, sub_answers))
    
    # Prepare the question_answers for the API response
    formatted_qa = [{"question": q, "answer": a} for q, a in question_answers]
    final_response = response["final_response"]
    return jsonify({"Partial Answers": formatted_qa, "Final Response": response["final_response"]})
    #return render_template('results.html', partial_answers=formatted_qa, final_response=final_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)