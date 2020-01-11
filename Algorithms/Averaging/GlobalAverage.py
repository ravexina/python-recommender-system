from PredictorBase import PredictorBase
from PredictionTrial import PredictionTrialSuccess, PredictionTrialFailure


class GlobalAverage(PredictorBase):

    def __init__(self, ratings, fold_id=None):
        """
        :param ratings: can be train_ratings || test_ratings
        """
        self.ratings = ratings

    def train(self):
        super().train(self.ratings)

    def predict(self, user_id, item_id, rating=0):
        
        # Easier access to ratings
        ratings = self.ratings
        
        # Create a default value if we were not able to calculate GAvg
        default = (ratings.min_value + ratings.max_value) / 2
        
        # When there is no rating
        if ratings.values_count == 0:
            return PredictionTrialFailure(default, 0, user_id, item_id, rating)
        # When the user or item does not exits
        elif not ratings.check_user_item(user_id, item_id):
            return PredictionTrialFailure(default, 0, user_id, item_id, rating)
        # return Global Avg
        else:
            return PredictionTrialSuccess(ratings.global_avg, 0, user_id, item_id, rating)
