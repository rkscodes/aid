# Am I Diabetic 🩺


https://github.com/rkscodes/aid/assets/30290728/401317bc-5e5b-4421-bf93-900d26c99c57


API :: https://predict-diabetes.fly.dev/predict 

[See the CURL command to hit the API below](#cloud-deployment-instruction)

## Dataset
[CDC Diabetes Health Indicators reference page](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)

The Diabetes Health Indicators Dataset contains healthcare statistics and lifestyle survey information about people in general along with their diagnosis of diabetes. The 35 features consist of some demographics, lab test results, and answers to survey questions for each patient.

Data is loaded direclty in code using the `ucimlrepo` module

## Problem Statement
1. The rising global prevalence of diabetes presents a significant challenge for healthcare systems, necessitating early detection and management to improve patient outcomes and reduce healthcare costs.

2. The Diabetes Health Indicators Dataset contains comprehensive information, including demographics, lab test results, and lifestyle survey responses, for a diverse group of individuals.

3. The primary objective is to develop a predictive model that accurately classifies individuals into one of two categories: diabetic or healthy.

4. Achieving this prediction will contribute to the early detection and management of diabetes, thereby improving patient outcomes and alleviating the burden on healthcare systems.

## Objective
Develop a predictive model using the Diabetes Health Indicators Dataset to classify individuals into diabetic and healthy category.

## Architecture
<img src='assets/arch.png'>


## Project Setup
To get started with this project, clone the repository to your local machine:
```bash
git clone https://github.com/rkscodes/aid.git
cd aid
```
Make sure you have [Conda/MiniConda](https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install) installed.
1. Setup virtual env 
	```bash
	conda create -n aid python=3.8 poetry
	```
2. Activate the env 
	```bash
	conda activate aid
	```
3. Install the dependency
	```bash
	poetry install --no-root --without dev
	```
4. Train Model
	```bash
	python train.py
	```

## Docker Setup
1. Make sure you are in root `aid/` containing `Dockerfile`.
2. Build Dockerfile Image
	```bash
	docker build -t predict_diabetes .
	```
3. Run Docker container
	```bash
	docker run -it --rm -p 6969:6969 predict_diabetes
	```
4. You can now now send `POST` request
	```bash
	curl -X POST \
	-H "Content-Type: application/json" \
	-d '{
		"highbp": "false",
		"highchol": "true",
		"cholcheck": "true",
		"bmi": 25,
		"smoker": "true",
		"stroke": "false",
		"heartdiseaseorattack": "false",
		"physactivity": "true",
		"fruits": "false",
		"veggies": "true",
		"hvyalcoholconsump": "false",
		"anyhealthcare": "true",
		"nodocbccost": "false",
		"genhlth": "good",
		"menthlth": 15,
		"physhlth": 3,
		"diffwalk": "true",
		"sex": "false",
		"age": "age_60_to_64",
		"education": "college_4_to_more",
		"income": "$50000_to_less_than_$75000"
	}' \
	http://0.0.0.0:6969/predict
    ```

## Cloud Deployment Instruction
1. Make sure you are in root folder containing `fly.toml`.
2. Create an account on [`fly.io`](https://fly.io)
3. Make sure to activate your account by entering credit card details, you might be charged!
4. Install `flyctl` 
	```bash
	brew install flyctl
	```
5. Authorize `flyctl`
	```bash
	flyctl auth login
	```
6. To deploy run
	```bash
	flyctl deploy
	```
7. Hit the api with tool of your choice or using curl
	```bash
	curl -X POST \
	-H "Content-Type: application/json" \
	-d '{
		"highbp": "false",
		"highchol": "true",
		"cholcheck": "true",
		"bmi": 25,
		"smoker": "true",
		"stroke": "false",
		"heartdiseaseorattack": "false",
		"physactivity": "true",
		"fruits": "false",
		"veggies": "true",
		"hvyalcoholconsump": "false",
		"anyhealthcare": "true",
		"nodocbccost": "false",
		"genhlth": "good",
		"menthlth": 15,
		"physhlth": 3,
		"diffwalk": "true",
		"sex": "false",
		"age": "age_60_to_64",
		"education": "college_4_to_more",
		"income": "$50000_to_less_than_$75000"
	}' \
	https://predict-diabetes.fly.dev/predict
    ```

## Data column defination
<details>

| Variable Name | Role | Type | Demographic | Description | Missing Values |
| --- | --- | --- | --- | --- | --- |
| ID | ID | Integer | Patient ID | no |
| Diabetes_binary | Target | Binary | 0 = no diabetes 1 = prediabetes or diabetes | no |
| HighBP | Feature | Binary | 0 = no high BP 1 = high BP | no |
| HighChol | Feature | Binary | 0 = no high cholesterol 1 = high cholesterol | no |
| CholCheck | Feature | Binary | 0 = no cholesterol check in 5 years 1 = yes cholesterol check in 5 years | no |
| BMI | Feature | Integer | Body Mass Index | no |
| Smoker | Feature | Binary | Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes] 0 = no 1 = yes | no |
| Stroke | Feature | Binary | (Ever told) you had a stroke. 0 = no 1 = yes | no |
| HeartDiseaseorAttack | Feature | Binary | coronary heart disease (CHD) or myocardial infarction (MI) 0 = no 1 = yes | no |
| PhysActivity | Feature | Binary | physical activity in past 30 days - not including job 0 = no 1 = yes | no |
| Fruits | Feature | Binary | Consume Fruit 1 or more times per day 0 = no 1 = yes | no |
| Veggies | Feature | Binary | Consume Vegetables 1 or more times per day 0 = no 1 = yes | no |
| HvyAlcoholConsump | Feature | Binary | Heavy drinkers (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week) 0 = no 1 = yes | no |
| AnyHealthcare | Feature | Binary | Have any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc. 0 = no 1 = yes | no |
| NoDocbcCost | Feature | Binary | Was there a time in the past 12 months when you needed to see a doctor but could not because of cost? 0 = no 1 = yes | no |
| GenHlth | Feature | Integer | Would you say that in general your health is: scale 1-5 1 = excellent 2 = very good 3 = good 4 = fair 5 = poor | no |
| MentHlth | Feature | Integer | Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health not good? scale 1-30 days | no |
| PhysHlth | Feature | Integer | Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health not good? scale 1-30 days | no |
| DiffWalk | Feature | Binary | Do you have serious difficulty walking or climbing stairs? 0 = no 1 = yes | no |
| Sex | Feature | Binary | Sex | 0 = female 1 = male | no |
| Age | Feature | Integer | Age | 13-level age category (_AGEG5YR see codebook) 1 = 18-24 9 = 60-64 13 = 80 or older | no |
| Education | Feature | Integer | Education Level | Education level (EDUCA see codebook) scale 1-6 1 = Never attended school or only kindergarten 2 = Grades 1 through 8 (Elementary) 3 = Grades 9 through 11 (Some high school) 4 = Grade 12 or GED (High school graduate) 5 = College 1 year to 3 years (Some college or technical school) 6 = College 4 years or more (College graduate) | no |
| Income | Feature | Integer | Income | Income scale (INCOME2 see codebook) scale 1-8 1 = less than $10,000 5 = less than $35,000 8 = $75,000 or more | no |
</details>

## Acknowledgements
It it important to reiterate that I did not create this dataset, it is just a cleaned and consolidated dataset created from the BRFSS 2015 dataset already on Kaggle. That dataset can be found [here](https://www.kaggle.com/cdc/behavioral-risk-factor-surveillance-system) and the notebook used for the data cleaning can be found [here](https://www.kaggle.com/alexteboul/diabetes-health-indicators-dataset-notebook).

## License
[MIT License](LICENSE)
