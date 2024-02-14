from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

def init_app():
    app = Flask(__name__)
    CORS(app)
    key_file = open('key.txt', mode='r')
    key = key_file.readline().strip()
    client = OpenAI(api_key=key)

    @app.route("/query", methods=['POST'])
    def query():
        try:
            request_data = request.json
            query = request_data.get('query')

            print(query)

            return {"answer": "Hi! The backend is working"}, 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return app

if __name__ == '__main__':
    app = init_app()
    # print(f"KEY: {key}")
    app.run(debug=True)