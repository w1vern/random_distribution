import sys
import json
from typing import List
from munkres import Munkres


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
            "computedChoice": self.computed_choice
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
    with open('input.json', 'w') as file:
        file.write(json.dumps([{"name": f"{i+1}", "choice": 0, "unavailable_places": ""}
                   for i in range(Student.count_of_students)], indent=4))


def solve():
    m = Munkres()
    with open('input.json', 'r') as file:
        Student.count_of_students = len(json.load(file))
    with open('input.json', 'r') as file:
        data = file.read()
    arr: List[Student] = Student.students_from_json(data)
    size = len(arr)
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[-1].append(abs(arr[i].choice-j-1) +
                              1000000 * arr[i].unavailable_places[j])
    result = m.compute(matrix)
    for i in range(Student.count_of_students):
        arr[i].computed_choice = result[i][1] + 1
    with open('output.json', 'w') as file:
        file.write(Student.students_to_json(arr))


def main():
    match sys.argv[1]:
        case 'create':
            Student.count_of_students = int(sys.argv[2])
            init_json()
            print(
                f"'input.json' done. Now you need to fill the file with data and Use '{sys.argv[0]} calc'.")
        case 'calc':
            solve()
            print("result done and written to 'output.json'.")
        case 'help':
            print(f"1. Use '{sys.argv[0]} create n' to create input file for n students.\n2. Fill the 'input.json' file with data.\n3. Use '{sys.argv[0]} calc' to get the result in the 'output.json' file.")
        case _:
            print(f"{sys.argv[1]} is not a command. See '{sys.argv[0]} help'.")


if __name__ == '__main__':
    main()
