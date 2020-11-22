# Python Recommender system
A simple recommender system in Python.

## Implemented Algorithms

- Implemented algorithms are:
  - ItemKNN
  - UserKNN
  - ItemAverage
  - UserAverage
  - UserItemAverage
  - GlobalAverage

- Similarity meseaurs:
  - Item based nearest neighbor
    - [Cosine](https://en.wikipedia.org/wiki/Cosine_similarity)
  - User based nearest neighbor
    - [Pearson](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)

## Test
The dataset comes in 5 folds. So without chaning how it looks, we ues it to perform a 5-fold cross-validation.

- To meseaure the quality of the predictions we use:
  - Prediction Coverage
  - [Mean absolute error MAE](https://en.wikipedia.org/wiki/Mean_absolute_error)

### Results
To see a set of results on a run check [here](https://github.com/ravexina/python-recommender-system/tree/master/results).

# How to use it:

## Download

Clone the project using:

```bash
git clone https://github.com/ravexina/python-recommender-system.git
```

Or downloading it from [here](https://github.com/ravexina/python-recommender-system/archive/master.zip): 

```bash
wget https://github.com/ravexina/python-recommender-system/archive/master.zip
```


## Dataset

I wrote this specifically to work with movielens 100k dataset. You can get it from here:  
http://files.grouplens.org/datasets/movielens/ml-100k.zip

Here is another link from archive.org if the link above does not work for you or it is unavailable:  
https://web.archive.org/web/*/http://files.grouplens.org/datasets/movielens/ml-100k.zip

Extract the content of `ml-100k` within the zip file into the `./dataset` directory. Install the necessary dependencies and you are good to go.

## Dependencies
The libraries I've used in this project are mostly embedded in Python. The only ones you have to install are:

- Numpy
- Pandas

Install Pandas and Numpy will be installed as a dependency of Pandas:

**Using pip**

```
pip install --user pandas
```

**Using pipenv**

```
pipenv install pandas
```

## Run the project

Run the `main.py` and you should start getting the results.

```
python3 main.py
```

or

```
pipenv run python3 main.py
```

# Improve the runtime

As you might know, similiraty matrices takes some to calculate. Once you run the project it stores calculated matrices in form of pickles in `./pickles` directory.

In the file `Algorithms/ItemKNN.py` and `Algorithms/UserKNN.py` there are two lines, which you can set an argument named `load_matrices` to `true` so next time you run the project it does not tries to recalculate the similarity matrices and uses the old one.

```python
# UserKNN
cosine = Cosine(self.ratings, load_matrices=False, save_matrices=True, fold_id=self.fold_id)
```

```python
# ItemKNN.py
pearson = Pearson(self.ratings, load_matrices=False, save_matrices=True, fold_id=self.fold_id)
```

## Download the pre-calculated pickles

Will be added soon.
