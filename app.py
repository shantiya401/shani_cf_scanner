from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import ipaddress
import requests
import time

app = Flask(__name__)
socketio = SocketIO(app)

cf_ips = [
    '104.24.0.0/14', '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22', '103.31.4.0/22',
    '141.101.64.0/18', '108.162.192.0/18', '190.93.240.0/20', '188.114.96.0/20',
    '197.234.240.0/22', '198.41.128.0/17', '162.158.0.0/15', '104.16.0.0/13',
    '172.64.0.0/13', '131.0.72.0/22'
]

def ping(ip):
    try:
        result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.PIPE, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                if "time=" in line:
                    ping_time = line.split("time=")[1].split("ms")[0]
                    return float(ping_time)
        return None
    except Exception as e:
        print(f'Error pinging {ip}: {e}')
    return None

def speed_test(ip, url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        speed = len(response.content) / (end_time - start_time)
        return round(speed / (1024 * 1024), 2)
    except requests.RequestException as e:
        print(f'Error during speed test for {ip}: {e}')
        return "Failed"

@app.route('/')
def index():
    url = 'https://speed.cloudflare.com/__down?bytes=10485760'
    selected_ip_range = cf_ips[0]
    num_ips = 5
    max_ping = 1000
    return render_template('index.html', cf_ips=cf_ips, selected_ip_range=selected_ip_range, num_ips=num_ips, max_ping=max_ping, test_url=url)

@app.route('/start_scan', methods=['POST'])
def start_scan():
    selected_ip_range = request.form.get('selected_ip_range')
    url = request.form.get('test_url')
    num_ips = int(request.form.get('num_ips', 5))
    max_ping = int(request.form.get('max_ping', 1000))

    ip_network = ipaddress.ip_network(selected_ip_range)
    available_ips = list(ip_network.hosts())
    results = []
    scan_details = []

    healthy_ips = []

    for ip in available_ips:
        ping_time = ping(str(ip))
        if ping_time is None:
            msg = f'testing {ip} Request timed out. (100% loss)'
            scan_details.append({'ip': str(ip), 'message': msg, 'status': 'failed'})
            socketio.emit('update', f'<span style="color:red;">{msg}</span>')
        elif ping_time > max_ping:
            msg = f'testing {ip} ping: {ping_time}ms rejected'
            scan_details.append({'ip': str(ip), 'message': msg, 'status': 'rejected'})
            socketio.emit('update', f'<span style="color:red;">{msg}</span>')
        else:
            speed = speed_test(str(ip), url)
            msg = f'testing {ip} ping: {ping_time}ms ok'
            scan_details.append({'ip': str(ip), 'message': msg, 'status': 'ok'})
            socketio.emit('update', f'<span style="color:green;">{msg}</span>')
            results.append({'ip': str(ip), 'ping': ping_time, 'speed': speed})
            healthy_ips.append(str(ip))
            if len(healthy_ips) >= num_ips:
                break

    return jsonify({'results': results, 'details': scan_details})



@app.route('/test_ping', methods=['POST'])
def test_ping():
    url = request.form.get('test_url')
    num_ips = int(request.form.get('num_ips', 5))
    max_ping = int(request.form.get('max_ping', 1000))
    selected_ip_range = request.form.get('selected_ip_range')

    ip_network = ipaddress.ip_network(selected_ip_range)
    available_ips = list(ip_network.hosts())[:num_ips]
    results = []
    details = []

    for ip in available_ips:
        ping_time = ping(str(ip))
        if ping_time and float(ping_time) < max_ping:
            results.append((str(ip), ping_time, 'Pending'))
            details.append(f'Ping test for {ip}: {ping_time} ms')
        else:
            details.append(f'Ping test for {ip} failed or was too high')

    return jsonify({'results': results, 'details': details})

@app.route('/test_speed', methods=['POST'])
def test_speed():
    url = request.form.get('test_url')
    num_ips = int(request.form.get('num_ips', 5))
    selected_ip_range = request.form.get('selected_ip_range')

    ip_network = ipaddress.ip_network(selected_ip_range)
    available_ips = list(ip_network.hosts())[:num_ips]
    results = []
    details = []

    for ip in available_ips:
        speed = speed_test(str(ip), url)
        results.append((str(ip), 'N/A', speed))
        details.append(f'Speed test for {ip}: {speed} MB/s')

    return jsonify({'results': results, 'details': details})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
