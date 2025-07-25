from fastapi import FastAPI
import uvicorn
import firebase_admin
from firebase_admin import credentials,auth
import pyrebase
from models import SingUpSchema,LoginSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request


#replace pyrebase with offfical firebase admin sdk after november 2025, as after 2025 outdated packages like pyrebase will be removed

app=FastAPI(
  description='This is a simple app to show Fierbase Auth with FastAPI',
  title='Firebase Auth',
  docs_url="/")

if not firebase_admin._apps:
  cred = credentials.Certificate("serviceAccountKey.json")
  firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyCJyTDKDCNwFRwtTXkYSOlti-N2JqO_2WU",
  "authDomain": "auth-c2e33.firebaseapp.com",
  "projectId": "auth-c2e33",
  "storageBucket": "auth-c2e33.firebasestorage.app",
  "messagingSenderId": "143840179470",
  "appId": "1:143840179470:web:beef178ecdf678f3af535f",
  "measurementId": "G-QXBT8NSTNT",
  "databaseURL":""
};

firebase = pyrebase.initialize_app(firebaseConfig)

@app.post('/register')
async def create_an_account(user_data:SingUpSchema):
  email=user_data.email
  password=user_data.password

  try:
    user= auth.create_user(
      email=email,
      password=password
      )
    return JSONResponse(content={"message":f"User account created successfully for user {user.uid} "},
                        status_code=201)


  except auth.EmailAlreadyExistsError:
    raise HTTPException(
      status_code=400,
      detail=f"Account already created for the email{email}"
    )
  


@app.post('/login')
async def create_access_token(user_data:LoginSchema):
  email=user_data.email
  password=user_data.password

  try:
    user=firebase.auth().sign_in_with_email_and_password(
      email=email,
      password=password
    )

    token=user['idToken']
    return JSONResponse(
      content={
        "token":token,
      },status_code=200
      
    )

  except:
    raise HTTPException(
      status_code=400,detail="Invalid Credentials"
    )


@app.post('/ping')
async def validate_token(request:Request):
  headers=request.headers
  jwt=headers.get('authorization')

  user=auth.verify_id_token(jwt)
  return user["user_id"]
  

if __name__=="__main__":
  uvicorn.run("main:app",reload=True)