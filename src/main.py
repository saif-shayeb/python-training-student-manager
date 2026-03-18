import sys
import os
from students import (
    add_student,
    update_grades,
    get_top_students,
    export_student_list,
    DuplicateEmailError,
    StudentNotFoundError,
)
from email_validator import EmailNotValidError


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def display_menu():
    print(f"\n{Colors.CYAN}{Colors.BOLD}--- Student Manager ---{Colors.ENDC}")
    print(f"{Colors.BLUE}1. Add a student{Colors.ENDC}")
    print(f"{Colors.BLUE}2. Update student grades{Colors.ENDC}")
    print(f"{Colors.BLUE}3. Get top students{Colors.ENDC}")
    print(f"{Colors.BLUE}4. Export student list{Colors.ENDC}")
    print(f"{Colors.WARNING}5. Exit{Colors.ENDC}")
    print(f"{Colors.CYAN}-----------------------{Colors.ENDC}")


def main():
    while True:
        display_menu()
        choice = input(f"{Colors.BOLD}Enter your choice (1-5): {Colors.ENDC}").strip()

        if choice == "1":
            name = input("Enter student's name: ").strip()
            email = input("Enter student's email: ").strip()
            grades_str = input("Enter student's grade: ").strip()
            try:
                add_student(name, email, grades_str)
                print(f"{Colors.GREEN} Student {name} added successfully!{Colors.ENDC}")
            except ValueError as e:
                print(f"{Colors.FAIL} Invalid input: {e}{Colors.ENDC}")
            except EmailNotValidError:
                print(f"{Colors.FAIL} Invalid email format.{Colors.ENDC}")
            except DuplicateEmailError as e:
                print(f"{Colors.FAIL} Error: {e}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL} An error occurred: {e}{Colors.ENDC}")

        elif choice == "2":
            email = input("Enter student's email to update: ").strip()
            try:
                new_grade = float(input("Enter new grade: "))
                update_grades(email, new_grade)
                print(
                    f"{Colors.GREEN} Grades for {email} updated successfully!{Colors.ENDC}"
                )
            except ValueError:
                print(
                    f"{Colors.FAIL} Invalid grade input. Please enter a valid number.{Colors.ENDC}"
                )
            except StudentNotFoundError as e:
                print(f"{Colors.FAIL} Error: {e}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL} An error occurred: {e}{Colors.ENDC}")

        elif choice == "3":
            try:
                window = int(input("How many top students do you want to see? "))
                top_students = get_top_students(window)
                if not top_students:
                    print(f"{Colors.WARNING}No students found.{Colors.ENDC}")
                else:
                    print(
                        f"\n{Colors.HEADER}{Colors.BOLD} --- Top Students --- {Colors.ENDC}"
                    )
                    for i, stu in enumerate(top_students, 1):
                        print(
                            f"{Colors.CYAN}{i}. {stu['name']} ({stu['email']}) - Grade: {stu['grades']}{Colors.ENDC}"
                        )
            except ValueError:
                print(
                    f"{Colors.FAIL} Invalid input. Please enter a whole number.{Colors.ENDC}"
                )

        elif choice == "4":
            try:
                export_student_list()
                print(
                    f"{Colors.GREEN} Student list exported to students.json successfully!{Colors.ENDC}"
                )
            except Exception as e:
                print(
                    f"{Colors.FAIL} An error occurred while exporting: {e}{Colors.ENDC}"
                )

        elif choice == "5":
            print(f"{Colors.WARNING}Exiting Student Manager. Goodbye!{Colors.ENDC}")
            sys.exit(0)

        else:
            print(
                f"{Colors.FAIL} Invalid choice. Please enter a number between 1 and 5.{Colors.ENDC}"
            )


if __name__ == "__main__":
    main()
