import glob
import os
import re


class Preprocessing:
    def __init__(self, directory):
        self.current_file = []
        self.directory = directory
        self.data = []
        self.old_regex = re.compile(r"\s+")
        self.new_regex = " "
        self.file_mappings = {}

    def replace_with_regex(self, file):
        with open(file) as lines:
            for line in lines:
                self.current_file.append(line)
        return self.old_regex.sub(self.new_regex, " ".join(self.current_file)).strip()

    def preprocess_data(self):
        prev_length = 0
        for path in glob.iglob(self.directory + '**/**', recursive=True):
            if os.path.isfile(path):
                new_data = self.replace_with_regex(path)
                self.file_mappings[path] = (prev_length, prev_length + len(new_data) - 1)
                prev_length = prev_length + len(new_data) - 1
                self.data.append(new_data)

        return " ".join(self.data), self.file_mappings
