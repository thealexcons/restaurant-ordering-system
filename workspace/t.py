from flask import Flask, render_template

# Initialise the Flask application
app = Flask(__name__)

# The home (menu) page of the web app
@app.route('/')
def menu():
    return render_template("menu.html", title="Menu")
    
# This runs the application
if __name__ == '__main__':
    app.run(debug=True)
    
