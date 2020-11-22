import numpy as np
import operator
from Lib.SimilarityMeasures import Cosine
from PredictorBase import PredictorBase
from PredictionTrial import PredictionTrialSuccess, PredictionTrialFailure


class ItemKNN(PredictorBase):

    def __init__(self, ratings, fold_id):
        """
        :type ratings: train_ratings
        :param ratings: can be train_ratings || test_ratings
        """
        self.ratings = ratings
        self.sim_matrix = None
        self.fold_id = fold_id

        self.k = np.inf
        self.threshold = 0

    def train(self):
        super().train(self.ratings)
        cosine = Cosine(self.ratings, load_matrices=False, save_matrices=True, fold_id=self.fold_id)
        self.sim_matrix = cosine.build()

    def predict(self, user_id, item_id, rating=0):
        # Easier access to ratings
        ratings = self.ratings

        # When the user or item does not exits return GA instead
        if not ratings.check_user_item(user_id, item_id):
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        # Items rated by this user
        items = ratings.user_rated_on(user_id)

        sim_list = []
        for j in items:
            if self.sim_matrix[item_id, j] is not None and self.sim_matrix[item_id, j] > self.threshold:
                sim_list.append((self.sim_matrix[item_id, j], j))

        # No similar user with our conditions (threshold)
        if len(sim_list) == 0:
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)

        if self.k is not np.inf:
            sim_list.sort(key=operator.itemgetter(0), reverse=True)
            sim_list = sim_list[:self.k]

        # Remove the similarities from list to only keep user id (to loop into as v)
        sim_list = map(operator.itemgetter(1), sim_list)

        dividend = 0
        divisor = 0
        for j in sim_list:
            # Rating of user to item i
            rv = ratings.rating_user_item(user_id, j)

            dividend += rv * self.sim_matrix[item_id, j]
            divisor += self.sim_matrix[item_id, j]

        try:
            prediction = dividend / divisor
            # If 5 < prediction < 0 scale it
            prediction = ratings.scale(prediction)
            return PredictionTrialSuccess(prediction, 0, user_id, item_id, rating)

        except ZeroDivisionError:
            # Division by zero, return default value
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)
