from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_radar', methods=['POST'])
def generate_radar():
    data = request.get_json()
    df = pd.DataFrame(data)

    metrics = df['Metric'].tolist()
    series = df.drop('Metric', axis=1).to_dict(orient='list')

    colors = [
        ("rgba(255, 99, 132, 1)", "rgba(255, 99, 132, 0.2)"),
        ("rgba(54, 162, 235, 1)", "rgba(54, 162, 235, 0.2)"),
        ("rgba(255, 206, 86, 1)", "rgba(255, 206, 86, 0.2)"),
        ("rgba(75, 192, 192, 1)", "rgba(75, 192, 192, 0.2)"),
        ("rgba(153, 102, 255, 1)", "rgba(153, 102, 255, 0.2)"),
        ("rgba(255, 159, 64, 1)", "rgba(255, 159, 64, 0.2)")
    ]

    radar_data = {"labels": metrics, "datasets": []}

    for idx, (series_name, values) in enumerate(series.items()):
        border, background = colors[idx % len(colors)]
        radar_data["datasets"].append({
            "label": series_name,
            "data": values,
            "fill": True,
            "borderColor": border,
            "backgroundColor": background,
            "pointBackgroundColor": border,
            "pointBorderColor": "#fff",
            "pointHoverBackgroundColor": "#fff",
            "pointHoverBorderColor": border
        })

    return jsonify(radar_data)

if __name__ == '__main__':
    # 本地调试用，Render 部署时会用 gunicorn 启动
    app.run(host='0.0.0.0', port=5000, debug=True)
