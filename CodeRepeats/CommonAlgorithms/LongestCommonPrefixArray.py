class LongestCommonPrefix:

    def __init__(self, string, suffix_array):
        self.string = string
        self.suffix_array = suffix_array

    def construct(self):
        suffix_array_length = len(self.suffix_array)

        longest_common_prefix_array = [0] * suffix_array_length

        inverse_suffix = [0] * suffix_array_length

        for i in range(suffix_array_length):
            # inverse_suffix[suffix_array[i] - 1] = i
            inverse_suffix[self.suffix_array[i]] = i

        prev_lcp_length = 0

        for i in range(suffix_array_length):
            if inverse_suffix[i] == suffix_array_length - 1:
                prev_lcp_length = 0
                continue

            # next_substring = suffix_array[inverse_suffix[i] + 1] - 1
            next_substring = self.suffix_array[inverse_suffix[i] + 1]

            while (i + prev_lcp_length < suffix_array_length) and (
                    next_substring + prev_lcp_length < suffix_array_length) \
                    and (self.string[i + prev_lcp_length] == self.string[next_substring + prev_lcp_length]):
                prev_lcp_length += 1

            inverse_suffix_val = inverse_suffix[i] + 1
            longest_common_prefix_array[inverse_suffix_val - 1] = prev_lcp_length

            if prev_lcp_length > 0:
                prev_lcp_length -= 1

        return longest_common_prefix_array
