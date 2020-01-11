"""
Class: Dataset

This class is responsible of loading datasets

After initializing using load method the class results two parameter:
    train:  contains train set
    test: contains test set

It's able of returning data structure in form of three lists:
    - users
    - items
    - values (which are ratings)
"""

import pandas as pd
from Ratings import Ratings


class DatasetLoader(object):

    # Default path where dataset files are located
    base_path = './dataset/'

    def __init__(self, ds_id, ds_name, ds_desc, ds_columns=None):

        if ds_columns is None:
            columns = ['user_id', 'item_id', 'values', 'timestamp']
        else:
            columns = ds_columns

        self.id = ds_id
        self.name = ds_name
        self.desc = ds_desc

        train_path = self.base_path + self.name + str(self.id) + '.base'
        test_path = self.base_path + self.name + str(self.id) + '.test'

        self.train = pd.read_csv(train_path, header=None, delim_whitespace=True)
        self.train.columns = columns

        self.test = pd.read_csv(test_path, header=None, delim_whitespace=True)
        self.test.columns = columns

        self.train_ratings = Ratings(self.to_lists(self.train))
        self.test_ratings = Ratings(self.to_lists(self.test))

    def to_lists(self, ds):
        """
        :param ds_type: str [train || test]
        :return: dataset in form of three list saved in a dict {users:u, items:i, values:v}
        """
        #ds = getattr(self, ds_type)

        lists = {
            'users': ds['user_id'].values,
            'items': ds['item_id'].values,
            'values': ds['values'].values
        }

        return lists

    def __str__(self):
        return f'Dataset Id: {self.id}, File Name: {self.name}, Description: {self.desc}. \
 train size: {len(self.train)}, test size: {len(self.test)}'


# Testing Area
# m_lens = Loader(2, 'u', 'MovieLens dataset, fold 1')
# print(len(m_lens.train))
# print(len(m_lens.test))
# print(m_lens)
