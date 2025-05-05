from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form ,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import Optional
import shutil
import os
import base64
from io import BytesIO
from PIL import Image

from app.database import SessionLocal, engine
from app import models
from app import face_utils
from app.schemas import UserCreate
from app.auth import authenticate_user_from_np_image
import numpy as np
import re
from starlette.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals["url_for"] = lambda name, **params: (
    f"/static/{params['filename']}" if name == "static" else f"/{name}"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=JSONResponse)
async def register_user(
    username: str = Form(...),
    image: UploadFile = File(None),
    captured_image: str = Form(None),
    db: Session = Depends(get_db)
):
    user_path = os.path.join(UPLOAD_DIR, f"{username}.jpg")

       

    if image and image.filename:
        contents = await image.read()
        try:
            with open(user_path, "wb") as f:
                f.write(contents)
            Image.open(user_path).verify()
        except Exception as e:
            if os.path.exists(user_path):
                os.remove(user_path)
            return JSONResponse(content={"detail": f"Invalid uploaded image: {str(e)}"}, status_code=400)
    elif captured_image:
        match = re.match(r"data:image/(?:jpeg|jpg|png);base64,(.*)", captured_image)
        if not match:
            return JSONResponse(content={"detail": f"Invalid image data: {captured_image[:50]}..."}, status_code=400)
        try:
            image_data = base64.b64decode(match.group(1))
            img = Image.open(BytesIO(image_data))
            img.save(user_path)
        except Exception as e:
            if os.path.exists(user_path):
                os.remove(user_path)
            return JSONResponse(content={"detail": f"Invalid base64 image: {str(e)}"}, status_code=400)
    else:
        return JSONResponse(content={"detail": "No image provided"}, status_code=400)

    face_encoding = face_utils.encode_face(user_path)
    if face_encoding is None:
        if os.path.exists(user_path):
            os.remove(user_path)
        return JSONResponse(content={"detail": "No face found in the image"}, status_code=400)

    if db.query(models.User).filter(models.User.username == username).first():
        return JSONResponse(content={"detail": f"Username {username} already exists"}, status_code=400) 

    db_user = models.User(username=username, encoding=face_encoding.tobytes())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        if os.path.exists(user_path):
            os.remove(user_path)
        return JSONResponse(content={"detail": f"Database error: {str(e)}"}, status_code=500)

    return JSONResponse(content={"message": f"User {username} registered successfully"})

@app.get("/login", response_class=HTMLResponse)
async def login_user(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=JSONResponse)
async def login(
    username: str = Form(...),
    captured_image: str = Form(...),
    db: Session = Depends(get_db)
):
    # More permissive regex to match jpg, jpeg, png, etc.
    match = re.match(r"data:image/(?:jpeg|jpg|png);base64,(.*)", captured_image)
    if not match:
        return JSONResponse(content={"detail": f"Invalid image data: {captured_image[:50]}..."}, status_code=400)

    image_data = base64.b64decode(match.group(1))
    image = Image.open(BytesIO(image_data)).convert("RGB")
    np_image = np.array(image)

    matched_username = authenticate_user_from_np_image(np_image, db)

    if matched_username and matched_username == username:
        return JSONResponse(content={"message": f"Welcome back, {matched_username}!"})
    else:
        return JSONResponse(content={"detail": "Face not recognized or username mismatch"}, status_code=401)


@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request, message: str = "Operation successful"):
    return templates.TemplateResponse("success.html", {"request": request, "message": message})