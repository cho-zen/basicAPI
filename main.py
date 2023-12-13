from fastapi import FastAPI, Body, File, UploadFile
from fastapi.responses import FileResponse
import base64
import cv2
import face_recognition
import pyrebase
import re
import ast
import numpy as np

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
    

# @app.post('/uploadcode/{user_number}/{survey}')
# def upload_facecode(user_number,survey,text: str=Body(...)):

#     with open("templates/image.jpg","wb") as file:
#         file.write(base64.b64decode((text)))

#     img = cv2.imread('templates/image.jpg')

#     face_loc = face_recognition.face_locations(img)
    
#     if len(face_loc) == 0:
#         return "0"
#     else:
#         face_enc = face_recognition.face_encodings(img)

#         firebase_config = {
#         "apiKey": "AIzaSyCUagURc1l3froPMMFLnUHgIs9eOODB9XI",
#         "authDomain": "survey-application-c9806.firebaseapp.com",
#         "databaseURL": "https://survey-application-c9806-default-rtdb.firebaseio.com",
#         "projectId": "survey-application-c9806",
#         "storageBucket": "survey-application-c9806.appspot.com",
#         "messagingSenderId": "112280167703",
#         "appId": "1:112280167703:web:aadeff65cb8141f52d0352"
#         }

#         firebase = pyrebase.initialize_app(firebase_config)

#             # Get the auth object
#         auth = firebase.auth()

#         # Get the current user
#         user = auth.current_user

#         # Get the user's token
#         token = user

#         # Connect to Database
#         db = firebase.database()
#         db.child(f"Data/{user_number}/{survey}/ImageData").push(str(face_enc[0]),token)

#         return "1"

@app.post('/uploadcode/{user_number}/{survey}/{file_name}')
def upload_facecode(user_number,survey,file_name,text: str=Body(...)):

    with open("templates/image.jpg","wb") as file:
        file.write(base64.b64decode((text)))

    img = cv2.imread('templates/image.jpg')

    face_loc = face_recognition.face_locations(img)
    
    if len(face_loc) == 0:
        return 0
    else:
        face_enc = face_recognition.face_encodings(img)
        
        db.child(f"Data/{user_number}/{survey}/ImageData/{file_name}").set(str(face_enc[0]),token)

        return str(face_enc[0])



@app.post("/matchface/{user_number}/{survey}/{file_name}")
def match_faces(user_number,survey,file_name,text: str=Body(...)):

    data = db.child(f"Data/{user_number}/{survey}/ImageData/").get()
    keys_list = list(data.val().keys())
    try:
        keys_list.remove(file_name)
    except:
        pass

    all_faces = list()
    for keys in keys_list:
        data = db.child(f"Data/{user_number}/{survey}/ImageData/{keys}").get().val()

        modified_string = re.sub(r'\s+', ',', data)
        output_list = np.array(ast.literal_eval(modified_string))

        all_faces.append(output_list)

    new_face = db.child(f"Data/{user_number}/{survey}/ImageData/{file_name}/").get().val()
    modified_string = re.sub(r'\s+', ',', new_face)
    new_face = np.array(ast.literal_eval(modified_string))

    match = face_recognition.compare_faces(all_faces,new_face)
    count = sum(bool(x) for x in match)

    if count == 0:
        return 0
    else:
        return 1
