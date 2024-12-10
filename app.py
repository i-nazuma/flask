from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    sensor_data = {
        'temperature': 22.5,
        'humidity': 60
    }

    temperature = sensor_data.get('temperature')
    humidity = sensor_data.get('humidity')
    return render_template(
    'index.html',
    temperature=temperature,
    humidity=humidity
)


if __name__ == "__main__":
    app.run(debug=True)
