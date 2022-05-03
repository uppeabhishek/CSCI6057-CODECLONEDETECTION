class MaximalRepeats:
    def __init__(self, current_string, suffixes, prefixes, min_length):
        self.string = current_string
        self.suffixes = suffixes
        self.prefixes = prefixes
        self.min_length = min_length

    def compute(self):
        if not len(self.prefixes):
            return None

        previous_prefix_length, current_index, prefixes_length, results = 0, 0, len(self.prefixes) - 1, {}
        stack = {'top': 0, 'max_val': []}

        current_suffix_position = self.suffixes[0]

        for i in range(prefixes_length):
            current_prefix_length = self.prefixes[i]
            next_suffix_position = self.suffixes[i + 1]
            end_suffix_position = max(current_suffix_position, next_suffix_position) + current_prefix_length
            diff_length = previous_prefix_length - current_prefix_length
            if diff_length < 0:
                stack['max_val'].append([-diff_length, i, end_suffix_position])
                stack['top'] += -diff_length
            elif diff_length > 0:
                self.removeStackItems(stack, results, diff_length, i)
            elif stack['top'] > 0 and end_suffix_position > stack['max_val'][-1][-1]:
                stack['max_val'][-1][-1] = end_suffix_position

            previous_prefix_length = current_prefix_length
            current_suffix_position = next_suffix_position

        if stack['top'] > 0:
            self.removeStackItems(stack, results, stack['top'], i + 1)

        result = []

        for (offset_end, count), (length, _) in results.items():
            result.append((offset_end - length, offset_end))
            ss = self.string[offset_end - length:offset_end]
            # stdout.write(ss + " " + str(offset_end - length) + " " + str(offset_end) + " " + str(
            #     offset_end - (offset_end - length)) + "\n")
            # stdout.flush()

        return result

    def removeStackItems(self, stack, results, length, index):
        prev_start = -1
        while length > 0:
            diff_length, current_start, max_end = stack['max_val'].pop()
            if prev_start != current_start:
                key = (max_end, index - current_start + 1)
                if key not in results or results[key][0] < stack['top']:
                    if max_end - (max_end - stack['top']) >= self.min_length:
                        results[key] = (stack['top'], current_start)
                prev_start = current_start
            length -= diff_length
            stack['top'] -= diff_length
        if length < 0:
            stack['max_val'].append([-length, current_start, max_end - diff_length - length])
            stack['top'] -= length
