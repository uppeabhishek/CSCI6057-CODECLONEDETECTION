class BullerWheelerTransform:

    def __init__(self, string, suffix_array):
        self.string = string
        self.suffix_array = suffix_array

    def construct(self):
        return [self.string[self.suffix_array[i] - 1] for i in range(len(self.suffix_array))]
