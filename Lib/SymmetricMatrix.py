class SymmetricMatrix:

    def __init__(self, dimension, init_value):
        self.dimension = dimension
        self.init_value = init_value
        self.matrix = [[init_value for _ in range(i + 1)] for i in range(dimension)]

    @staticmethod
    def _fix_keys(keys):
        i, j = keys

        # Indexes start at 0 but calls start at 1, so matrix[1,1] refers to:
        # matrix[0, 0]
        i -= 1
        j -= 1

        # j can't be bigger than of i
        if i >= j:
            return i, j

        i, j = j, i
        return i, j

    def __getitem__(self, keys):
        i, j = self._fix_keys(keys)
        return self.matrix[i][j]

    def __setitem__(self, keys, value):
        i, j = self._fix_keys(keys)
        self.matrix[i][j] = value

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        return str(self.matrix)

# - Test Area, works like a charm -    
# from pprint import pprint
# mat = SymmetricMatrix(dimension=10, init_value=0)
# mat[5, 7] = 2
# pprint(mat.matrix)
