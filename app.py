from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 DevOps Project Running Successfully!"

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # IMPORTANT: host must be 0.0.0.0 for Docker
    app.run(host="0.0.0.0", port=5000)
