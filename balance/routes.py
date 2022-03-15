from balance import app

@app.route("/")
def home():
    return "Working"