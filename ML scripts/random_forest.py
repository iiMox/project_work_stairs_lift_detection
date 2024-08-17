import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from collections import Counter
from imblearn.over_sampling import RandomOverSampler
from helper_functions import validationCurveEstimatorsChart, generateConfusionMatrix, saveResultsToSheet

randSeed = 789456 #do not change this random seed anytime.

def trainModal(filepath, testParticipant):
    output = f'{filepath}/Collected Data/preprocessed/{testParticipant}'
    
    data = pd.read_csv(f'{output}/preprocessed_traindata.csv')

    x = data.drop('Label', axis=1) #features
    y = data['Label']
    y = y.str.strip()

    labelEncoder = LabelEncoder()
    encodedTrainingLabels = labelEncoder.fit_transform(y)

    labelMapping = dict(zip(encodedTrainingLabels, y))

    y = encodedTrainingLabels
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)

    xTrainResampled, yTrainResampled = RandomOverSampler(sampling_strategy= "not majority", random_state=randSeed).fit_resample(xTrain, yTrain)
    #print (sorted(Counter(yTrainResampled).items())) 

    xResampled, yResampled = RandomOverSampler(sampling_strategy= "not majority", random_state=randSeed).fit_resample(x, y)
    #print (sorted(Counter(yResampled).items()))

    # Define the parameter grid
    paramGrid = {
        'n_estimators': [200, 225, 250, 275, 300, 325, 350],  # Testing different values for n_estimators
        'max_depth': [None,5, 10, 15, 20],       # Testing different values for max_depth
    }

    # Initializing Random Forest classifier
    rfClassifier = RandomForestClassifier(random_state=randSeed)

    # Initialize GridSearchCV
    gridSearch = GridSearchCV(estimator=rfClassifier, param_grid=paramGrid, cv=10, scoring='accuracy', n_jobs=-1)

    # Perform grid search to find the best hyperparameters
    gridSearch.fit(xResampled, yResampled)

    # Get the best model and best parameters
    bestRf = gridSearch.best_estimator_
    bestParams = gridSearch.best_params_

    print("Best Parameters:", bestParams)

    validationCurveEstimatorsChart(gridSearch, output)

    final_rf = RandomForestClassifier(n_estimators=200, random_state=randSeed) # Training the model using the best parameters
    final_rf.fit(xResampled, yResampled) #use xTrainResampled & yTrainResampled for training accuracy. x_resampled and y_resampled for testing accuracy

    data = pd.read_csv(f'{output}/preprocessed_testdata.csv')

    xTest = data.drop('Label', axis=1) #features
    yTest = data['Label'].str.strip()

    encodedTestingLabels = labelEncoder.fit_transform(yTest)
    labelMapping = dict(zip(encodedTestingLabels, yTest))
    print("Label Mapping:", labelMapping)
    print(encodedTestingLabels)

    yPred = final_rf.predict(xTest)
    yTest = encodedTestingLabels
    accuracy = accuracy_score(yTest, yPred)
    print("Accuracy:", accuracy)
    f1Micro = f1_score(yTest, yPred, average='micro')
    f1Macro = f1_score(yTest, yPred, average='macro')
    f1Weighted = f1_score(yTest, yPred, average='weighted')
    print("F1 Score micro:", f1Micro)
    print("F1 Score macro:", f1Macro)
    print("F1 Score weighted:", f1Weighted)

    generateConfusionMatrix(yTest, yPred, labelEncoder, output)

    importanceList = final_rf.feature_importances_
    features = x.columns  # Get feature names from your DataFrame
    featuresImportance = pd.DataFrame({'Feature': features, 'Importance': importanceList})
    featuresImportance = featuresImportance.set_index('Feature')
    
    importanceList = list(map(lambda x: str(x), importanceList))
    print(",".join(importanceList))

    # Print the transposed DataFrame
    print(featuresImportance)

    saveResultsToSheet(bestParams, accuracy, f1Micro, f1Macro, f1Weighted, featuresImportance, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Random Forest',
                    description='Execute Random Forest Ons Preprocessed Data',
                    epilog='Text at the bottom of help')
    parser.add_argument('filepath') # "C:/...../Collected Data/"
    parser.add_argument('-tp', '--testParticipant')

    args = parser.parse_args()
    trainModal(args.filepath, args.testParticipant)