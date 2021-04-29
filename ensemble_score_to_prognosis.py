# call like this:
# python ensemble_score_to_prognosis.py -i "<yourPath>/ensemble.csv"
# e.g.
#python ensemble_score_to_prognosis.py -i "ensemble.csv"

import argparse
from glob import glob

import pandas as pd

print()
 
parser = argparse.ArgumentParser(description='Maps scores to MILD and SEVERE condition with MILD: score < 0.5')
parser.add_argument('-i','--input', help='Path to ensemble.csv containing the scores',required=True)
parser.add_argument('-o','--output', default='.', help='Location for combined csv called prognosis.csv')
args = parser.parse_args()

ensemble_scores_file = args.input

ensemble_scores = pd.read_csv(ensemble_scores_file)
ensemble_scores['Prognosis'] = 'SEVERE'
ensemble_scores.loc[ensemble_scores['Ensemble_Average'] < 0.5, 'Prognosis'] = 'MILD'

ensemble_scores = ensemble_scores[['PatientID', 'Prognosis']]

ensemble_scores.to_csv(args.output + "/prognosis.csv", index=False)
