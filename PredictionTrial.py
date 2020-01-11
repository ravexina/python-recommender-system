"""
This class holds details about a prediction and the state of it
whatever it has been failed or was run successfully
"""


class PredictionTrial(object):

    def __init__(self, prediction, index=0, user_id=0, item_id=0, rating=0):
        """
        :param user_id
        :param item_id
        :param rating
        :param args
            args Takes all parameters as a dictionary
            index, user_id, item_id, rating, prediction
        """
        self.index = index
        self.rating = rating
        self.user_id = user_id
        self.item_id = item_id
        self.prediction = prediction

    @property
    def done_successfully(self):
        return isinstance(self, PredictionTrialSuccess)
        
    def __str__(self):
        return f'{{PredictionTrial}} Index:{self.index} P({self.user_id}, {self.item_id},\
 {self.rating}) = {self.prediction} | Success: {self.done_successfully}'


class PredictionTrialSuccess(PredictionTrial):
    def __init__(self, prediction, index=0, user_id=0, item_id=0, rating=0):
        super().__init__(prediction, index, user_id, item_id, rating)


class PredictionTrialFailure(PredictionTrial):
    def __init__(self, prediction, index=0, user_id=0, item_id=0, rating=0):
        super().__init__(prediction, index, user_id, item_id, rating)


# Testing Area
#
# result = PredictionTrialFailure(user_id=1, item_id=2, prediction='foo')
# print(result)
#
# result = PredictionTrialSuccess(user_id=1, item_id=2, prediction='foo')
# print(result)
