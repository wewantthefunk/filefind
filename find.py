import csv
import sys

class FileData:
    def __init__(self, search_filename, filename, folder_location):
        self.search_file_name = search_filename
        self.filename = filename
        self.folder_location = folder_location

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

    target_filename = str(sys.argv[1]).lower()
    found_file = []
    if target_filename == "--info":
        print(f"\n{len(file_list)} total indexed files\n\nFolders Indexed:")
        with open('list.idx', 'r', newline='') as idxfile:
            lines = idxfile.readlines()
            for line in lines:
                print(line.replace("\n", ""))

        exit(0)
    
    print("Searching ...")
    if target_filename.startswith("*") and target_filename.endswith("*"):
        target_filename = target_filename[1:len(target_filename) - 1]
        found_file = search_contains(file_list, target_filename)
    elif target_filename.endswith("*"):
        target_filename = target_filename[0:len(target_filename) - 1]
        found_file = binary_search_startswith(file_list, target_filename)
    elif target_filename.startswith("*"):
        target_filename = target_filename[1:]
        rev_target_filename = target_filename[1:][::-1]
        found_file = binary_search_startswith(rev_file_list, rev_target_filename)        
    else:
        found_file = binary_search_startswith(file_list, target_filename)

    for f in found_file:
        if f is not None:
            print(f"{f.folder_location.replace("\\", "/")}/", end='')
            starts = get_occurrences(f.filename.lower(), target_filename)
            start = 0
            for index in starts:
                print(f.filename[start: index].replace("\\", "/"), end="")
                print("\033[91m" + f.filename[index:index+len(target_filename)].replace("\\", "/") + "\033[00m", end='')
                start = start + index + len(target_filename)

            print(f.filename[start:].replace("\\", "/"))
        else:
            print("File not found.")

    print()
    if len(found_file) == 1 and found_file[0] is None:
        print("0 files found.")
    else:
        print(f"{len(found_file)} files found.")

def get_occurrences(string, substring):
    positions = []
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            break
        positions.append(start)
        start += len(substring)

    return positions

if __name__ == "__main__":
    main()
