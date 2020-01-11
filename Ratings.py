class Ratings(object):

    def __init__(self, dataset):
        """
        Initialize the instance variables
        :param dataset: dictionary of dataset in list form {users:u, items:i, values:v}

        All of these will be calculated dynamically

            users
            items
            values

            users_count =
            items_counts =
            values_counts = 100K

            min_value : 1
            max_value : 5
            values_sum : sum(values)

            min_user_id : 1
            max_user_id : 943

            min_item_id : 1
            max_item_id : 1682

            by_user : indexes of user u
            by_item : indexes of item i

            user_ratings_count : count of user's u ratings
            item_ratings_count : count of item's i ratings

            user_ratings_sum : sum of user's u ratings
            item_ratings_sum : sum of item's i ratings

            user_ratings_avg : rating average of user u
            item_ratings_avg : rating average of item i

        """

        # Reading arguments passed to constructor as a dictionary
        self.users = list(dataset['users'])
        self.items = list(dataset['items'])
        self.values = list(dataset['values'])

        # --------------------------------------------------------------

        # Counts
        # length = len(self.users)
        # self.users_count = self.items_count = self.values_count

        self.users_count = len(set(self.users))
        self.items_count = len(set(self.items))
        self.values_count = len(self.values)  # otherwise would be 5: {1-5}

        # Min and Max rating values
        # For movie lens we use 1 up to 5
        self.min_value = 1  # min(dataset['values'])
        self.max_value = 5  # max(dataset['values'])
        self.values_sum = sum(self.values)

        # Min and Max user Ids
        self.min_user_id = min(self.users)
        self.max_user_id = max(self.users)

        # Min and Max item Ids
        self.min_item_id = min(self.items)
        self.max_item_id = max(self.items)

        # Global Average
        self.global_avg = self.values_sum / self.values_count

        # =============================================================================
        #                       Usage in building indexes
        # =============================================================================

        users_keys_lst = [x for x in range(1, self.max_user_id)]
        items_keys_lst = [x for x in range(1, self.max_item_id)]

        self.by_user = {}
        self.by_item = {}

        self.user_ratings_count = dict.fromkeys(users_keys_lst, 0)
        self.item_ratings_count = dict.fromkeys(items_keys_lst, 0)

        self.user_ratings_sum = dict.fromkeys(users_keys_lst, 0)
        self.item_ratings_sum = dict.fromkeys(items_keys_lst, 0)

        self.user_ratings_avg = dict.fromkeys(users_keys_lst, 0)
        self.item_ratings_avg = dict.fromkeys(items_keys_lst, 0)

        # Build attributes indexes
        # self.build_model()

    def build_model(self):

        # Generate a unique list of users, items, values
        uq_users = set(self.users)
        uq_items = set(self.items)

        for u in uq_users:
            self.by_user[u] = []

        for i in uq_items:
            self.by_item[i] = []

        # Loop into whole data structures for 1 time (Read 100,000 value once)
        # print(len(self.users), len(self.items), len(self.values))
        for i in range(len(self.users)):
            # self.users[i] = value (use id)
            self.by_user[self.users[i]].append(i)
            self.by_item[self.items[i]].append(i)

        for u in uq_users:
            self.user_ratings_count[u] = self.user_rating_count(u)
            self.user_ratings_sum[u] = self.user_rating_sum(u)
            self.user_ratings_avg[u] = self.user_rating_avg(u)

        for i in uq_items:
            self.item_ratings_count[i] = self.item_rating_count(i)
            self.item_ratings_sum[i] = self.item_rating_sum(i)
            self.item_ratings_avg[i] = self.item_rating_avg(i)

    # A set of helpers to build by_user, by_item, and other instance variables

    # Returns the count of a user ratings
    def user_rating_count(self, user_id):
        return len(self.by_user[user_id])

    # Returns the count of an item ratings
    def item_rating_count(self, item_id):
        return len(self.by_item[item_id])

    # Returns the average of a user ratings
    def user_rating_avg(self, user_id):
        return self.user_rating_sum(user_id) / self.user_rating_count(user_id)

    # Returns the average of an item's ratings
    def item_rating_avg(self, item_id):
        return self.item_rating_sum(item_id) / self.item_rating_count(item_id)

    # Returns the rating of user v to item i
    def rating_user_item(self, user_id, item_id):
        # All indexes that this user has rated on
        indexes = self.by_user[user_id]
        for i in indexes:
            # If we found user has rating on item i
            if self.items[i] == item_id:
                # We return the rating
                return self.values[i]

        # This user has not rated on item i
        return None

    # Returns which items (item id) a user have rated on
    def user_rated_on(self, user_id):
        return [self.items[item_index] for item_index in self.by_user[user_id]]

    # Returns the sum of a user ratings
    def user_rating_sum(self, user_id):
        s = 0
        for i in self.by_user[user_id]:
            s += self.values[i]
        return s

    # Returns the sum of an item ratings
    def item_rating_sum(self, item_id):
        s = 0
        for i in self.by_item[item_id]:
            s += self.values[i]
        return s

    # Scale to correct form
    @staticmethod
    def scale(rating):
        if rating > 5:
            return 5
        elif rating < 1:
            return 1
        else:
            return rating

    # Helper methods
    def check_user_item(self, user_id, item_id):
        """
        Check and see if a user and item id exists in our dataset

        param: user_id
        param: item_id
        """

        # if user_id not in set(self.users):
        #     return False
        #
        # if item_id not in set(self.items):
        #     return False

        if user_id > self.max_user_id or user_id < self.min_user_id:
            return False

        if item_id > self.max_item_id or item_id < self.min_item_id:
            return False

        return True
