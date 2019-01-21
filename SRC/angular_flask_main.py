from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="../Templates", static_folder="../static")
CORS(app)


@app.route('/')
def main_page():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return main_page()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="40876", debug=False, threaded=True)
