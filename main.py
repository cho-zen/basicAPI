from fastapi import FastAPI, Body, File, UploadFile
from fastapi.responses import FileResponse
import base64
import cv2
import face_recognition
import pyrebase

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

    with open('templates/image.jpg','wb') as f:
        f.write(image_file)

    image_file = cv2.imread('templates/image.jpg')

    face_loc = face_recognition.face_locations(image_file)
    
    if len(face_loc) == 0:
        return "0"
    else:
        face_enc = face_recognition.face_encodings(image_file)
        return str(face_enc[0])


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
    

@app.post('/uploadcode/{user_number}/{survey}')
def upload_facecode(user_number,survey,text: str=Body(...)):

    with open("templates/image.jpg","wb") as file:
        file.write(base64.b64decode((text)))

    img = cv2.imread('templates/image.jpg')

    face_loc = face_recognition.face_locations(img)
    
    if len(face_loc) == 0:
        return "0"
    else:
        face_enc = face_recognition.face_encodings(img)

        firebase_config = {
        "apiKey": "AIzaSyCUagURc1l3froPMMFLnUHgIs9eOODB9XI",
        "authDomain": "survey-application-c9806.firebaseapp.com",
        "databaseURL": "https://survey-application-c9806-default-rtdb.firebaseio.com",
        "projectId": "survey-application-c9806",
        "storageBucket": "survey-application-c9806.appspot.com",
        "messagingSenderId": "112280167703",
        "appId": "1:112280167703:web:aadeff65cb8141f52d0352"
        }

        firebase = pyrebase.initialize_app(firebase_config)

            # Get the auth object
        auth = firebase.auth()

        # Get the current user
        user = auth.current_user

        # Get the user's token
        token = user

        # Connect to Database
        db = firebase.database()
        db.child(f"Data/{user_number}/{survey}/ImageData").push(str(face_enc[0]),token)

        return "1"
