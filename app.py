from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Define a simple route
@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/offer" , methods=['GET'])
def offer():
    return "This is offer API"


@app.rute("/leads/uploads", methods=['POST'])
def upload_leads():
    return "This is leads upload API"


@app.route("/score", methods=['POST'])
def score():
    # TODO: Implement scoring logic here
    return "this is a score API"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
