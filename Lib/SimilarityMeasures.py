import os
import math
import pickle
import numpy as np
from abc import abstractmethod
from collections import Counter

from Lib.SymmetricMatrix import SymmetricMatrix


class SimilarityMeasures:
    @abstractmethod
    def build(self):
        pass

    def _save_matrix(self, matrix, name_to_save):
        name_to_save = str(self.fold) + '_' + name_to_save

        with open('./pickles/' + name_to_save + '.pickle', 'wb') as f:
            pickle.dump(matrix, f)

    def _load_matrix(self, pickle_name):
        pickle_name = str(self.fold) + '_' + pickle_name

        if os.path.isfile('./pickles/' + pickle_name + '.pickle'):
            with open('./pickles/' + pickle_name + '.pickle', 'rb') as f:
                return pickle.load(f)
        else:
            raise Exception(f'Requested pickle file "{pickle_name}" does not exists')


class Pearson(SimilarityMeasures):
    def __init__(self, ratings, fold_id=None, load_matrices=False, save_matrices=False):

        if load_matrices and (fold_id is None):
            raise Exception("Please pass the fold id, I need it to load the matrices")

        self.ratings = ratings
        self.fold = fold_id
        self.load_matrices = load_matrices
        self.save_matrices = save_matrices

        # Matrices for calculating pearson matrix
        self.freqs = SymmetricMatrix(ratings.users_count, 0)
        self.uv_sums = SymmetricMatrix(ratings.users_count, 0)
        self.uu_sums = SymmetricMatrix(ratings.users_count, 0)
        self.vv_sums = SymmetricMatrix(ratings.users_count, 0)

        self.similarity_matrix = SymmetricMatrix(ratings.users_count, None)

    # Necessary matrices to calculate the pearson matrix
    def _build_matrices(self):

        matrices_list = ['freqs', 'uv_sums', 'uu_sums', 'vv_sums']

        if self.load_matrices:
            for matrix in matrices_list:
                setattr(self, matrix, self._load_matrix(matrix))
            return

        # Easier access to ratings
        ratings = self.ratings
        # Build the model so we can access (by_item)
        ratings.build_model()

        for indices in ratings.by_item.values():
            for index1 in range(len(indices)):
                index_u = indices[index1]
                u = ratings.users[index_u]
                ru = ratings.values[index_u]
                du = ru - ratings.user_ratings_avg[u]

                for index2 in range(index1 + 1, len(indices)):
                    index_v = indices[index2]
                    v = ratings.users[index_v]
                    rv = ratings.values[index_v]
                    dv = rv - ratings.user_ratings_avg[v]

                    # Update sums
                    self.freqs[u, v] += 1
                    self.uv_sums[u, v] += du * dv
                    self.uu_sums[u, v] += du * du
                    self.vv_sums[u, v] += dv * dv

        if self.save_matrices:
            for matrix_name in matrices_list:
                self._save_matrix(getattr(self, matrix_name), matrix_name)

    def build(self):
        # No matter what, if pearson.pickle exists, load and return it
        if os.path.isfile('./pickles/' + str(self.fold) + '_pearson' + '.pickle'):
            # print(f'Loading pearson for fold: {self.fold}')
            return self._load_matrix('pearson')

        print(f'Calculating pearson for fold: {self.fold}')

        # If it does not exists then build the necessary matrices then
        # build the pearson matrix, we may not build the other
        # matrices (we might load them) based on
        # load matrices = True/False
        self._build_matrices()

        for u in range(1, self.ratings.users_count):
            self.similarity_matrix[u, u] = 1

        for u in range(1, self.ratings.users_count):
            for v in range(u + 1, self.ratings.users_count):
                if self.freqs[u, v] < 2:
                    self.similarity_matrix[u, v] = None
                else:
                    numerator = self.uv_sums[u, v]
                    denominator = math.sqrt(self.uu_sums[u, v] * self.vv_sums[u, v])

                    if denominator == 0:
                        self.similarity_matrix[u, v] = None
                    else:
                        self.similarity_matrix[u, v] = numerator / denominator

        if self.save_matrices:
            self._save_matrix(self.similarity_matrix, 'pearson')

        return self.similarity_matrix


class Cosine(SimilarityMeasures):
    def __init__(self, ratings, fold_id=None, load_matrices=False, save_matrices=False):

        if load_matrices and (fold_id is None):
            raise Exception("Please pass the fold id, I need it to load the matrices")

        self.fold = fold_id
        self.save_matrices = save_matrices
        self.load_matrices = load_matrices

        self.ratings = ratings
        self.similarity_matrix = SymmetricMatrix(self.ratings.max_item_id, None)

    def build(self):

        # No matter what, if cosine.pickle exists, load and return it
        if os.path.isfile('./pickles/' + str(self.fold) + '_cosine' + '.pickle'):
            # print(f'Loading Cosine for fold: {self.fold}')
            self.similarity_matrix = self._load_matrix('cosine')
            return self.similarity_matrix

        # Matrix does not exists, so build and return it
        print('Building Cosine')
        self._build_matrices()
        return self.similarity_matrix

    def _build_matrices(self):
        ratings = self.ratings

        # Build the model so we can access (by_item)
        ratings.build_model()

        for i in set(ratings.items):
            for j in set(ratings.items):

                # Similarity of an item with itself
                if i == j:
                    continue

                # We have calculate it already
                if self.similarity_matrix[i, j] is not None:
                    continue

                # Item i and item j has been rated by these users
                i_rated_by = set([ratings.users[r] for r in ratings.by_item[i]])
                j_rated_by = set([ratings.users[r] for r in ratings.by_item[j]])

                # Set of users with rating on both i & j
                intersection = i_rated_by.intersection(j_rated_by)

                # There is no user who rated on both of these items
                if len(intersection) == 0:
                    continue

                i_ratings = np.array([ratings.rating_user_item(u, i) for u in intersection]) ** 2
                j_ratings = np.array([ratings.rating_user_item(u, j) for u in intersection]) ** 2

                self.similarity_matrix[i, j] = (np.dot(i_ratings, j_ratings) /
                                                (np.sqrt(np.sum(i_ratings)) * np.sqrt(np.sum(j_ratings))))

        if self.save_matrices:
            self._save_matrix(self.similarity_matrix, 'cosine')

    def _fix_values(self):
        # Generate a list of ratings where users rating average has been removed
        self.values = []
        for i in range(len(self.ratings.values)):
            user = self.ratings.users[i]
            r = self.ratings.values[i] - self.ratings.user_ratings_avg[user]
            r = self.ratings.scale(r)
            self.values.append(r)
