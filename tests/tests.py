import students
import pytest
from email_validator import EmailNotValidError
import os
import json


def test_add_student_with_valid_info():
    students.add_student("Ahmad rami", "ahmad1@ex.com", 95.5)
    res = [
        student
        for student in students.students_list
        if student["email"] == "ahmad@ex.com"
    ]
    assert len(res) != 0


def test_add_student_with_invalid_email():
    with pytest.raises(EmailNotValidError):
        students.add_student("Ahmad rami", "ahmad@excom", 95.5)


def test_add_student_with_invalid_grade():
    with pytest.raises(ValueError):
        students.add_student("Ahmad rami", "ahmad@ex.com", 101)


def test_add_student_with_negative_grade():
    with pytest.raises(ValueError):
        students.add_student("Ahmad rami", "ahmad@ex.com", -1)


def test_add_student_with_empty_name():
    with pytest.raises(ValueError):
        students.add_student("", "ahmad@ex.com", 95.5)


def test_add_student_with_spaces_name():
    with pytest.raises(ValueError):
        students.add_student("   ", "ahmadd@ex.com", 95.5)


def test_add_student_with_duplicate_email():
    students.add_student("Ahmad rami", "ahmad@ex.com", 95.5)
    with pytest.raises(students.DuplicateEmailError):
        students.add_student("Ahmad rami", "ahmad@ex.com", 95.5)


def test_update_grades_success():
    students.add_student("Update Test", "update@ex.com", 80)
    students.update_grades("update@ex.com", 90)
    res = [s for s in students.students_list if s["email"] == "update@ex.com"]
    assert res[0]["grades"] == 90


def test_update_grades_student_not_found():
    with pytest.raises(students.StudentNotFoundError):
        students.update_grades("nonexistent@exam.com", 85)


def test_get_top_students():
    students.add_student("Top One", "top1@ex.com", 100)
    students.add_student("Top Two", "top2@ex.com", 98)
    top = students.get_top_students(2)
    assert len(top) == 2
    assert top[0]["grades"] >= top[1]["grades"]


def test_get_top_students_large_window():
    total_students = len(students.students_list)
    top = students.get_top_students(total_students + 10)
    assert len(top) == total_students


def test_export_student_list():
    if os.path.exists("students.json"):
        os.remove("students.json")
    students.export_student_list()
    assert os.path.exists("students.json")
    with open("students.json", "r") as f:
        data = json.load(f)
    assert len(data) == len(students.students_list)
