Project Overview:
This project is a powerful criminal identification system built using Flask, a lightweight web framework. It processes CCTV footage and other visual data, utilizing advanced machine learning algorithms to analyze and match faces, recognize suspicious activity, and search for known criminals.

The application allows users to upload or stream footage. It then extracts relevant images for analysis. By comparing facial features against a database of known criminals, it helps law enforcement or security teams quickly identify suspects. It also has filters and search functionalities to enable efficient tracking of potential criminals.

This Flask-based interface is designed to be user-friendly, providing easy access to all features, including real-time searches and image uploads. The system supports multiple image formats and offers integration with security systems for continuous monitoring. Ultimately, this project aims to improve public safety by automating the criminal identification process.

Key Features:
- User Authentication: Login and secure access for authorized users (security personnel, law enforcement).
- Real-time Face Detection: Detects and matches faces from CCTV footage.
- Database Integration: Stores criminal records and uploaded images in a MySQL database.
- Image Search: Search for records based on full name, case number, crime description, and more.
- Real-Time Image Upload: Allows the user to upload or stream images for criminal identification.
- Face Recognition: Matches uploaded images with known criminal records.
- Multiple Image Formats: Supports various image file types (PNG, JPG, JPEG, GIF).
- User Dashboard: A comprehensive dashboard for adding, managing, and searching criminal records.

Technology Stack:
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: MySQL
- Libraries:
    - OpenCV for face detection and image processing.
    - Werkzeug for file handling (secure file upload).
    - bcrypt for password hashing.
- Machine Learning: Used for face recognition and matching.

Setup & Installation:

1. Clone the Repository:
    git clone https://github.com/Aravind-Hari001/hackathon2k25.git

2. Install Dependencies:
    Make sure you have Python 3 installed. Install the necessary libraries:
    pip install -r requirements.txt

    The requirements.txt file should contain the following:
    Flask==2.0.2
    Flask-MySQLdb==1.0.1
    opencv-python==4.5.3.56
    numpy==1.19.5
    werkzeug==2.0.1
    bcrypt==3.2.0

3. Configure the Database:
    Ensure you have MySQL installed and set up. You will need a database named criminal_database. You can create it using:
    CREATE DATABASE criminal_database;

    Make sure the table criminal_records is created to store the necessary criminal data. The schema for the table should include fields like:
    - record_id
    - full_name
    - date_of_birth
    - gender
    - crime_description
    - case_number
    - arrest_date
    - court_name
    - sentencing_date
    - previous_criminal_history
    - last_known_address
    - district
    - state
    - additional_notes
    - image_dir
    - image

    Also, create a users table to store authorized user credentials.

4. Update Configuration:
    In the Flask app, update the MySQL connection parameters in the app.config:
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "your_username"
    app.config["MYSQL_PASSWORD"] = "your_password"
    app.config["MYSQL_DB"] = "criminal_database"

5. Run the Application:
    Once everything is set up, you can run the Flask application using:
    python app.py

    The app will be running on http://127.0.0.1:5000/ by default.

Usage:
1. Login:
    Navigate to / to log in using authorized credentials.
    After logging in, you’ll be directed to the dashboard.

2. Dashboard:
    You can add criminal data, including images, through the "Add Data" section.
    Use the "Search" section to search through the criminal database by various filters.
    View detailed records by clicking on individual entries.

3. Upload Images for Search:
    Upload a face image in the Search Image section.
    The system will try to match the uploaded face against stored images in the database, returning any matches if found.

4. View Criminal Records:
    Search for criminal records and view details such as full name, crime description, and arrest details.

5. Logout:
    Use the "Logout" option to log out of the application.

Error Handling and Debugging:
    The app is configured with detailed logging for debugging purposes.
    If errors occur (e.g., image upload failure, database connection issues), error messages are logged, and the user receives feedback on the front-end.

Conclusion:
    This system can be used to improve public safety by automating criminal identification through image processing and machine learning. By using Flask, OpenCV, and MySQL, the project aims to enhance law enforcement’s ability to quickly identify suspects from CCTV footage and other visual data.
