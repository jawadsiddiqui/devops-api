from flask import Flask, jsonify, request
import socket
import time
import redis
import os
from prometheus_client import generate_latest, Gauge
from flask_prometheus_metrics import register_metrics

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

# Metrics
version_gauge = Gauge('api_version', 'Current API version')
health_gauge = Gauge('api_health', 'Health of the API')

# API version
VERSION = "0.1.0"

@app.route('/')
def root():
    # Root endpoint that provides current date and version info
    is_kubernetes = os.getenv('KUBERNETES_SERVICE_HOST') is not None
    return jsonify({
        "version": VERSION,
        "date": int(time.time()),
        "kubernetes": is_kubernetes
    })

@app.route('/v1/tools/lookup', methods=['GET'])
def lookup():
    # Resolve IPv4 addresses for a domain
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "domain parameter is required"}), 400

    try:
        # Resolve IPv4 addresses
        ip_addresses = socket.gethostbyname_ex(domain)[2]
        ipv4_addresses = [ip for ip in ip_addresses if '.' in ip]

        # Log successful query
        redis_db.lpush('lookup_history', f"{domain}: {ipv4_addresses}")
        redis_db.ltrim('lookup_history', 0, 19)  # Keep only the latest 20 entries

        return jsonify({"domain": domain, "ipv4_addresses": ipv4_addresses})
    except socket.gaierror:
        return jsonify({"error": "Unable to resolve domain"}), 400

@app.route('/v1/tools/validate', methods=['POST'])
def validate():
    # Validate if input is an IPv4 address
    data = request.json
    if not data or 'ip' not in data:
        return jsonify({"error": "IP address is required"}), 400

    ip = data['ip']
    try:
        socket.inet_aton(ip)
        is_valid = True
    except socket.error:
        is_valid = False

    return jsonify({"ip": ip, "valid": is_valid})

@app.route('/v1/history', methods=['GET'])
def history():
    # Retrieve the latest 20 saved queries from Redis
    history = redis_db.lrange('lookup_history', 0, 19)
    return jsonify({"history": history})

@app.route('/metrics')
def metrics():
    # Prometheus metrics endpoint
    return generate_latest(), 200

@app.route('/health')
def health():
    # Health check endpoint
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
