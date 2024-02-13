from flask import Flask

app = Flask(__name__)

@app.route("/query")
def query():
    return 'Hi! The backend is working'

if __name__ == '__main__':
    app.run(debug=True)