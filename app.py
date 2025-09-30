from flask import Flask
import scheduler  # this is your scheduler.py code (make sure it’s structured as functions)

app = Flask(__name__)

@app.route("/run-diet")
def run_diet():
    # Call your scheduler logic
    result = scheduler.run_scheduler()
    return f"Executed: {result}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
