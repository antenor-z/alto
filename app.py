from dataclasses import dataclass
from json import load
from flask import Flask, redirect, render_template, request, Response, session
from config import Config, get_config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from stream import generate_frames
from cam import CameraController
from totp import check2fa
import threading
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
controller = CameraController()
config: Config = get_config()

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)

app.config['SECRET_KEY'] = config.session_key

@app.route('/')
def index():
    try_logged()
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    try_logged()
    return Response(generate_frames(rtsp_url=config.RTSP_URL), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    try_logged()
    direction = request.form.get('direction')
    if direction:
        thread = threading.Thread(target=controller.move, args=(direction,))
        thread.start()
    return '', 204

@app.get("/login")
@limiter.limit("5 per hour")
def get_login():
    return render_template("login.html")

@app.get("/logout")
@limiter.limit("5 per hour")
def logout():
    session.pop("is_logged")
    return redirect("/")

class NotLoggedError(Exception):
    ...

def try_logged():
    if session.get("is_logged") != True:
        raise NotLoggedError

@app.post("/login")
@limiter.limit("5 per hour")
def post_login():
    user_name = request.form.get('user')
    passwd = request.form.get('password')
    totp = request.form.get('totp')
    if user_name == config.user and passwd == config.password and check2fa(config.totp_token, totp):
        session["is_logged"] = True
    return redirect("/")

@app.errorhandler(NotLoggedError)
def not_logged(e):
    return redirect("/login")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
