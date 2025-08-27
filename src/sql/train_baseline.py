# install once if needed: pip install scikit-learn
import duckdb, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression

con = duckdb.connect("data/features.duckdb")
df = con.execute("""
SELECT
  (control_status = 'Poorly Controlled')::INT AS y,
  age, bmi, smoker_flag, er_visits, fev1,
  gender, bmi_category, comorbidity, environment
FROM asthma_features
""").fetch_df()
con.close()

X = df.drop(columns=["y"])
y = df["y"]

num_cols = ["age","bmi","smoker_flag","er_visits","fev1"]
cat_cols = ["gender","bmi_category","comorbidity","environment"]

pre = ColumnTransformer([
    ("num", "passthrough", num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

clf = Pipeline([
    ("pre", pre),
    ("lr", LogisticRegression(max_iter=200))
])

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
clf.fit(X_tr, y_tr)
proba = clf.predict_proba(X_te)[:,1]
pred  = (proba >= 0.5).astype(int)

print(classification_report(y_te, pred))
print("ROC-AUC:", roc_auc_score(y_te, proba))