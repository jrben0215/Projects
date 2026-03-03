import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import accuracy_score, roc_curve, roc_auc_score, auc, classification_report
import matplotlib.pyplot as plt
from sklearn import datasets

file_path = 'C:\\Users\\jrben\\OneDrive\\Desktop\\heartdisease.csv'
df = pd.read_csv(file_path)

x = df.drop(columns = ['ten_year_chd'])
y = df['ten_year_chd']

x = x.apply(lambda col: col.fillna(col.median()), axis=0)

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)


model = LogisticRegression(max_iter = 5000)
model.fit(x, y)

# evaluating model on the test set
y_pred = model.predict(x)
y_pred_proba = model.predict_proba(x)[:, 1]


coefficients = pd.DataFrame({
    'Feature': x.columns,
    'Coefficient': model.coef_[0]
})

print("Model Coefficients:")
print(coefficients.sort_values(by="Coefficient", ascending=False))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=42)

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LogisticRegression(max_iter = 5000)
model.fit(x_train, y_train)

# evaluating model on the test set
y_test_pred = model.predict(x_test)
y_test_pred_proba = model.predict_proba(x_test)[:, 1]

#calculating accuracy
accuracy = accuracy_score(y_test, y_test_pred)

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_test_pred_proba)
auc = roc_auc_score(y_test, y_test_pred_proba)

# Plot ROC
plt.figure()
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.2f})")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()

print(f"Accuracy: {accuracy:.2f}, AUC: {auc:.2f}")

iris = datasets.load_iris()
x = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target)

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

model = LogisticRegression(solver='lbfgs', max_iter=1000)
model.fit(x_scaled, y)

coefficients = model.coef_
print("Model Coefficients:")
print(coefficients)

odds_ratios = np.exp(coefficients)

odds_ratio_df = pd.DataFrame(odds_ratios.T, columns=[f'Class {i}' for i in range(3)], index=iris.feature_names)

print("\nOdds Ratios for predictors:")
print(odds_ratio_df)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

lasso_model = LogisticRegressionCV(cv=5, solver='liblinear', max_iter=1000,
                                   penalty='l1', scoring='accuracy')
lasso_model.fit(x_train, y_train)

# Predict and evaluate the Lasso model
y_pred_lasso = lasso_model.predict(x_test)

# Performance Metrics for Lasso (L1) regularization model
print("\nLasso Model Performance Metrics:")
print("Accuracy:", accuracy_score(y_test, y_pred_lasso))
print("\nClassification Report (Lasso):\n", classification_report(y_test, y_pred_lasso))

# Original logistic regression model
orig_model = LogisticRegression(solver='lbfgs', max_iter=1000)
orig_model.fit(x_train, y_train)

# Predict and evaluate the original model
y_pred_orig = orig_model.predict(x_test)

# Performance Metrics for the original model
print("\nOriginal Model Performance Metrics:")
print("Accuracy:", accuracy_score(y_test, y_pred_orig))

print("\nClassification Report (Original):\n", classification_report(y_test, y_pred_orig))
