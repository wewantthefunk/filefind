import csv
import sys

class FileData:
    def __init__(self, search_filename, filename, folder_location):
        self.search_file_name = search_filename
        self.filename = filename
        self.folder_location = folder_location

def binary_search(files, target):
    low = 0
    high = len(files) - 1

    while low <= high:
        mid = (low + high) // 2
        if files[mid].filename == target:
            return [files[mid]]
        elif files[mid].filename < target:
            low = mid + 1
        else:
            high = mid - 1
    return [None]

def binary_search_startswith(files, target):
    low = 0
    high = len(files) - 1
    found_files = []

    while low <= high:
        mid = (low + high) // 2
        if files[mid].search_file_name[0:len(target)] == target:
            found_one = True
            mid = mid - 1

            while found_one and mid > 0:
                if files[mid].search_file_name[0:len(target)] == target:
                    mid = mid - 1
                else:
                    found_one = False

            found_one = True
            mid = mid + 1

            while found_one and mid < len(files):
                if files[mid].search_file_name[0:len(target)] == target:
                    found_files.append(files[mid])
                    mid = mid + 1
                else:
                    found_one = False
            break

        elif files[mid].search_file_name[0:len(target)] < target:
            low = mid + 1
        else:
            high = mid - 1

    if len(found_files) == 0:
        found_files.append(None)

    return found_files

def search_contains(files, target):
    found_files = [file_data for file_data in files if target in file_data.search_file_name]
    
    if len(found_files) == 0:
        found_files.append(None)

    return found_files

def main():
    file_list = []
    rev_file_list = []

    with open('sorted_files.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_data = FileData(row['Search'],row['Filename'], row['Folder Location'])
            file_list.append(file_data)

    with open('rev_sorted_files.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_data = FileData(row['Search'],row['Filename'], row['Folder Location'])
            rev_file_list.append(file_data)

    if len(sys.argv) < 2:
        print("Please provide a filename as a command-line argument.")
        return

    target_filename = sys.argv[1]
    if target_filename.startswith("*") and target_filename.endswith("*"):
        target_filename = target_filename[1:len(target_filename) - 1]
        found_file = search_contains(file_list, target_filename)
    elif target_filename.endswith("*"):
        target_filename = target_filename[0:len(target_filename) - 1]
        found_file = binary_search_startswith(file_list, target_filename)
    elif target_filename.startswith("*"):
        target_filename = target_filename[1:][::-1]
        found_file = binary_search_startswith(rev_file_list, target_filename)
    else:
        found_file = binary_search(file_list, target_filename)

    for f in found_file:
        if f is not None:
            print(f"{f.folder_location}/{f.filename}")
        else:
            print("File not found.")

    print()
    if len(found_file) == 1 and found_file[0] is None:
        print("0 files found.")
    else:
        print(f"{len(found_file)} files found.")

if __name__ == "__main__":
    main()