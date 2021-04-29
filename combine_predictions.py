# call like this:
# python combine_predictions.py --gt "<yourPath>/trainSet.txt" --i "<yourPathToPredictionCSVs>"
# e.g.
#python combine_predictions.py -gt "hida_workspace/HackathonCovidData/trainSet/trainSet.txt" -i "hida_workspace/HackathonCovidData/predictions/"

import argparse
from glob import glob

import pandas as pd

print()
 
parser = argparse.ArgumentParser(description='Combines all predictions from csv files in folder given by --input')
parser.add_argument('-gt','--groundtruth', help='Path to trainSet.txt or testSet.txt to set it as ground truth',required=True)
parser.add_argument('-i','--input', help='Folder containing als prediciton-csvs',required=True)
parser.add_argument('-o','--output', default='.', help='Location for combined csv called ensemble.csv')
args = parser.parse_args()

groundtruth = args.groundtruth

clinical_data = pd.read_csv(groundtruth)

ground_truth = clinical_data[["PatientID", "Prognosis"]].copy()
if (ground_truth.Prognosis[0] != '<undefined>'):
    ground_truth['GroundTruth'] = 0
    ground_truth.loc[ground_truth.Prognosis == "SEVERE", 'GroundTruth'] = 1
ground_truth = ground_truth.drop('Prognosis', axis=1)

print('Loading Prediction Files from ' + args.input)
prediction_files = glob(args.input + "*.csv")

for prediction_file in prediction_files:
    predictions = pd.read_csv(prediction_file).set_index('PatientID')
    ground_truth = ground_truth.join(predictions, on=['PatientID'])

print('Calculating Average')
ground_truth['Ensemble_Average'] = ground_truth.drop(['GroundTruth', 'PatientID'], axis=1, errors='ignore').mean(axis=1)

print('Saving ensemble.csv to ' + args.output + "/ensemble.csv")
#print(ground_truth)
ground_truth.to_csv(args.output + "/ensemble.csv", index=False)

print()