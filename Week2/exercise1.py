import argparse
parser = argparse.ArgumentParser(description='A program to read from an input file, and either write it out in the console, or to an output file')

def print_file_content(file):
    with open(file,'r') as file_object:
        fileText = file_object.read()
        print(fileText)

def write_list_to_file(output_file, lst):
    with open(output_file, 'w') as file_object:
        file_object.write(lst)
        
def read_file(input_file):
    with open(input_file,'r') as file_object:
        return file_object.read()

if __name__ == '__main__':
    parser.add_argument('inputFile', help='Name of input file. Must be in the same directory as this file.')
    parser.add_argument('--file', '-file_name', help='Name of output file.')
    args = parser.parse_args()

    if args.file:
        outputFile = args.file
        lst = read_file(args.inputFile)
        write_list_to_file(outputFile,lst)
        
    else:
        print_file_content(args.inputFile)