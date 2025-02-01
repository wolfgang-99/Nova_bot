from flask import Flask
import threading
from bot import main

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    # Run Flask in a separate thread
    threading.Thread(target=run_flask).start()
    main()
