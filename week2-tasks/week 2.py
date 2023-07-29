import csv
import os
import argparse
import zipfile
import re

def grep(patterns, file_path, recursive=False, case_sensitive=True, line_numbers=False, count_matches=False):
    try:
        flags = 0
        if not case_sensitive:
            flags = re.IGNORECASE

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()

        matched_lines = []
        for line_number, line in enumerate(lines, start=1):
            if any(re.search(pattern, line, flags) for pattern in patterns):
                matched_lines.append((line_number, line.strip()))

        if line_numbers:
            for line_number, line in matched_lines:
                print(f"{file_path}:{line_number}:{line}")
        else:
            for line_number, _ in matched_lines:
                print(file_path)
                if count_matches == False:
                    return

        if count_matches:
            print(f"Total matches: {len(matched_lines)}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{file_path}'. It might be a binary file.")


def search_in_directory(patterns, directory, recursive, case_sensitive, line_numbers, count_matches):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            grep(patterns, file_path, recursive, case_sensitive, line_numbers, count_matches)


def get_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def print_col(file, action):
    datas = []
    for c in file:
        data = []
        for i in action:
            data.append(c[int(i)-1])
        datas.append(data)
    return datas


def sum_column(file, action):
    sum = []
    for i in range(len(file[0])+5):
        sum.append(0)
    for c in file:
        for s in action:
            sum[int(s)-1] += int(c[int(s)-1])
    return sum


def compress_file(input_file, output_file):
    with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file, os.path.basename(input_file))


def custom_sort_by_length(lines, reverse=False):
    return sorted(lines, key=lambda x: len(x), reverse=reverse)


def sort_lines(input_file, sort_type, reverse=False):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

            if sort_type == "alphabetical":
                lines.sort(reverse=reverse)
            elif sort_type == "numerical":
                lines.sort(key=lambda x: float(x), reverse=reverse)
            elif sort_type == "case_insensitive":
                lines.sort(key=lambda x: x.lower(), reverse=reverse)
            elif sort_type == "custom":
                 lines = custom_sort_by_length(lines, reverse=reverse)
              
            else:
                print("Invalid sort type. Available options: alphabetical, numerical, case_insensitive, custom")
                return

            for line in lines:
                print(line.strip())

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    
    except Exception as e:
        print("Something is not correct!")


parser = argparse.ArgumentParser(description="Text Based Utility")
subparsers = parser.add_subparsers(title="Operation", dest="operation")

add_parser = subparsers.add_parser("compress_file", help="compress Operation to perform")
add_parser.add_argument("input_file", type=str, help="The input file to compress.")
add_parser.add_argument("output_file", type=str, help="The output compressed file.")

add_parser = subparsers.add_parser("print_column", help="print Operation to perform")
add_parser.add_argument("arguments", nargs="*", type=int, help="arguments like 1 etc")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("sum_column", help="sum Operation to perform")
add_parser.add_argument("arguments", nargs="*", type=int, help="arguments like 1 etc")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("cut_text", help="cut Operation to perform")
add_parser.add_argument("arguments", nargs=2, type=int, help="2 integer arguments")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("replace_text", help="replace Operation to perform")
add_parser.add_argument("arguments", nargs=2, type=str, help="2 string argument")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("repsave_text", help="replace and save Operation to perform")
add_parser.add_argument("arguments", nargs=2, type=str, help="2 string argument")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("see_text", help="see text Operation to perform")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

add_parser = subparsers.add_parser("see_csv", help="see csv Operation to perform")
add_parser.add_argument("file",type=argparse.FileType("r"), help="file_name")

# python text_manu.py sort_text "cut.txt" alphabetical -r
# python text_manu.py sort_text "cut.txt" alphabetical
add_parser = subparsers.add_parser("sort_text", help="sort_text Operation to perform")
add_parser.add_argument("input_file", help="The input file to be sorted.")
add_parser.add_argument("sort_type", choices=["alphabetical", "numerical", "case_insensitive", "custom"], 
                    help="Type of sorting: alphabetical, numerical, case_insensitive, or custom")
add_parser.add_argument("-r", "--reverse", action="store_true", help="Reverse the sorting order.")

add_parser = subparsers.add_parser("greb_text", help="greb_text Operation to perform")
add_parser.add_argument("patterns", nargs='+', help="The pattern(s) to search for.")
add_parser.add_argument("files", nargs='+', help="The file(s) or directory to search in.")
add_parser.add_argument("--recursive", "-r", action="store_true", help="Perform a recursive search through directories.")
add_parser.add_argument("--ignore-case", "-i", action="store_true", help="Perform a case-insensitive search.")
add_parser.add_argument("--line-numbers", "-n", action="store_true", help="Display line numbers for matched patterns.")
add_parser.add_argument("--count", "-c", action="store_true", help="Count the number of matches.")

args = parser.parse_args()
try: 
    if args.operation == "print_column":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".csv" or get_file_extension(file) == ".txt":
            with open(file, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)
        result = print_col(data, args.arguments)
        for i in result:
            for j in i:
                print(j, end=" ")
            print()

    elif args.operation == "sum_column":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".csv" or get_file_extension(file) == ".txt":
            with open(file, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)
        result = sum_column(data, args.arguments)
        for i in result:
            if i != 0:
                print(i, end=" ")

    elif args.operation == "cut_text":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".txt":
            with open(file, 'r') as files:
                data = files.read()
        arg = args.arguments
        if arg[0] < arg[1]:
            print(data[arg[0]-1 : arg[1]])
        else:
            print("Warning : limits are wrong!")
    
    elif args.operation == "replace_text":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".txt":
            with open(file, 'r') as files:
                data = files.read()
        arg = args.arguments
        data = data.replace(arg[0], arg[1])
        print(data)
        

    elif args.operation == "repsave_text":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".txt":
            with open(file, 'r') as files:
                data = files.read()
        arg = args.arguments
        data = data.replace(arg[0], arg[1])
        with open(file, 'w') as files:
                files.write(data)
        print(data)

    elif args.operation == "see_text":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".txt":
            with open(file, 'r') as files:
                data = files.read()
        print(data)
    elif args.operation == "see_csv":
        data = []
        file = args.file
        file = str(file.name)
        if get_file_extension(file) == ".csv":
            with open(file, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)
        for i in data:
            print(i)

    elif args.operation == "compress_file":
        compress_file(args.input_file, args.output_file)
        
    elif args.operation == "sort_text":
        sort_lines(args.input_file, args.sort_type, args.reverse)

    elif args.operation == "greb_text":
        for file_path in args.files:
            if os.path.isfile(file_path):
                grep(args.patterns, file_path, args.recursive, not args.ignore_case, args.line_numbers, args.count)
            elif os.path.isdir(file_path):
                if args.recursive:
                    search_in_directory(args.patterns, file_path, True, not args.ignore_case, args.line_numbers, args.count)
                else:
                    print(f"Error: '{file_path}' is a directory. Use the --recursive option to search recursively.")
            else:
                print(f"Error: '{file_path}' is not a valid file or directory.")
    
    else:
        raise ValueError("Invalid operation")

except Exception as e:
    print("Error : Invalid Arguments" )