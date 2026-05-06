from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

@app.route('/track/<num>')
def track(num):
    # Mengambil User-Agent (Merek/Tipe HP)
    ua = request.headers.get('User-Agent')
    ip = request.remote_addr
    log = f"[{datetime.datetime.now()}] Target {num} | IP: {ip} | Device: {ua}\n"
    
    with open("tracker_logs.txt", "a") as f:
        f.write(log)
    
    return redirect("https://www.google.com")

if __name__ == "__main__":
    print("Tracker active on port 5000...")
    app.run(host='0.0.0.0', port=5000)