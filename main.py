from fastapi import FastAPI, Body, File, UploadFile

app = FastAPI()


@app.get('/')
def index():
    return "Hello World!"


@app.post("/upload")
def upload_text(text: str=Body(...)):
    return text


@app.post('/uploadimg')
async def upload_image(image: UploadFile= File(...)):
    
    image_file = await image.read()
    # with open('template/image.jpg','wb') as f:
    #     f.write(image_file)

    return "Done"
