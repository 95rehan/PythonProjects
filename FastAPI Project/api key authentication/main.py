from fastapi import FastAPI


app = FastAPI()





@app.get('/login')
def home(api_key):
    return f"Hello {name}"




