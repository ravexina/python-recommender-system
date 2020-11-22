# Python Recommender system
A simple recommender system in Python.

## Implemented Algorithms

Implemented algorithms are:
- ItemKNN
- UserKNN
- ItemAverage
- UserAverage
- UserItemAverage
- GlobalAverage

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
