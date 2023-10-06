import pandas as pd

# Read the CSV files
general = pd.read_csv('general.csv')
prenatal = pd.read_csv('prenatal.csv')
sports = pd.read_csv('sports.csv')

# Rename columns in prenatal and sports dataframes
prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

# Concatenate the dataframes
merged = pd.concat([general, prenatal, sports], ignore_index=True)

# Drop the 'Unnamed: 0' column
merged.drop('Unnamed: 0', inplace=True, axis=1)

# Delete empty rows
merged.dropna(how='all', inplace=True)

# Correct the gender column values
merged['gender'] = merged['gender'].str.lower()
merged['gender'] = merged['gender'].replace({'female': 'f', 'male': 'm', 'woman': 'f', 'man': 'm'})

# Replace NaN values with zeros in specified columns
columns_to_replace = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
merged[columns_to_replace] = merged[columns_to_replace].fillna(0)

# Replace NaN values with 'f' in the gender column of prenatal hospital
merged.loc[merged['hospital'] == 'prenatal', 'gender'] = (merged.loc[merged['hospital'] == 'prenatal', 'gender']
                                                          .fillna('f'))

# Which hospital has the highest number of patients?
hospital_counts = merged['hospital'].value_counts()
hospital_with_most_patients = hospital_counts.index[0]
print("The answer to the 1st question is", hospital_with_most_patients)

# What share of the patients in the general hospital suffers from stomach-related issues?
general_patients = merged[merged['hospital'] == 'general']
share_stomach_issues = (general_patients['diagnosis'] == 'stomach').mean()
print("The answer to the 2nd question is", round(share_stomach_issues, 3))

# What share of the patients in the sports hospital suffers from dislocation-related issues?
sports_patients = merged[merged['hospital'] == 'sports']
share_dislocation_issues = (sports_patients['diagnosis'] == 'dislocation').mean()
print("The answer to the 3rd question is", round(share_dislocation_issues, 3))

# What is the difference in the median ages of the patients in the general and sports hospitals?
median_age_general = general_patients['age'].median()
median_age_sports = sports_patients['age'].median()
age_difference = median_age_general - median_age_sports
print("The answer to the 4th question is", age_difference)

# In which hospital the blood test was taken the most often? How many blood tests were taken?
blood_test_counts = merged.pivot_table(index='hospital', values='blood_test', aggfunc=lambda x: (x == 't').sum())
hospital_with_most_blood_tests = blood_test_counts.idxmax().iloc[0]
max_blood_tests_count = blood_test_counts.max().iloc[0]
print("The answer to the 5th question is", hospital_with_most_blood_tests + ",", max_blood_tests_count, "blood tests")
