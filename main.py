
import sys
import json
from typing import List
from munkres import Munkres

input_file_name = 'input'
output_file_name = 'output'

class Student:
    count_of_students: int = 0

    def __init__(self, name: str, choice: int, unavailable_places: str):
        self.name: str = name
        self.choice: int = choice
        self.computed_choice: int = 0
        self.unavailable_places: List[bool] = self.__calc_unavailable(
            unavailable_places)

    def __calc_unavailable(self, unavailable_places: str) -> List[bool]:
        result = [False] * Student.count_of_students
        unavailable_places.replace(' ', '')
        if unavailable_places == '':
            return result
        ranges = unavailable_places.split(',')
        for r in ranges:
            if '-' in r:
                start, end = map(int, r.split('-'))
                for i in range(start, end + 1):
                    result[i-1] = True
            else:
                result[int(r)-1] = True
        return result

    def to_dict(self):
        return {
            "name": self.name,
            "computed_choice": self.computed_choice
        }

    @staticmethod
    def from_dict(data):
        return Student(name=data["name"], choice=data["choice"],
                       unavailable_places=data["unavailable_places"])

    @staticmethod
    def students_to_json(students):
        dict_list = [student.to_dict() for student in students]
        return json.dumps(dict_list, indent=4)

    @staticmethod
    def students_from_json(json_str):
        dict_list = json.loads(json_str)
        return [Student.from_dict(data) for data in dict_list]


def init_json():
    with open(input_file_name + '.json', 'w') as file:
        file.write(json.dumps([{"name": f"{i+1}", "choice": 0, "unavailable_places": ""}
                   for i in range(Student.count_of_students)], indent=4))

def upload_students() -> List[Student]:
    with open(input_file_name + '.json', 'r') as file:
        Student.count_of_students = len(json.load(file))
    with open(input_file_name + '.json', 'r') as file:
        data = file.read()
    students = Student.students_from_json(data)
    return students

def save_students(students : List[Student], style : int = 0):
    match style:
        case 0:
             with open(output_file_name + '.txt', 'w') as file:
                for i in range(len(students)):
                    file.write(f"{i+1}. {students[i].name}\n")
        case 1:
            with open(output_file_name + '.json', 'w') as file:
                file.write(Student.students_to_json(students))

def solve(students : List[Student]) -> List[Student]:
    m = Munkres()
    size = len(students)
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[-1].append(abs(students[i].choice-j-1) +
                              1000000 * students[i].unavailable_places[j])
    result = m.compute(matrix)
    for i in range(Student.count_of_students):
        students[i].computed_choice = result[i][1] + 1
    students = list(sorted(students, key=lambda x: x.computed_choice))
    return students


def main():
    match sys.argv[1]:
        case 'create':
            if len(sys.argv) == 3:
                Student.count_of_students = int(sys.argv[2])
                init_json()
                print(
                    f"'{input_file_name}.json' done. Now you need to fill the file with data and Use '{sys.argv[0]} calc'.")
            else:
                print(f"invalid input. See '{sys.argv[0]} help'.")
        case 'calc':
            save_students(solve(upload_students()), style=0)
            print(f"result done and written to '{output_file_name}.txt'.")
        case 'help':
            print(f"1. Use '{sys.argv[0]} create n' to create input file for n students.\n2. Fill the '{input_file_name}.json' file with data.\n3. Use '{sys.argv[0]} calc' to get the result in the '{output_file_name}.txt' file.")
        case _:
            print(f"{sys.argv[1]} is not a command. See '{sys.argv[0]} help'.")


if __name__ == '__main__':
    main()
