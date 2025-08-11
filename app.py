from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Gauge

app = Flask(__name__)

# Prometheus metrics
REQUESTS = Counter('app_requests_total', 'Total HTTP requests', ['endpoint', 'method'])
IN_PROGRESS = Gauge('app_inprogress_requests', 'In-progress requests')

@app.before_request
def before():
    IN_PROGRESS.inc()

@app.after_request
def after(response):
    IN_PROGRESS.dec()
    REQUESTS.labels(endpoint=request.path, method=request.method).inc()
    return response

@app.route('/')
def home():
    return jsonify(message="Hello from Kubernetes!")

@app.route('/health')
def health():
    return jsonify(status="healthy")

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
