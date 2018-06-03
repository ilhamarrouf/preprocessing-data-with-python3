# Installation
```sh
$ pip install virtualenv
$ wget https://github.com/ilhamarrouf/preprocessing-data-with-python3.git ~/tesis
$ cd ~/tesis
$ virtualenv -p python3 env 
$ . env/bin/activate
$ pip install -r requirements.txt
$ python3
```
```python
>>> import nltk
>>> nltk.download('state_union')
>>> nltk.download('stopwords')
>>> nltk.download('averaged_perceptron_tagger')
>>> nltk.download('punkt')
```
- import data.sql to your sql database
- Running code 
```sh
$ python preprocessing_data.py
$ python preprocessing_data_clean.py
$ python preprocessing_data_test.py
```