import os
from flask import Flask

app = Flask(__name__)

print("Template folder:", app.template_folder)

if __name__ == "__main__":
    app.run(debug=True)
