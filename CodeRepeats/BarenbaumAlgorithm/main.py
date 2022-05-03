import time

from CodeRepeats.BarenbaumAlgorithm.MaximalRepeats import MaximalRepeats
from CodeRepeats.CommonAlgorithms.FastSuffixArray import FastSuffixArray
from CodeRepeats.CommonAlgorithms.LongestCommonPrefixArray import LongestCommonPrefix


class BarenbaumAlgorithm:
    def __init__(self, string, minimum_length=10, cache=None):
        self.string = string
        self.minimum_length = minimum_length
        self.cache = cache

    def find_repeated_code(self):
        suffix_array = FastSuffixArray(self.string)
        start = time.time()
        suffix_array_result = suffix_array.construct()
        self.cache['suffix_array_result'] = suffix_array_result
        end = time.time()
        print("suffix" + " " + str(end - start))

        longest_common_prefix = LongestCommonPrefix(self.string, suffix_array_result)
        start = time.time()
        longest_common_prefix_result = longest_common_prefix.construct()
        self.cache['longest_common_prefix_result'] = longest_common_prefix_result
        end = time.time()
        print("prefix" + " " + str(end - start))

        start = time.time()
        maximal_repeats = MaximalRepeats(self.string, suffix_array_result, longest_common_prefix_result,
                                         self.minimum_length)
        end = time.time()
        result = maximal_repeats.compute()
        print("repeats" + " " + str(end - start))
        return result, self.cache
