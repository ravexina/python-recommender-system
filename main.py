import pandas as pd
from Lib.ExecEval import Timing
from Dataset import DatasetLoader
from Experiments import ExperimentsResult
from Algorithms.UserKNN import UserKNN
from Algorithms.ItemKNN import ItemKNN
from Algorithms.Averaging.GlobalAverage import GlobalAverage
from Algorithms.Averaging.UserItemAverage import UserItemAverage
from Algorithms.Averaging.UserAverage import UserAverage
from Algorithms.Averaging.ItemAverage import ItemAverage


def main():
    results = []
    fold_results = []

    for algorithm in (GlobalAverage, UserAverage, ItemAverage, UserItemAverage, UserKNN, ItemKNN):
        mae = []
        pc = []
        for fold_id in range(1, 6):

            # Start timing for evaluation the execution time
            time_evaluator = Timing()

            m_lens = DatasetLoader(fold_id, 'u', f'Movie Lens Fold {fold_id}')

            rs = algorithm(m_lens.train_ratings, fold_id=fold_id)
            rs.train()

            # Default is infinity
            # rs.k = 5

            # Default is 0
            # rs.threshold = 0

            algorithm_name = rs.__class__.__name__
            print(f'\n> Running {algorithm_name} on Movie Lens, Fold: {fold_id}:\n')

            predictions = rs.evaluate(m_lens.test_ratings)
            experiment_result = ExperimentsResult(predictions)

            if hasattr(rs, 'threshold'):
                print(f'Threshold: {rs.threshold}, K: {rs.k}')

            print(f'MAE: {experiment_result.mae}')
            print(f'PCov: {experiment_result.prediction_coverage}')

            time_evaluator.end()
            time_evaluator.log()

            mae.append(experiment_result.mae)
            pc.append(experiment_result.prediction_coverage)

            fold_results.append([algorithm_name, fold_id,
                                 round(experiment_result.mae, 3),
                                 round(experiment_result.prediction_coverage, 3)])

        mae_avg = sum(mae) / len(mae)
        pc_avg = sum(pc) / len(pc)

        # Keeping more details
        results.append([algorithm_name, mae_avg, pc_avg])

        print('Average of this algorithm on all folds:')
        print(f'\nMAE Average: {mae_avg}')
        print(f'PCov Average: {pc_avg}')

        print('\n' + '=' * 60 + '\n')

    results_df = pd.DataFrame(results, columns=['Algorithm', 'MAE', 'Prediction Coverage'])
    fold_results_df = pd.DataFrame(fold_results, columns=['Algorithm', 'fold_id', 'MAE', 'PC'])

    print('\nAverage of all algorithms:\n')
    print(results_df)
    print('\n', '-'*60)
    print('\nAverage of all algorithms on different folds:\n')
    print(fold_results_df)


if __name__ == '__main__':
    main()
