class ExperimentsResult(object):

    def __init__(self, predictions):
        self.experiment = ExperimentsMeasures.build_by(predictions)

    @property
    def mae(self):
        return self.experiment.mae
    
    @property
    def prediction_coverage(self):
        return self.experiment.prediction_coverage


class ExperimentsMeasures(object):

    def __init__(self, prediction_count, success_count, failure_count, mae, prediction_coverage):

        self.prediction_count = prediction_count
        self.success_count = success_count
        self.failure_count = failure_count
        self.mae = mae
        self.prediction_coverage = prediction_coverage

    def __str__(self):
        return f'Prediction Count: {self.prediction_count} Success Count: {self.success_count}, Failure Count: \
{self.failure_count}, MAE: {self.mae}, Prediction Coverage: {self.prediction_coverage}'

    # Measures MAE And other stuff using a list of prediction trials
    @staticmethod
    def build_by(predictions):

        mae = 0
        # prediction_coverage = 0
        success_prediction_count = 0
        failure_prediction_count = 0
        prediction_count = len(predictions)

        for predict in predictions:
            if predict.done_successfully:
                success_prediction_count += 1
                error = abs(predict.rating - predict.prediction)
                if error > 4 or error < 0:
                    raise Exception('Prediction is not in range:', predict.prediction)

                mae += error
            else:
                failure_prediction_count += 1

        mae = None if success_prediction_count == 0 else mae / success_prediction_count
        prediction_coverage = None if prediction_count == 0 else success_prediction_count * 100 / prediction_count
        return ExperimentsMeasures(prediction_count, success_prediction_count,
                                   failure_prediction_count, mae, prediction_coverage)
