from collections import defaultdict

from CodeRepeats.BarenbaumAlgorithm.main import BarenbaumAlgorithm
from CodeRepeats.BellerAlgorithm.main import BellerAlgorithm
from CodeRepeats.CodeRepeat.Preprocessing import Preprocessing


class CodeRepeat:
    def __init__(self, directory):
        self.cache = {}
        self.directory = directory

    def __get_duplicated_count(self, value, current_list):
        cnt = 0
        for ele in current_list:
            if ele[0] >= value[0] and ele[1] <= value[1]:
                cnt += ele[1] - ele[0]
        if cnt > 0:
            return True, cnt
        return False, cnt

    def print_duplicated_files_and_length(self, data, file_mapping):
        result = defaultdict(int)

        for key, value in file_mapping.items():
            exists, diff = self.__get_duplicated_count(value, data)
            if exists:
                result[key] += diff

        print(result)

    def preprocessing(self):
        preprocessing = Preprocessing(self.directory)
        data, file_mappings = preprocessing.preprocess_data()
        return data, file_mappings

    def find_repeated_code_using_barenbaum_algorithm(self):
        data, file_mappings = self.preprocessing()
        barenbaumAlgorithm = BarenbaumAlgorithm(data, 10, self.cache)
        repeated_code, self.cache = barenbaumAlgorithm.find_repeated_code()
        self.print_duplicated_files_and_length(repeated_code, file_mappings)

    def find_repeated_code_using_beller_algorithm(self):
        data, file_mappings = self.preprocessing()
        bellerAlgorithm = BellerAlgorithm(data, 10, self.cache)
        self.print_duplicated_files_and_length(bellerAlgorithm.find_repeated_code(), file_mappings)


if __name__ == "__main__":
    c = CodeRepeat("../testing/test")
    c.find_repeated_code_using_barenbaum_algorithm()
    c.find_repeated_code_using_beller_algorithm()
