import time

from CodeRepeats.BellerAlgorithm.MaximalRepeats import MaximalRepeats
from CodeRepeats.CommonAlgorithms.FastSuffixArray import FastSuffixArray
from CodeRepeats.CommonAlgorithms.LongestCommonPrefixArray import LongestCommonPrefix


class BellerAlgorithm:
    def __init__(self, string, minimum_length=10, cache=None):
        self.string = string
        self.minimum_length = minimum_length
        self.cache = cache

    def find_repeated_code(self):
        suffix_array = FastSuffixArray(self.string)
        start = time.time()
        if 'suffix_array_result' in self.cache:
            suffix_array_result = self.cache['suffix_array_result']
        else:
            suffix_array_result = suffix_array.construct()
        end = time.time()
        print("suffix" + " " + str(end - start))

        longest_common_prefix = LongestCommonPrefix(self.string, suffix_array_result)
        start = time.time()
        if 'longest_common_prefix_result' in self.cache:
            longest_common_prefix_result = self.cache['longest_common_prefix_result']
        else:
            longest_common_prefix_result = longest_common_prefix.construct()
        end = time.time()
        print("prefix" + " " + str(end - start))

        start = time.time()
        maximal_repeats = MaximalRepeats(self.string, suffix_array_result, longest_common_prefix_result,
                                         self.minimum_length)
        end = time.time()
        result = maximal_repeats.compute()
        print("repeats" + " " + str(end - start))
        return result
