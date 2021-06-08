import csv
class UserProfile:

    def __init__(self, age, text_font, color_blindness, user_id):
        self.age = age
        self.text_font = text_font
        self.color_blindness = color_blindness
        self.user_id = user_id

class  ReadWriteUserData:

    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        persons = []
        with open(self.file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    new_person = UserProfile(row[1], row[3], row[2], row[0])
                    persons.append(new_person)
                    line_count += 1
            # print(f'Processed {line_count} lines.')
            return persons


read_write = ReadWriteUserData('./users_profile')
read_write.read_file()