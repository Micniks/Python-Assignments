import os

def first_function(path, output_file):
    lst = os.listdir(path)
    with open(output_file, 'w') as file_object:
        for line in lst:
            file_object.write(line + "\n")
    
def second_function(path, output_file):
    lst = []
    for root, directories, files in os.walk(path, topdown=False):
            for name in files:
                lst.append(os.path.join(root, name)[len(path):])
            for name in directories:
                lst.append(os.path.join(root, name)[len(path):])
    with open(output_file, 'w') as file_object:
        for line in lst:
            file_object.write(line + "\n")
    
def third_function(lst):
    for file in lst:
        with open(file,'r') as file_object:
            print("First line in: " + file + "\n" + file_object.readlines()[0])
    
def fourth_function(lst):
    for file in lst:
        with open(file,'r') as file_object:
            for line in file_object.readlines():
                if "@" in line:
                    print("File: " + file + "\n" + line)
    
def fifth_function(lst, output_file):
    lines_to_output = []
    for file in lst:
        with open(file,'r') as file_object:
            for line in file_object.readlines():
                if line[0] == "#":
                    lines_to_output.append(line);
        with open(output_file, 'w') as file_object:
            for line in lines_to_output:
                file_object.write(line)