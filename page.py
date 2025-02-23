from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb.cursors import DictCursor
import bcrypt  
import cv2
import numpy as np
from datetime import timedelta
import uuid
import os
import logging
app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

app.secret_key = "secret-key"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "criminal_database"

mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def login():
    errors = [] 

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email:
            errors.append("Please enter your email.")
        if not password:
            errors.append("Please enter your password.")

        if errors:
            return render_template("login.html", errors=errors)

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            users = cursor.fetchone()
            cursor.close()

            if users and users["password"]== password:
                session["loggedin"] = True
                session["email"] = users["email"]
                return redirect(url_for("dashboard"))
            else:
                errors.append("Invalid Email or Password. Please try again!")

        except Exception as e:
            errors.append(f"Database error: {str(e)}")

    return render_template("login.html", errors=errors)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route('/add-data', methods=['POST'])
def add_data():
    errors = []
    
    if request.method == 'POST':
        try:
            # Extract form data
            full_name = request.form['full_name']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            title = request.form['title']
            crime_description = request.form['crime_description']
            case_number = request.form['case_number']
            arrest_date = request.form['arrest_date']
            court_name = request.form['court_name']
            sentencing_date = request.form['sentencing_date']
            previous_criminal_history = request.form['previous_criminal_history']
            last_known_address = request.form['last_known_address']
            district = request.form['district']
            state = request.form['state']
            additional_notes = request.form['additional_notes']
            images = request.files.getlist('images')  # List of images uploaded

            # Check if images were uploaded
            if not images:
                errors.append("At least one image is required.")

            if errors:
                return render_template("dashboard.html", errors=errors)  # Return errors if any
            
            uid=str(uuid.uuid4())
            unique_folder_name = full_name + uid
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_folder_name)

            # Create the folder to store images
            os.makedirs(folder_path, exist_ok=True)

            # Save each uploaded image in the newly created folder
            image_paths = []
            img_name=""
            c=0
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    if c==0:
                        img_name=uid+filename
                        filename = img_name
                        c+=1
                    image_path = os.path.join(folder_path, filename)
                    image.save(image_path)
                    image_paths.append(image_path)
                else:
                    errors.append(f"Invalid file type for {image.filename}")

            if errors:
                error_msg = "; ".join(errors)
                return redirect(url_for('dashboard', status=400, msg=error_msg))

            # Store the folder name (you could store individual image paths too, depending on your needs)
            image_folder_name = unique_folder_name  # Store the folder name, not the full file paths

            # SQL query to insert data into the database
            query = """
                INSERT INTO criminal_records (full_name, date_of_birth, gender, title, crime_description, 
                case_number, arrest_date, court_name, 
                sentencing_date, previous_criminal_history, last_known_address, 
                district, state, additional_notes,image_dir, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Prepare the data tuple
            data = (
                full_name if full_name else "",
                date_of_birth if date_of_birth else None, 
                gender if gender else "",
                title if title else "",
                crime_description if crime_description else "",
                case_number if case_number else "",
                arrest_date if arrest_date else None, 
                court_name if court_name else "",
                sentencing_date if sentencing_date else None,
                previous_criminal_history if previous_criminal_history else "",
                last_known_address if last_known_address else "",
                district if district else "",
                state if state else "",
                additional_notes if additional_notes else "",
                image_folder_name if image_folder_name else "",
                img_name
            )

            # Execute the query and commit the changes to the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            print("SQL Query: ", query)
            print("Data being inserted: ", data)
            cursor.execute(query, data)
            mysql.connection.commit()

            # Close the cursor
            cursor.close()

            return redirect(url_for('dashboard', status=200, msg="Record successfully added!"))

        except Exception as e:
            # If an error occurred, display the message
            return redirect(url_for('dashboard', status=500, msg=f"An error occurred: {str(e)}"))


@app.route('/search', methods=['GET'])
def search_records():
    search_results = []
    search_term = request.args.get('search_term', '').strip()  # Get search term from query parameters
    errors = []

    try:
        # Start building the query
        query = "SELECT * FROM criminal_records WHERE 1"
        filters = []

        # Add filter for the search term (search in multiple fields)
        if search_term:
            query += """ AND (full_name LIKE %s OR case_number LIKE %s OR crime_description LIKE %s 
                        OR court_name LIKE %s OR district LIKE %s OR state LIKE %s)"""
            filters = ['%' + search_term + '%'] * 6  # Apply the search term for multiple fields

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, tuple(filters) if filters else ())
        search_results = cursor.fetchall()
        cursor.close()

    except Exception as e:
        errors.append(f"Error occurred: {str(e)}")

    return jsonify(search_results)  # Return the results as JSON

@app.route('/record/<int:record_id>', methods=['GET'])
def fetch_record(record_id):
    record = None
    try:
        # SQL query to fetch a specific record by its ID
        query = "SELECT * FROM criminal_records WHERE record_id = %s"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (record_id,))
        record = cursor.fetchone()
        cursor.close()

        if record:
            return jsonify(record)
        else:
            return jsonify({"error": "Record not found"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

def extract_face_embedding(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    face = image[y:y + h, x:x + w]
    return face


logging.basicConfig(level=logging.DEBUG)

@app.route('/search-img', methods=['POST'])
def search_image():
    try:
        logging.debug("Received request to /search-img")

        if 'image' not in request.files:
            logging.error("No image uploaded")
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            logging.error("No file selected")
            return jsonify({"error": "No file selected"}), 400

        upload_dir = 'uploads/temp'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, secure_filename(file.filename))
        file.save(file_path)
        logging.debug(f"File saved at: {file_path}")

        uploaded_image = cv2.imread(file_path)
        if uploaded_image is None:
            logging.error("Failed to read the uploaded image")
            return jsonify({"error": "Failed to read the uploaded image"}), 500

        gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            logging.error("No face detected in the uploaded image")
            return jsonify({"error": "No face detected in the uploaded image"}), 400

        logging.debug(f"Faces detected: {len(faces)}")

        all_dirs = os.listdir('static/uploads')
        for dirname in all_dirs:
            dir_path = os.path.join('static/uploads', dirname)
            if os.path.isdir(dir_path):
                logging.debug(f"Checking directory: {dir_path}")
                
                for filename in os.listdir(dir_path):
                    if filename.endswith(('.jpg', '.jpeg', '.png')):
                        image_path = os.path.join(dir_path, filename)
                        db_image = cv2.imread(image_path)

                        if db_image is None:
                            logging.warning(f"Failed to read image: {image_path}")
                            continue

                        db_gray = cv2.cvtColor(db_image, cv2.COLOR_BGR2GRAY)
                        db_faces = face_cascade.detectMultiScale(db_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                        if len(db_faces) > 0:
                            logging.debug(f"Face found in image: {image_path}")

                            (dx, dy, dw, dh) = db_faces[0]
                            db_face_region = db_image[dy:dy+dh, dx:dx+dw]

                            result = cv2.matchTemplate(uploaded_image, db_face_region, cv2.TM_CCOEFF_NORMED)
                            threshold = 0.8
                            if np.max(result) >= threshold:
                                logging.debug(f"Match found in directory {dirname}")
                                
                                # Corrected cursor creation
                                cursor = mysql.connection.cursor(DictCursor)  # Use DictCursor here
                                cursor.execute("SELECT * FROM criminal_records WHERE image_dir = %s", (dirname,))
                                record = cursor.fetchone()
                                cursor.close()

                                if record:
                                    logging.debug(f"Record found: {record}")
                                    return jsonify(record), 200

        logging.error("No matching face found in any directory")
        return jsonify({"error": "No matching face found"}), 404

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route("/dashboard")
def dashboard():
    if "loggedin" in session:
        return render_template("dashboard.html", email=session["email"])
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/check_db")
def check_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        return f"Connected to database: {db_name}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
