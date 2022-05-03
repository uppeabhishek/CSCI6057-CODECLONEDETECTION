class FastSuffixArray:

    def __init__(self, string):
        self.alphabet_size = 256
        self.string = string

    def get_bucket_size(self, text, alphabet_size):
        arr = [0] * alphabet_size
        try:
            for c in text:
                arr[c] += 1
        except Exception as e:
            print(e)
        return arr

    def get_suffix_types(self, data):
        array = [False] * (len(data) + 1)
        array[len(data)] = True
        if len(data) == 0:
            return array
        array[len(data) - 1] = False
        for i in range(len(data) - 2, -1, -1):
            if data[i] < data[i + 1]:
                array[i] = True
            elif data[i] > data[i + 1]:
                array[i] = False
            else:
                array[i] = array[i + 1]

        return array

    def get_bucket_heads(self, bucket_sizes):
        heads = [0] * len(bucket_sizes)
        offset = 1
        for i in range(len(bucket_sizes)):
            heads[i] = offset
            offset += bucket_sizes[i]
        return heads

    def get_bucket_tails(self, bucket_sizes):
        tails = [0] * len(bucket_sizes)
        offset = 1
        for i in range(len(bucket_sizes)):
            offset += bucket_sizes[i]
            tails[i] = offset - 1
        return tails

    def is_lms_character(self, index, suffix_types):
        if index == 0:
            return False
        return suffix_types[index] == True and suffix_types[index - 1] == False

    def fix_lms_characters(self, data, suffix_array, suffix_types, bucket_sizes):
        suffix_array[0] = len(data)
        bucket_tails = self.get_bucket_tails(bucket_sizes)
        for i in range(len(data) - 1, -1, -1):
            if not self.is_lms_character(i, suffix_types):
                continue
            suffix_array[bucket_tails[data[i]]] = i
            bucket_tails[data[i]] -= 1

    def fix_lms_characters_summary(self, data, suffix_array, bucket_sizes, summary_suffix_array, summary_offsets):
        suffix_array[0] = len(data)
        bucket_tails = self.get_bucket_tails(bucket_sizes)
        for i in range(len(summary_suffix_array) - 1, 1, -1):
            try:
                c_i = summary_offsets[summary_suffix_array[i]]
                b_i = data[c_i]
                suffix_array[bucket_tails[b_i]] = c_i
                bucket_tails[b_i] -= 1
            except Exception as e:
                print(e)

    def induction_sort_l(self, data, suffix_array, suffix_types, bucket_sizes):
        buckets = self.get_bucket_heads(bucket_sizes)
        for i in range(len(suffix_array)):
            j = suffix_array[i] - 1
            if j < 0 or suffix_types[j] is not False:
                continue
            try:
                suffix_array[buckets[data[j]]] = j
                buckets[data[j]] += 1
            except Exception as e:
                print(e)

    def induction_sort_r(self, data, suffix_array, suffix_types, bucket_sizes):
        buckets = self.get_bucket_tails(bucket_sizes)
        for i in range(len(suffix_array) - 1, -1, -1):
            j = suffix_array[i] - 1
            if j < 0 or suffix_types[j] is not True:
                continue
            try:
                suffix_array[buckets[data[j]]] = j
                buckets[data[j]] -= 1
            except Exception as e:
                print(e)

    def is_lms_blocks_equal(self, data, prev_offset, cur_offset, suffix_types):
        if prev_offset == len(data) or cur_offset == len(data):
            return False
        if data[prev_offset] != data[cur_offset]:
            return False

        for i in range(1, len(data)):
            prev_lms, cur_lms = self.is_lms_character(prev_offset + i, suffix_types), self.is_lms_character(
                cur_offset + i, suffix_types)
            if prev_lms and cur_lms:
                return True
            if prev_lms != cur_lms:
                return False
            if data[prev_offset + i] != data[cur_offset + i]:
                return False

        return False

    def reduce_array(self, data, suffix_array, suffix_types):
        lms_names = [-1] * (len(data) + 1)
        cur_name, cnt = 0, 1
        lms_names[suffix_array[0]] = cur_name
        cur_offset, prev_offset = suffix_array[0], suffix_array[0]
        for i in range(1, len(suffix_array)):
            if not self.is_lms_character(suffix_array[i], suffix_types):
                continue
            cur_offset = suffix_array[i]
            if not self.is_lms_blocks_equal(data, prev_offset, cur_offset, suffix_types):
                cur_name += 1
            prev_offset = cur_offset
            lms_names[cur_offset] = cur_name
            cnt += 1

        reduced_text = [0] * cnt
        offsets = [0] * cnt
        i, j = 0, 0
        while i < len(lms_names):
            if lms_names[i] == -1:
                i += 1
                continue
            reduced_text[j] = lms_names[i]
            offsets[j] = i
            j += 1
            i += 1
        return {'reduced_text': reduced_text, 'offsets': offsets, 'cur_name': cur_name + 1}

    def construct_suffix_array(self, data, alphabet_size):
        suffix_types = self.get_suffix_types(data)
        bucket_size = self.get_bucket_size(data, alphabet_size)
        suffix_array = [-1] * (len(data) + 1)

        self.fix_lms_characters(data, suffix_array, suffix_types, bucket_size)
        self.induction_sort_l(data, suffix_array, suffix_types, bucket_size)
        self.induction_sort_r(data, suffix_array, suffix_types, bucket_size)

        summary = self.reduce_array(data, suffix_array, suffix_types)
        summary_suffix_array = self.construct_summary_suffix(summary)
        suffix_array = [-1] * (len(data) + 1)

        self.fix_lms_characters_summary(data, suffix_array, bucket_size, summary_suffix_array, summary['offsets'])
        self.induction_sort_l(data, suffix_array, suffix_types, bucket_size)
        self.induction_sort_r(data, suffix_array, suffix_types, bucket_size)

        return suffix_array

    def construct(self):
        data = [ord(c) for c in self.string]
        return self.construct_suffix_array(data, self.alphabet_size)[1:]

    def construct_summary_suffix(self, reduced_dictionary):
        reduced_text_length = len(reduced_dictionary['reduced_text'])
        if reduced_dictionary['cur_name'] == reduced_text_length:
            suffix_array = [0] * (reduced_text_length + 1)
            suffix_array[0] = reduced_text_length
            for i in range(1, reduced_text_length):
                suffix_array[reduced_dictionary['reduced_text'][i] + 1] = i
            return suffix_array
        return self.construct_suffix_array(reduced_dictionary['reduced_text'], reduced_dictionary['cur_name'])
