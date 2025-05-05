# Face Recognition Attendance System

This project is a web application that uses facial recognition to manage attendance. Users can register and log in using their face via a webcam, and administrators can view a list of registered users. The application is built with FastAPI, Python, and face recognition libraries like `dlib` and `face_recognition`.

## Directory Structure

- `app/`: Contains backend logic and utilities (e.g., `database.py`, `models.py`, `face_utils.py`, `auth.py`, `schemas.py`).
- `static/`: Stores static files like `style.css` for frontend styling.
- `templates/`: Contains Jinja2 templates (`index.html`, `login.html`, `register.html`, `success.html`, `users.html`, `base.html`) for rendering HTML pages.
- `test/`: Directory for test scripts or files (currently empty or placeholder).
- `uploads/`: Stores user-uploaded images (e.g., face photos for registration).
- `.gitignore`: Specifies files/directories to ignore in Git (e.g., `__pycache__`, `uploads/`).
- `README.md`: Project documentation (this file).
- `dlib-19.22.99-cp310-cp310-win_amd64.whl`: A precompiled `dlib` wheel file for Windows (Python 3.10), used for face recognition.
- `face_recog.db`: SQLite database file storing user data (e.g., usernames, face encodings).
- `main.py`: Main FastAPI application file containing routes and logic.
- `requirements.txt`: Lists project dependencies (e.g., `fastapi`, `uvicorn`, `face_recognition`).

## Prerequisites

- **Python 3.10**: Ensure Python 3.10 is installed (matches the `dlib` wheel version).
- **pip**: Python package manager for installing dependencies.
- **Webcam**: Required for capturing face images during login/registration.
- **Dependencies**: Listed in `requirements.txt`.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/abdelrahman-elseht/Attendance-System.git
   cd Attendance-System
   ```

2. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   **or using conda**
   ```bash
   conda create -n Attendance-System python=3.10
   conda activate Attendance-System
   ```

3. **Install Dependencies**: Install the required packages, including the precompiled `dlib` wheel.

   ```bash
   pip install -r requirements.txt
   pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
   ```

   Ensure `requirements.txt` includes:

   ```
    face_recognition == 1.3.0
    opencv-python == 4.8.0.76
    cmake == 3.26.0
    numpy == 1.24.3
    fastapi == 0.104.1
    sqlalchemy == 2.0.36
    pydantic == 2.5.3
    python-multipart == 0.0.19
    uvicorn == 0.24.0
    jinja2 == 3.1.2
    python-multipart == 0.0.19
   ```

4. **Create Necessary Directories**: The `uploads/` directory should already exist (as per the structure). If not:

   ```bash
   mkdir uploads
   ```

5. **Initialize the Database**: The application uses SQLite (`face_recog.db`). The database is created automatically when you run `main.py` for the first time, as `models.Base.metadata.create_all` is called.

## Usage

1. **Run the Application**: Start the FastAPI server using `uvicorn`.

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the Application**: Open your browser and navigate to:

   ```
   http://127.0.0.1:8000/
   ```

3. **Interact with the Application**:

   - **Home Page (**`/`**)**: Landing page with links to login, register, and view users.
   - **Register (**`/register`**)**: Register a new user by providing a username and capturing a face image via webcam.
   - **Login (**`/login`**)**: Log in by providing a username and capturing a face image for authentication.
   - **Users (**`/users`**)**: View a list of registered users.
   - **Success (**`/success`**)**: Displays a success message after login/registration.

## Routes

- `GET /`: Landing page.
- `GET /register`: Displays the registration form.
- `POST /register`: Handles user registration with face image.
- `GET /login`: Displays the login form.
- `POST /login`: Authenticates user via face recognition.
- `GET /users`: Displays a list of registered users.
- `GET /success`: Shows a success message after login/registration.

