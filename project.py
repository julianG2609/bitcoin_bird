from flask import Flask, render_template
import game
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def run_flask():
    app.run('localhost', 1205, True, False)

def main():
    # Check if a command-line argument was provided
    if len(sys.argv) != 2 or sys.argv[1] not in ['server', 'game']:
        print("Usage: python project.py [server|game]")
        return

    if sys.argv[1] == 'server':
        run_flask()
    elif sys.argv[1] == 'game':
        game.main_game()

if __name__ == "__main__":
    main()
