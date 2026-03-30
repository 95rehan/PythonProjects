from flask import Flask
app = Flask(__name__)

@app.route("/home/<name>")
def hello_world(name):   
    return f"<p>Hello World !</p>"

def authenticate(token : str) -> bool:
    return True if token == 'abc' else False
    
@app.route('/login/<token>')
def login(token):
    if authenticate(token=token):
        return f"<p>Login succesfully !</p>"
    else:
        return f"<p>Sorry Coule not authenticate with token !</p>"



if __name__ == '__main__':
    app.run()