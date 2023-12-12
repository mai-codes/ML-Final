import numpy as np  
import pandas as pd
from sklearn.model_selection import train_test_split
from decisiontree import DecisionTree
from logistic_regression import LogisticRegression
from adaboost import Adaboost

def accuracy_score(y_pred, y):
    return np.sum(y_pred == y) / len(y)

def recall_score(y_pred, y):
    true_positive = np.sum((y == 1) & (y_pred == 1))
    false_negative = np.sum((y == 1) & (y_pred == 0))
    
    if true_positive + false_negative == 0:
        return 0  # handle division by zero
    else:
        return true_positive / (true_positive + false_negative)

def precision_score(y_pred, y):
    true_positive = np.sum((y == 1) & (y_pred == 1))
    false_positive = np.sum((y == 0) & (y_pred == 1))
    
    if true_positive + false_positive == 0:
        return 0  # handle division by zero
    else:
        return true_positive / (true_positive + false_positive)

def f1_score(y_pred, y):
    precision = precision_score(y_pred, y)
    recall = recall_score(y_pred, y)

    if precision + recall == 0:
        return 0  # handle division by zero
    else:
        return 2 * precision * recall / (precision + recall)

def label_encode_column(df_train, column_name):
    unique_values = df_train[column_name].unique()
    mapping = {unique_values[i]: i for i in range(len(unique_values))}
    return df_train[column_name].replace(mapping)

def z_score_normalize(df_train):
    return (df_train - df_train.mean()) / df_train.std()

def calculate_metrics(y_pred, y):
    false_positive = np.sum((y == 0) & (y_pred == 1))
    false_negative = np.sum((y == 1) & (y_pred == 0))
    true_positive = np.sum((y == 1) & (y_pred == 1))
    true_negative = np.sum((y == 0) & (y_pred == 0))
    
    recall = true_positive / (true_positive + false_negative)
    precision = true_positive / (true_positive + false_positive)
    f1_score = 2 * precision * recall / (precision + recall)
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)

    return precision, recall, f1_score, accuracy

data = pd.read_csv('updated_df_train_file.csv')

y = data['class']
# y[y == 'e'] = 0
# y[y == 'p'] = 1

#For adaBoost change in the target class
y[y == 'e'] = -1
y[y == 'p'] = 1
y = y.astype(int)
x = data.drop('class', axis=1)
x_encoded = pd.get_dummies(x)

x_train, x_valid, y_train, y_valid = train_test_split(x_encoded, y, test_size=0.2, random_state=0)

# cast the dataframes to numpy
x_train = np.array(x_train)
x_valid = np.array(x_valid)
y_train = np.array(y_train)
y_valid = np.array(y_valid)


#Decision Tree
# tree = DecisionTree()
# y_valid_pred = tree.myDT(x_train, y_train, x_valid)


#Logistic Regression
# learning_rate = 0.1
# epochs = 10000
# small_value = 2**(-32)
# clf = LogisticRegression(learning_rate=0.1, epochs=10000, small_value=2**(-32))

# weights, mean_log_loss_history = clf.run_logistic_regression(x_train, y_train)




# weights, mean_log_loss_history_train = clf.run_logistic_regression(x_valid, y_valid)


#  # Metrics for training data 
# y_valid_pred = clf.predict(x_valid)


#AdaBoost
clf = Adaboost(n_clf=50)
clf.fit(x_train, y_train)
y_valid_pred = clf.predict(x_valid)


acc = accuracy_score(y_valid_pred, y_valid)
precision   = precision_score(y_valid_pred, y_valid)
recall      = recall_score(y_valid_pred, y_valid)
f1_score    = f1_score(y_valid_pred, y_valid)

#precision, recall, f1_score, accuracy = calculate_metrics(y_pred, y_valid.values)

print('Precision: ', precision)
print('Recall: ', recall)
print('F1 Score: ', f1_score)
print('Accuracy: ', acc)