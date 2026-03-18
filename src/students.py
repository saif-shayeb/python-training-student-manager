import uuid
from email_validator import validate_email, EmailNotValidError
import json


class DuplicateEmailError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StudentNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


students_list = []


def add_student(stu_name, stu_email, stu_grades):
    grade = float(stu_grades)
    if grade > 100 or grade < 0:
        raise ValueError("Grades should be between 0 and 100")
    try:
        validate_email(stu_email, check_deliverability=False)
    except Exception:
        raise EmailNotValidError
    if not stu_name or stu_name.strip() == "":
        raise ValueError("Name cannot be empty")

    stu = {
        "ID": str(uuid.uuid4()),
        "name": stu_name,
        "email": stu_email,
        "grades": grade,
    }
    duplicate = [
        student for student in students_list if (student["email"] == stu["email"])
    ]
    if len(duplicate) != 0:
        raise DuplicateEmailError("duplicate email address")
    else:
        students_list.append(stu)


def update_grades(stu_email, new_grade):
    stu = [student for student in students_list if student["email"] == stu_email]
    if len(stu) != 1:
        raise StudentNotFoundError("no student found with provided email")
    students_list.remove(stu[0])
    updated_student = stu[0]
    updated_student["grades"] = new_grade
    students_list.append(updated_student)


def get_top_students(window):
    students_list.sort(key=lambda x: x["grades"], reverse=True)
    window = min(window, len(students_list))
    return students_list[:window]


def export_student_list():
    with open("students.json", "w+") as f:
        json.dump(students_list, f)
