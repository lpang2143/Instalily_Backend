from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import Agent
import os

global app

def init_app():
    global app
    app = Flask(__name__)
    CORS(app)
    # key_file = open('key.txt', mode='r')
    # key = key_file.readline().strip()
    # client = OpenAI(api_key=key)
    global agent
    agent = None

    @app.route("/query", methods=['POST'])
    def query():
        try:
            global agent
            request_data = request.json
            query = request_data.get('query')
            os.environ['QUERY'] = query
            if not agent:
                print('Creating Agent')
                agent = Agent()
            print(f"Querying agent with: {query}")
            response = agent.query(query)
            # print(f"Agent History: {agent.get_history()}\n---\n")

            return {"answer": response['output']}, 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return app

if __name__ == '__main__':
    key_file = open('key.txt', mode='r')
    key = key_file.readline().strip()
    os.environ['OPENAI_API_KEY'] = key

    pinecone_key_file = open('pinecone_key.txt', mode='r')
    pinecone_key = pinecone_key_file.readline().strip()
    os.environ['PINECONE_KEY'] = pinecone_key
    app = init_app()
    # print(f"KEY: {key}")
    app.run(port=os.environ.get('PORT', 5000), debug=True)