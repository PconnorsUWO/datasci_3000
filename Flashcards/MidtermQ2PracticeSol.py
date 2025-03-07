## Block 1: Importing libraries
import numpy as np
from itertools import chain, combinations
import pandas as pd
import polars as pl
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SequentialFeatureSelector
import matplotlib.pyplot as plt
import seaborn as sns

## Block 2: Data loading
# Load the data using polars
df = pl.read_csv("data_clean.parquet")

# Calculate the descriptive statistics
df.describe()

# Calculate X and y vectors
X = df.drop(["target"])
y = df.select("target")

## Block 3: Data splitting and cleaning
# Split the data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Get the train median values
v1_median = X_train.select('Var1').median()
v2_median = X_train.select('Var2').median()

# Fill the missing values with the median
X_train = X_train.with_columns(pl.col('Var1').replace(0, v1_median))
X_train = X_train.with_columns(pl.col('Var2').replace(0, v2_median))
X_test = X_test.with_columns(pl.col('Var1').replace(0, v1_median))
X_test = X_test.with_columns(pl.col('Var2').replace(0, v2_median))

## Block 4: Standardize the data
# Define the standard scaler
scaler = StandardScaler()

# Fit the scaler on the training data
scaler.fit(X_train)

# Transform the training and test data
X_train_scaled = scaler.transform(X_train)

# Transform the test data
X_test_scaled = scaler.transform(X_test)

## Block 5: ElasticNetCV model applied to the test set
# Define the ElasticNetCV model
model = ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, .99, 1], 
                     n_alphas=100, cv=5)

# Fit the model
model.fit(X_train_scaled, y_train)

# Predict the test set
y_pred = model.predict(X_test_scaled)

# Calculate the MSE and R2
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
