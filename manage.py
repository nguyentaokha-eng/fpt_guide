#Q1
class StudentEnrollment:
    def __init__(self, student_id, student_name, program, department, start_year):
        self.student_id = str(student_id)
        self.student_name = str(student_name)
        self.program = str(program)
        self.department = str(department)
        self.__start_year = int(start_year)
    def get_start_year(self):
        print (f'Start year: {self.__start_year}')
    def set_start_year(self, year):
        if year > 0:
            self.__start_year = year
            return self.__start_year
        else:
            print('invalid year')
    def __str__(self):
        return f'Student ID: {self.student_id}, Student Name: {self.student_name}, Program: {self.program}, Department: {self.department}, Start Year: {self.__start_year}'     
        
student = StudentEnrollment('DE201022', 'A', 'Eng', 'P213', 2024)
student.set_start_year(2025)
print(student.set_start_year(2025))
print(student)

#Q2
filename = 'student_enrollment_data.txt'
def load_enrollment_data(filename):
    with open(filename) as file:
        lst = []
        next(file)
        for line in file:
            info = line.strip().split(' ')
            student_id = info[0]
            student_name = info[1]
            program = info[2]
            department = info[3]
            start_year = int(info[4])
            obj = StudentEnrollment(student_id, student_name, program, department, start_year)
            lst.append(obj)
    return lst
enrollment_data = load_enrollment_data(filename)
print(enrollment_data)