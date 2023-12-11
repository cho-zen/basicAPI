from fastapi import FastAPI, Body, File, UploadFile
import base64
import cv2
import face_recognition

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


@app.post("/bash64")
def upload_bashCode(text:str=Body(...)):

    with open("templates/image.jpg","wb") as file:
        file.write(base64.b64decode((text)))

    image = cv2.imread('templates/image.jpg')
    

    return {"Shape":image.shape}


@app.post("/facebash")
def upload_facebashcode(text: str=Body(...)):

    with open("templates/image.jpg","wb") as file:
        file.write(base64.b64decode((text)))

    img = cv2.imread('templates/image.jpg')

    face_loc = face_recognition.face_locations(img)
    
    if len(face_loc) == 0:
        return "0"
    else:
        face_enc = face_recognition.face_encodings(img)
        return str(face_enc[0])

