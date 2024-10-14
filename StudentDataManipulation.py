# Meerub Sultan
# 2021296

import csv
import datetime

# used classes to define each item in the files in the order that was given


class Student:

    def __init__(self, student_id, last_name, first_name, major, action):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.action = action


class GPA:

    def __init__(self, stud_id, gpa_1):
        self.stud_id = stud_id
        self.gpa = gpa_1


class Graduation:

    def __init__(self, s_id, grad_date):
        self.s_id = s_id
        self.grad_date = grad_date


# used functions to open and read each line in the file and appended the same information in the correct order to lists


def read_students(file_names):
    students = []
    with open(file_names, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            student_id, first_name, last_name, major, action = row
            students.append(Student(student_id, first_name, last_name, major, action))
    return students


def read_gpa(file_names):
    gpa_list = []
    with open(file_names, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stud_id, gpa_s = row
            gpa_list.append(GPA(stud_id, gpa_s))
    return gpa_list


def read_grad(file_names):
    grad_list = []
    with open(file_names, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            s_id, grad_date = row
            grad_list.append(Graduation(s_id, grad_date))
    return grad_list


# Input the file names so that they to run through the functions and store them into the following variables


students_data = read_students('StudentsMajorsList.csv')
gpa_data = read_gpa('GPAList.csv')
grad_data = read_grad('GraduationDatesList.csv')


def sort_id(students):
    return students.student_id


def sort_id_gpa(gpa_s):
    return gpa_s.stud_id


def sort_id_grad(grad_s):
    return grad_s.s_id


sorted_students_id = sorted(students_data, key=sort_id)
# print(sorted_students_id[0].student_id)
sorted_students_gpa = sorted(gpa_data, key=sort_id_gpa)
sorted_students_grad = sorted(grad_data, key=sort_id_grad)


majors = []
# used a for loop to append each major into the empty majors list if they were not already in the list and opened
# each file to write to with the specified file name
for student in sorted_students_id:
    if student.major not in majors:
        majors.append(student.major)


gpa_lists = []
# appended every students gpa so I could refer to them later once the query is entered
for student in sorted_students_gpa:
    gpa_lists.append(student.gpa)

# Used a while loop to check all criteria
while True:
    query = input("Enter a Major and GPA (or 'q' to quit): ").strip().lower()
    if query == 'q':  # After output for one query, query the user again. Allow ‘q’ to quit.
        break

    # assigned the current date
    today = datetime.date.today()
    current_date = today.strftime("%m-%d-%Y")

    # holds major/gpa found in the query
    majors_found = []
    gpa_found = []

    # sorted student by gpa
    def sort_by_gpa(gpa_s):
        return gpa_s.gpa


    Sorted_Students_GPA = sorted(gpa_data, key=sort_by_gpa, reverse=True)

    # checks if any of the majors in the list can be found in the query
    # and if it can it appends it to the list major_found
    for m in majors:
        if m.lower() in query:
            majors_found.append(m)

    # checks if any of the students gpa can be found in the query and if it is the gpa
    # is appended to the list gpa_found
    for g in gpa_lists:
        if g in query:
            gpa_found.append(g)

    # if more than one major or gpa is found in the query 'No such Student' is printed
    if len(majors_found) > 1 or len(gpa_found) > 1:
        print("No such Student")
    else:
        if majors_found:
            print("Found major:", majors_found[0])  # tells you which major was found
            if gpa_found:  # tells you which GPA is found
                print("Found GPA:", gpa_found[0])
                for gpa in Sorted_Students_GPA:  # matches students from the three files
                    for student in sorted_students_id:
                        if student.student_id == gpa.stud_id:
                            for grad in sorted_students_grad:
                                if student.student_id == grad.s_id:
                                    if (student.action != 'Y') and (grad.grad_date > current_date):  # if the student
                                        # has graduated or had disciplinary action they will not be considered
                                        # converts GPA and finds the difference so I can compare later
                                        student_gpa = float(gpa.gpa)
                                        all_gpa_diff = []
                                        gpa_difference = abs(student_gpa - float(gpa_found[0]))
                                        all_gpa_diff.append(gpa_difference)

                                        # checks if the difference is within .25 and prints the student information
                                        if gpa_difference <= 0.25:
                                            print("You may consider:", student.student_id, student.first_name,
                                                  student.last_name, gpa.gpa)
                                            #  checks if the difference is within .1 and prints the student information
                                            if gpa_difference <= 0.1:
                                                print('Your Student(s):', student.student_id, student.first_name,
                                                      student.last_name, gpa.gpa)

                                        else:  # if the student has the same major their information will be printed
                                            if student.major == majors_found[0]:
                                                print('Closest Student:', student.student_id, student.first_name,
                                                      student.last_name, gpa.gpa)
