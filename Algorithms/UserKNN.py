import numpy as np
import operator
from Lib.SimilarityMeasures import Pearson
from PredictorBase import PredictorBase
from PredictionTrial import PredictionTrialSuccess, PredictionTrialFailure


class UserKNN(PredictorBase):

    def __init__(self, ratings, fold_id):
        """
        :param ratings: can be train_ratings || test_ratings
        """
        self.ratings = ratings
        self.sim_matrix = None
        self.fold_id = fold_id

        self.threshold = 0
        self.k = np.inf

    def train(self):
        super().train(self.ratings)
        pearson = Pearson(self.ratings, load_matrices=False, save_matrices=True, fold_id=self.fold_id)
        self.sim_matrix = pearson.build()

    def predict(self, user_id, item_id, rating=0):
        # Easier access to ratings
        ratings = self.ratings

        # When the user or item does not exits return GA instead
        if not ratings.check_user_item(user_id, item_id):
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        # index of all users that has rating for item i
        try:
            indexes = ratings.by_item[item_id]
        except KeyError:
            # print('Failure', item_id)
            # This item was not in our train data Failure in prediction
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        lst = []
        # Find all users that has rating on item i with a
        # correlation higher than of self.threshold
        for i in indexes:
            v = ratings.users[i]
            if user_id == v:
                continue

            sim = self.sim_matrix[user_id, v]
            if sim is not None and sim > self.threshold:
                lst.append((self.sim_matrix[user_id, v], v))

        # No similar user with our conditions:
        # > threshold
        # > k: Doesn't have any meaning here, cause it should be zero
        if len(lst) == 0:
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        if self.k is not np.inf:
            lst.sort(key=operator.itemgetter(0), reverse=True)
            lst = lst[:self.k]

        # Remove the similarities from list to only keep user id (to loop into as v)
        lst = map(operator.itemgetter(1), lst)

        dividend = 0
        divisor = 0
        for v in lst:
            # Rating of user v to item i
            rv = ratings.rating_user_item(v, item_id)

            dividend += (rv - ratings.user_ratings_avg[v]) * self.sim_matrix[user_id, v]
            divisor += self.sim_matrix[user_id, v]

        try:
            prediction = ratings.user_ratings_avg[user_id] + (dividend / divisor)
            # If 5 < prediction < 0 scale it
            prediction = ratings.scale(prediction)
        except ZeroDivisionError:
            # Division by zero, return default value
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        return PredictionTrialSuccess(prediction, 0, user_id, item_id, rating)
