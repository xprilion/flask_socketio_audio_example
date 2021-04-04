"""Audio Recording Socket.IO Example

Implements server-side audio recording.
"""
import os
import uuid
import wave
from flask import current_app, session, url_for, Flask, jsonify
from flask_socketio import emit, SocketIO
from io import BytesIO
from pydub import AudioSegment

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

app.config['FILEDIR'] = "uploads/"
#bp = Blueprint('audio', __name__, static_folder='static',
#               template_folder='templates')

@socketio.on('start-recording')
def start_recording(options):
    """Start recording audio from the client."""
    id = uuid.uuid4().hex  # server-side filename
    session['wavename'] = id + '.wav'
    wf = wave.open(app.config['FILEDIR'] + session['wavename'], 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    session['wavefile'] = wf


@socketio.on('write-audio')
def write_audio(data):
    print(data)
    """Write a chunk of audio from the client."""
    session['wavefile'].writeframes(data)


@socketio.on('end-recording')
def end_recording():
    """Stop recording audio from the client."""
    session['wavefile'].close()
    print(session["wavename"])
    del session['wavefile']
    del session['wavename']

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='6789')
