import pandas as pd
import numpy as np 
import pickle


from ucimlrepo import fetch_ucirepo 
from pathlib import Path
from tqdm import tqdm

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mutual_info_score
from sklearn.model_selection import KFold


## Important Parameters
n_splits = 5
data_cache = Path('assets/data_cache')
output_file = Path('assets/model.bin')


print("Loading DataSet")
if data_cache.is_file():
    with open(data_cache, 'rb') as f:
        df, y = pickle.load(f)
else: 
    # fetch dataset 
    cdc_diabetes_health_indicators = fetch_ucirepo(id=891) 
      
    # data (as pandas dataframes) 
    df = cdc_diabetes_health_indicators.data.features 
    y = cdc_diabetes_health_indicators.data.targets 

    # cache it for further use
    with open(data_cache, 'wb') as f: 
        pickle.dump((df,y), f)

print("Dataset Loaded Successfully")

df['diabetes_binary'] = y
df.columns = df.columns.str.replace(' ', '_').str.lower()


binary_cols = ['highbp',
 'highchol',
 'cholcheck',
 'smoker',
 'stroke',
 'heartdiseaseorattack',
 'physactivity',
 'fruits',
 'veggies',
 'hvyalcoholconsump',
 'anyhealthcare',
 'nodocbccost',
 'diffwalk',
 'sex'
]
multicat_cols = ['age','genhlth', 'education', 'income']
cat_cols = binary_cols + multicat_cols
num_cols = ['bmi','menthlth', 'physhlth','diabetes_binary']

# map categorical values
binary_values = {
    0 : 'false',
    1 : 'true'
}

for col in binary_cols: 
    df[col] = df[col].map(binary_values)


# change categorical values to cateogary for so that we can better binary hot encode it
genhlth_values = {
    1: 'excellent',
    2: 'very_good',
    3: 'good',
    4: 'fair',
    5: 'poor'
}

df.genhlth = df.genhlth.map(genhlth_values)


education_values = {
    1 : 'never_attended_school',
    2 : 'grade_1_to_8',
    3 : 'grade_9_to_11',
    4 : 'grade_12_to_high_school_graduate',
    5 : 'college_1_to_3_years',
    6 : 'college_4_to_more'
}
df.education = df.education.map(education_values)


income_values = {
    1 : 'Less than $10,000',
    2 : '$10,000 to less than $15,000',
    3 : '$15,000 to less than $20,000',
    4 : '$20,000 to less than $25,000',
    5 : '$25,000 to less than $35,000',
    6 : '$35,000 to less than $50,000',
    7 : '$50,000 to less than $75,000',
    8 : '$75,000 or more'
}
df.income = df.income.map(income_values)
df.income = df.income.str.lower().str.replace(' ', '_').str.replace(',','')


age_values = {
    1 :	'Age 18 to 24',
    2 :	'Age 25 to 29',
    3 :	'Age 30 to 34',
    4 :	'Age 35 to 39',
    5 :	'Age 40 to 44',
    6 :	'Age 45 to 49',
    7 :	'Age 50 to 54',
    8 :	'Age 55 to 59',
    9 :	'Age 60 to 64',
    10 : 'Age 65 to 69',
    11 : 'Age 70 to 74',
    12 : 'Age 75 to 79',
    13 : 'Age 80 or older',
}
df.age = df.age.map(age_values)
df.age = df.age.str.lower().str.replace(' ', '_')


# Let's split the data from in train test split 
df_train_full, df_val = train_test_split(df, test_size=0.20, random_state=1)
df_train, df_test = train_test_split(df_train_full, test_size=0.25, random_state =1)

print("Categorical Columns Conversion Successful")



### EDA Feature importance MI and Corr

print('Calculating Features Importance (could take a min)')
def calculate_mi(series):
    return mutual_info_score(series, df_train_full.diabetes_binary.map({0: 'false', 1 : 'true'}))

df_mi = df_train_full[binary_cols + multicat_cols].apply(calculate_mi)
print(df_mi.sort_values(ascending=False))
print()
print(df_train_full[num_cols].corrwith(df_train_full.diabetes_binary))
print()

# #### I thnink I should remove few columns from the list itself as they might not contribute enough
# ['sex', 'nodocbccost', 'anyhealthcare']

unnecessary_cols = ['sex', 'nodocbccost', 'anyhealthcare', 'fruits', 'veggies']
print(f"Unncessary columns are: {unnecessary_cols}")

# # Let's try to optimize the hyperparameter for Randomforest Classifier
# # Found best is between 60 to 100 then becomes nearly constant till 200. Trust me or run it to be sure will take around 20 to 30 minutes

# n_estimators = np.linspace(start = 1, stop = 200, num = 50,endpoint = True)
# n_estimators = [int(x) for x in n_estimators]
# scores = []
# for estimator in tqdm(n_estimators, total=50): 
#     rf = RandomForestClassifier(n_estimators = estimator, random_state =1 )
#     rf.fit(X_train, y_train)

#     y_pred = rf.predict_proba(X_val)[:, 1]
#     score = roc_auc_score(y_val, y_pred)
#     scores.append((estimator, score))

# df_scores = pd.DataFrame(scores, columns = ['estimator', 'score'])

# sns.set_theme()
# sns.relplot(data = df_scores, x='estimator', y='score')


# #### Approach 2 Gradient Boosting

# In[30]:


## Later On Sometime, let's first work on deployment


# ### Tuning K-Fold hyperparameter 

# In[33]:


train_cols = list(set(num_cols + cat_cols) - set(unnecessary_cols) - set(['diabetes_binary']))
train_cols


def train(df_train, y_train, n_estimators=69):
    dict = df_train[train_cols].to_dict(orient='records')
    dv  = DictVectorizer(sparse=False)

    X_train = dv.fit_transform(dict)
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=1)
    model.fit(X_train, y_train)

    return dv, model


def predict(df,dv,model): 
    dicts = df[train_cols].to_dict(orient='records')

    X = dv.transform(dicts)
    y_pred = model.predict_proba(X)[:, 1]

    return y_pred



kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)
scores = []
fold = 1
for train_idx, val_idx in tqdm(kfold.split(df_train_full)):
    df_train = df_train_full.iloc[train_idx]
    df_val = df_train_full.iloc[val_idx]

    y_train = df_train.diabetes_binary.values
    y_val = df_val.diabetes_binary.values

    del df_train['diabetes_binary']
    del df_val['diabetes_binary']

    dv,model = train(df_train, y_train)
    y_pred = predict(df_val, dv, model)

    auc = roc_auc_score(y_val, y_pred)
    scores.append(auc)
    print(f'AUC on fold {fold} = {auc}')
    fold += 1



print('n_splits=%s mean_score=%.3f std_dev=+- %.3f' % (n_splits,np.mean(scores), np.std(scores)))


# #### Since deviation is low we can be sure that model has said accuracy
with open(output_file, 'wb') as f: 
    pickle.dump((dv, model), f)
    print(f"Model Dumped Successfully at :: {output_file}")
