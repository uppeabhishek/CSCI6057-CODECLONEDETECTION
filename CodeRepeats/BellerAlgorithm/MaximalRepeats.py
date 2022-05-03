from CodeRepeats.BellerAlgorithm.BullerWheelerTransform import BullerWheelerTransform


class MaximalRepeats:
    def __init__(self, string, suffix_array, prefix_array, minimum_length):
        self.string = string
        self.suffix_array = suffix_array
        self.prefix_array = prefix_array
        self.minimum_length = minimum_length

    def get_same_prefix_sum_array(self, bwt):
        array = [1] * len(bwt)
        for i in range(1, len(bwt)):
            if bwt[i] == bwt[i - 1]:
                array[i] = array[i - 1]
            else:
                array[i] = array[i - 1] + 1
        return array

    # BFS over the suffix array (just to replicate suffix tree and get the suffix tree intervals instead of
    # constructing suffix tree)
    def compute(self):

        bullerWheelerTransform = BullerWheelerTransform(self.string, self.suffix_array)
        prefix_sum = self.get_same_prefix_sum_array(bullerWheelerTransform.construct())

        results = []

        stack = []
        stack.append((0, 0, None))
        for i in range(0, len(self.prefix_array)):
            lb = i
            while self.prefix_array[i] < stack[-1][0]:
                stack[-1] = (stack[-1][0], stack[-1][1], i)
                temp = stack.pop()
                le, start, end = temp
                start_index = self.suffix_array[start]
                if prefix_sum[end] - prefix_sum[start] > 0 and le >= self.minimum_length:
                    results.append((start_index, start_index + le))
                    # stdout.write(self.string[start_index:start_index + le] + " " + str(start_index) + " " + str(
                    #     start_index + le) + " " + str(le) + "\n")
                    # stdout.flush()
                lb = temp[1]
            if self.prefix_array[i] > stack[-1][0]:
                stack.append((self.prefix_array[i], lb, None))

        return results
