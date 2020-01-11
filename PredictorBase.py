from abc import abstractmethod
from Ratings import Ratings


class PredictorBase(object):

    def train(self, train_ratings):
        ratings = train_ratings
        ratings.build_model()

    @abstractmethod
    def predict(self, user_id, item_id):
        pass

    def evaluate(self, test_ratings: Ratings):
        """
        :type test_ratings: Ratings
        """
        results = []

        if test_ratings is None:
            raise Exception('PredictorBase: Evaluate: parameter testRatings could not be null.')

        if len(test_ratings.values) == 0:
            return results
 
         # loop into all test data
        for i in range(test_ratings.values_count):

            # run predict (of subclass ex: global_avg) on (userid,itemid)
            user_id = test_ratings.users[i]
            item_id = test_ratings.items[i]
            rating = test_ratings.values[i]
            # result is a prediction trial
            # add result to results
            results.append(self.predict(user_id, item_id, rating))

        return results
