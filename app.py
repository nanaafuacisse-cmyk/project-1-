from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import bcrypt
from datetime import datetime


app = Flask(__name__)

# Secret key for login sessions
app.secret_key = "cliniccare-secret-key"

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user_id = request.form["user_id"].strip()
        password = request.form["password"]
        role = request.form["role"]

        users = load_users()

        # Check if user ID already exists
        for user in users:
            if user["user_id"] == user_id:
                return "User ID already exists. Please choose another ID."

        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        new_user = {
            "user_id": user_id,
            "password": password_hash,
            "role": role
        }

        users.append(new_user)
        save_users(users)

        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():

    user_id = request.form["user_id"].strip()
    password = request.form["password"]

    users = load_users()

    for user in users:

        if user["user_id"] == user_id:

            # Check password against bcrypt hash
            if bcrypt.checkpw(
                password.encode("utf-8"),
                user["password"].encode("utf-8")
            ):

                session["user_id"] = user["user_id"]
                session["role"] = user["role"]

                if user["role"] == "patient":
                    return redirect(url_for("patient_dashboard"))

                elif user["role"] == "clinician":
                    return redirect(url_for("clinician_dashboard"))

            return "Incorrect password."

    return "User ID not found."


@app.route("/patient/dashboard")
def patient_dashboard():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "patient":
        return "Access denied."

    return render_template(
        "patient_dashboard.html",
        user_id=session["user_id"]
    )


@app.route("/clinician/dashboard")
def clinician_dashboard():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    return render_template(
        "clinician_dashboard.html",
        user_id=session["user_id"]
    )


@app.route("/clinician/tasks/create", methods=["GET", "POST"])
def create_task():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    if request.method == "POST":

        task_title = request.form["task_title"].strip()
        description = request.form["description"].strip()
        patient_id = request.form["patient_id"].strip()

        # Load existing tasks
        if os.path.exists("health_tasks.json"):
            with open("health_tasks.json", "r") as file:
                tasks = json.load(file)
        else:
            tasks = []

        # Create a new task
        new_task = {
            "task_id": len(tasks) + 1,
            "title": task_title,
            "description": description,
            "patient_id": patient_id,
            "assigned_by": session["user_id"],
            "status": "assigned"
        }

        tasks.append(new_task)

        # Save the task
        with open("health_tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)

        return redirect(url_for("clinician_dashboard"))

    return render_template("create_task.html")


@app.route("/patient/tasks")
def patient_tasks():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "patient":
        return "Access denied."

    patient_id = session["user_id"]

    if os.path.exists("health_tasks.json"):
        with open("health_tasks.json", "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

    # Show only tasks assigned to the logged-in patient
    patient_tasks = [
        task for task in tasks
        if task["patient_id"] == patient_id
    ]

    # Load patient submissions
    if os.path.exists("task_submissions.json"):
        with open("task_submissions.json", "r") as file:
            submissions = json.load(file)
    else:
        submissions = []

    # Show only this patient's submissions
    patient_submissions = [
        submission for submission in submissions
        if submission["patient_id"] == patient_id
    ]

    return render_template(
        "patient_tasks.html",
        tasks=patient_tasks,
        submissions=patient_submissions
    )


@app.route("/patient/tasks/<int:task_id>/submit", methods=["GET", "POST"])
def submit_task(task_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "patient":
        return "Access denied."

    patient_id = session["user_id"]

    # Load health tasks
    if os.path.exists("health_tasks.json"):
        with open("health_tasks.json", "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

    # Find the task
    task = None

    for item in tasks:
        if item["task_id"] == task_id and item["patient_id"] == patient_id:
            task = item
            break

    if task is None:
        return "Task not found or access denied."

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            return "Please select a file."

        # Allowed file types
        allowed_extensions = {"txt", "csv", "pdf"}

        filename = uploaded_file.filename
        extension = filename.rsplit(".", 1)[-1].lower()

        if extension not in allowed_extensions:
            return "Invalid file type. Only TXT, CSV, and PDF files are allowed."

        # Create submissions folder if needed
        os.makedirs("submissions", exist_ok=True)

        # Create a unique filename using patient ID and task ID
        safe_filename = f"{patient_id}_{task_id}.{extension}"

        # Save inside the submissions folder
        filepath = os.path.join("submissions", safe_filename)
        uploaded_file.save(filepath)

        # Load existing submissions
        if os.path.exists("task_submissions.json"):
            with open("task_submissions.json", "r") as file:
                submissions = json.load(file)
        else:
            submissions = []

        # Create submission record
        new_submission = {
            "submission_id": len(submissions) + 1,
            "task_id": task_id,
            "patient_id": patient_id,
            "filename": filename,
            "filepath": filepath,
            "status": "submitted"
        }

        submissions.append(new_submission)

        # Save submission record
        with open("task_submissions.json", "w") as file:
            json.dump(submissions, file, indent=4)

        return "Task submitted successfully!"

    return render_template(
        "submit_task.html",
        task=task
    )


@app.route("/clinician/submissions")
def review_submissions():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    if os.path.exists("task_submissions.json"):
        with open("task_submissions.json", "r") as file:
            submissions = json.load(file)
    else:
        submissions = []

    return render_template(
        "review_submissions.html",
        submissions=submissions
    )


@app.route("/clinician/submissions/<int:submission_id>/review", methods=["POST"])
def submit_review(submission_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    if os.path.exists("task_submissions.json"):
        with open("task_submissions.json", "r") as file:
            submissions = json.load(file)
    else:
        submissions = []

    decision = request.form["decision"]
    feedback = request.form["feedback"].strip()

    for submission in submissions:

        if submission["submission_id"] == submission_id:

            submission["status"] = decision
            submission["feedback"] = feedback
            submission["reviewed_by"] = session["user_id"]
            submission["reviewed_at"] = datetime.now().isoformat()

    with open("task_submissions.json", "w") as file:
        json.dump(submissions, file, indent=4)

    return redirect(url_for("review_submissions"))


@app.route("/patient/messages", methods=["GET", "POST"])
def patient_messages():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "patient":
        return "Access denied."

    current_user = session["user_id"]

    if os.path.exists("messages.json"):
        with open("messages.json", "r") as file:
            messages = json.load(file)
    else:
        messages = []

    if request.method == "POST":

        recipient = request.form["recipient"].strip()
        message = request.form["message"].strip()

        new_message = {
            "message_id": len(messages) + 1,
            "sender": current_user,
            "recipient": recipient,
            "message": message
        }

        messages.append(new_message)

        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)

        return redirect(url_for("patient_messages"))

    user_messages = [
        msg for msg in messages
        if msg["sender"] == current_user
        or msg["recipient"] == current_user
    ]

    return render_template(
        "messages.html",
        messages=user_messages
    )


@app.route("/clinician/messages", methods=["GET", "POST"])
def clinician_messages():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    current_user = session["user_id"]

    if os.path.exists("messages.json"):
        with open("messages.json", "r") as file:
            messages = json.load(file)
    else:
        messages = []

    if request.method == "POST":

        recipient = request.form["recipient"].strip()
        message = request.form["message"].strip()

        new_message = {
            "message_id": len(messages) + 1,
            "sender": current_user,
            "recipient": recipient,
            "message": message
        }

        messages.append(new_message)

        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)

        return redirect(url_for("clinician_messages"))

    user_messages = [
        msg for msg in messages
        if msg["sender"] == current_user
        or msg["recipient"] == current_user
    ]

    return render_template(
        "clinician_messages.html",
        messages=user_messages
    )


@app.route("/announcements")
def announcements():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if os.path.exists("announcements.json"):
        with open("announcements.json", "r") as file:
            announcements_list = json.load(file)
    else:
        announcements_list = []

    return render_template(
        "announcements.html",
        announcements=announcements_list
    )


@app.route("/clinician/announcements/create", methods=["GET", "POST"])
def create_announcement():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    if os.path.exists("announcements.json"):
        with open("announcements.json", "r") as file:
            announcements = json.load(file)
    else:
        announcements = []

    if request.method == "POST":

        title = request.form["title"].strip()
        message = request.form["message"].strip()

        new_announcement = {
            "announcement_id": len(announcements) + 1,
            "title": title,
            "message": message,
            "posted_by": session["user_id"]
        }

        announcements.append(new_announcement)

        with open("announcements.json", "w") as file:
            json.dump(announcements, file, indent=4)

        return redirect(url_for("announcements"))

    return render_template("create_announcement.html")


@app.route("/clinician/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session.get("role") != "clinician":
        return "Access denied."

    # Load health tasks
    if os.path.exists("health_tasks.json"):
        with open("health_tasks.json", "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

    # Load submissions
    if os.path.exists("task_submissions.json"):
        with open("task_submissions.json", "r") as file:
            submissions = json.load(file)
    else:
        submissions = []

    # Load messages
    if os.path.exists("messages.json"):
        with open("messages.json", "r") as file:
            messages = json.load(file)
    else:
        messages = []

    total_tasks = len(tasks)
    total_submissions = len(submissions)

    pending = sum(
        1 for submission in submissions
        if submission["status"] in ["submitted", "Pending"]
    )

    reviewed_normal = sum(
        1 for submission in submissions
        if submission["status"] == "Reviewed — Normal"
    )

    needs_followup = sum(
        1 for submission in submissions
        if submission["status"] == "Needs Follow-up"
    )

    escalated = sum(
        1 for submission in submissions
        if submission["status"] == "Escalated"
    )

    total_messages = len(messages)

    return render_template(
        "analytics.html",
        total_tasks=total_tasks,
        total_submissions=total_submissions,
        pending=pending,
        reviewed_normal=reviewed_normal,
        needs_followup=needs_followup,
        escalated=escalated,
        total_messages=total_messages
    )


if __name__ == "__main__":
    app.run(debug=True)