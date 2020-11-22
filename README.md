# Python Recommender system
A simple recommender system in Python.

Implemented algorithms are:
- ItemKNN
- UserKNN
- ItemAverage
- UserAverage
- UserItemAverage
- GlobalAverage

# How to use it:

## DatasetI wrote this specifically to work with movielens 100k dataset. You can get it from here: http://files.grouplens.org/datasets/movielens/ml-100k.zip

Here is another link from archive.org if the link above does not work for you or it is unavailable: https://web.archive.org/web/*/http://files.grouplens.org/datasets/movielens/ml-100k.zip
Extract the content of `ml-100k` within the zip file into the `./dataset` directory.

Install the necessary dependencies and you are good to go.
## Dependencies
The libraries I've used in this project are mostly embedded in Python. The only ones you have to install are:
- Numpy- Pandas
Install Pandas and Numpy will be installed as a dependency of Pandas:

**Using pip**

``` pip install --user pandas
```    

**Using pipenv**

``` pipenv install pandas
```

## Run the project

Run the `main.py` and you should start getting the results.

``` python3 main.py
```

or

``` pipenv run python3 main.py
```
