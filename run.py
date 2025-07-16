# test of test
from flask import Flask, render_template 
from flask import request
import os, signal


#initialise program
app = Flask(__name__,   
            template_folder="templates",
            static_folder='static', 
            static_url_path='/')
app.secret_key="sekrit dokumints )))))"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/exit")
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)


# add external site
from fdbsql import engdb
app.register_blueprint(engdb, url_prefix="/engdb")


from processingcore import processing
app.register_blueprint(processing, url_prefix="/process_file")


if __name__ == '__main__':
    import os
    url = "http://127.0.0.1:5000"
    os.startfile(url)
    app.run(debug=True) # after this command, lines from code do not execute, 
    # command runs like "while True"
    
    