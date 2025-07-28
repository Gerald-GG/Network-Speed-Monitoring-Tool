from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def graph():
    graph_path = os.path.join('logs', 'speed_graph.png')
    return send_from_directory('logs', 'speed_graph.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
