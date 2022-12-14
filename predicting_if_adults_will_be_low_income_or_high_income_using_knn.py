# -*- coding: utf-8 -*-
"""Predicting if Adults will be low income or high income using KNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qBjbj3pWRlcxfAHJBB_WldTOFhd43S3N
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

# Commented out IPython magic to ensure Python compatibility.
#mount google drive for file access
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive

data = pd.read_csv(r"/gdrive/MyDrive/Learning ML/KNN (K-Nearest Neighbors)/Incomes.csv")
data.head()

'''

p = preprocessing.LabelEncoder()

l = []
for i in data.columns:
  if data[i].dtype == 'object':
    #x = p.fit_transform(list(data[i]))
    #l.append(x)
    print(i)

'''

#replace categorical data with qunatitative data
p = preprocessing.LabelEncoder()
workclass = p.fit_transform(list(data['workclass']))
education = p.fit_transform(list(data['education']))
marital_status = p.fit_transform(list(data['marital-status']))
occupation = p.fit_transform(list(data['occupation']))
relationship = p.fit_transform(list(data['relationship']))
race = p.fit_transform(list(data['race']))
gender = p.fit_transform(list(data['gender']))
native_country = p.fit_transform(list(data['native-country']))
income = p.fit_transform(list(data['income']))

x = list(zip(workclass, education, marital_status, occupation, relationship,race, gender, native_country))
y = list(income)

"""# Single Test"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=47)
model.fit(x_train, y_train)
accuracy = model.score(x_test, y_test)
print(accuracy)

"""# Optimizing"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

from operator import indexOf
results = []
best = None
for i in range(100):
  model = KNeighborsClassifier(n_neighbors=i+1)
  model.fit(x_train, y_train)
  accuracy = model.score(x_test, y_test)
  results.append(accuracy)

maximum = max(results)

print("best is " , maximum, "\n"+ "at index ", indexOf(results, maximum))

"""# Results"""

