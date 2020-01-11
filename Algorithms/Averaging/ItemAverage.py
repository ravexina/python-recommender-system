from PredictorBase import PredictorBase
from PredictionTrial import PredictionTrialSuccess, PredictionTrialFailure


class ItemAverage(PredictorBase):

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

        # When the user or item does not exits return GA instead
        if not ratings.check_user_item(user_id, item_id):
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)
        # When user has not rate anything
        elif ratings.item_ratings_count[item_id] == 0:
            # When we have no ratings return default
            if ratings.values_count == 0:
                return PredictionTrialFailure(default, 0, user_id, item_id, rating)
            # Otherwise return global average
            return PredictionTrialFailure(ratings.global_avg, 0, user_id, item_id, rating)
    
        # Return item_id ratings average
        return PredictionTrialSuccess(ratings.item_ratings_avg[item_id], 0, user_id, item_id, rating)
