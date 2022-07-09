#!/usr/bin/env python3
"""Validate prediction file.
Prediction files between Task 1 and 2 are pretty much exactly
the same, with the exception of one column name, where:
    - Task 1: done
    - Task 2: empty
"""

import json
import argparse
import pandas as pd

# COLNAMES = {
#     "1": ['participant', 'was_preterm', 'probability'],
#     "2": ['participant', 'was_early_preterm', 'probability']
# }


def get_args():
    parser = argparse.ArgumentParser()
    """Set up command-line interface and get arguments."""
    parser.add_argument("-s", "--submission_file", help="Submission File")
    parser.add_argument("-g", "--goldstandard", required=True, help="Goldstandard for scoring")
    parser.add_argument("-e", "--entity_type", required=True, help="synapse entity type downloaded")
    parser.add_argument("-r", "--results", required=True, help="validation results")
    return parser.parse_args()


def main():
    """Main function."""
    args = get_args()

    if args.submission_file is None:
            prediction_file_status = "INVALID"
            invalid_reasons = ['Expected FileEntity type but found ' + args.entity_type]
    else:
        required_shape = (40, 2)
        invalid_reasons = []
        prediction_file_status = "VALIDATED"

        # judge if csv file
        try:
            submission_df = pd.read_csv(args.submission_file)
            if not (submission_df.shape == required_shape):
                invalid_reasons.append(f"Submission csv is not in right shape (i.e. {required_shape})")
                invalid_reasons.append(f"Actual shape is {submission_df.shape}")
                prediction_file_status = "INVALID"
            # if nan eexist
            for col in range(2):
                if submission_df.iloc[:, col].isnull().any():
                    invalid_reasons.append(f"Column {col} of submission csv file contains NaN value")
                    prediction_file_status = "INVALID"

            # if match gold standard ImageName
            gt_df = pd.read_csv(args.goldstandard)
            if not (set(gt_df.iloc[:, 0].tolist()) == set(submission_df.iloc[:, 0].tolist())):
                invalid_reasons.append(f"Image name in submission csv file doesn't match standard submission.")
                prediction_file_status = "INVALID"

        except:
            invalid_reasons.append("Cannot open submission file with pandas.read_csv()")
            invalid_reasons.append(f"Path is {args.submission_file}")
            prediction_file_status = "INVALID"
    result = {'submission_errors': "\n".join(invalid_reasons),
              'submission_status': prediction_file_status}
    with open(args.results, 'w') as o:
        o.write(json.dumps(result))


if __name__ == "__main__":
    main()    
