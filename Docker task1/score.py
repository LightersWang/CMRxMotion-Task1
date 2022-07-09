 #!/usr/bin/env python3

import argparse
import json
import pandas as pd
import sklearn.metrics as metrics


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--submissionfile", type=str, required=True, help="Submission File")
    parser.add_argument("-g", "--goldstandard", type=str,required=True, help="Goldstandard for scoring")
    parser.add_argument("-r", "--results", type=str, required=True, default="results.json", help="Scoring results")
    return parser.parse_args()


def cal_score_tsk1(gt, pred):
    acc = metrics.accuracy_score(gt, pred)
    kappa = metrics.cohen_kappa_score(gt, pred, weights='linear')

    result = {
        'acc': acc,
        'kappa': kappa
    }

    return result


def main():
    """Main function."""
    args = get_args()

    # read files and ground truth
    pred_df = pd.read_csv(args.submissionfile, index_col=0).sort_index()
    gt_df = pd.read_csv(args.goldstandard, index_col=0).sort_index()
    pred = pred_df.iloc[:, 0].to_numpy()
    gt   = gt_df.iloc[:, 0].to_numpy()

    # cal scores of task1
    scores = cal_score_tsk1(gt, pred)

    with open(args.results, "w") as out:
        results = {
            "submission_status": "SCORED",
            **scores
        }
        out.write(json.dumps(results))


if __name__ == "__main__":
    main()
