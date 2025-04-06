import os
import csv

class FileData:
    def __init__(self, search_file_name, filename, folder_location):
        self.search_file_name = search_file_name
        self.filename = filename
        self.folder_location = folder_location

def quick_sort(files):
    if len(files) <= 1:
        return files
    else:
        pivot = files[len(files) // 2]
        left = [x for x in files if x.search_file_name < pivot.search_file_name]
        middle = [x for x in files if x.search_file_name == pivot.search_file_name]
        right = [x for x in files if x.search_file_name > pivot.search_file_name]
        return quick_sort(left) + middle + quick_sort(right)

def main():
    with open('list.idx', 'r') as f:
        folders = [line.strip() for line in f.readlines()]
        
    file_list = []
    rev_file_list = []

    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                file_data = FileData(filename, filename, root)
                file_list.append(file_data)
                rev_file_data = FileData(filename[::-1], filename, root)
                rev_file_list.append(rev_file_data)

    sorted_files = quick_sort(file_list)
    rev_sorted_files = quick_sort(rev_file_list)

    with open('sorted_files.csv', 'w', newline='') as csvfile:
        fieldnames = ['Search', 'Filename', 'Folder Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for file in sorted_files:
            writer.writerow({'Search': file.search_file_name, 'Filename': file.filename, 'Folder Location': file.folder_location})

    with open('rev_sorted_files.csv', 'w', newline='') as csvfile:
        fieldnames = ['Search', 'Filename', 'Folder Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for file in rev_sorted_files:
            writer.writerow({'Search': file.search_file_name, 'Filename': file.filename, 'Folder Location': file.folder_location})

if __name__ == "__main__":
    main()