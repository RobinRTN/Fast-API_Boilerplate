from extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("A client connected")
    socketio.emit("server_message", {"message": "Welcome!"})


@socketio.on("disconnect")
def handle_disconnect():
    print("A client disconnected")

@socketio.on_error_default
def default_error_handler(e):
    app.logger.error(f"Unhandled WebSocket error: {e}")
