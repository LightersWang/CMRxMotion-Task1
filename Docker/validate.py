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

COLNAMES = {
    "1": ['participant', 'was_preterm', 'probability'],
    "2": ['participant', 'was_early_preterm', 'probability']
}


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--predictions_file",
                        type=str, required=True)
    parser.add_argument("-g", "--goldstandard_file",
                        type=str, required=True)
    parser.add_argument("-t", "--task", type=str, default="1")
    parser.add_argument("-o", "--output", type=str)
    return parser.parse_args()


def check_colnames(pred, task):
    """Check for expected columns."""
    expected_columns = COLNAMES[task]
    if set(pred.columns) != set(expected_columns):
        return (
            f"Invalid columns: {pred.columns.to_list()}. "
            f"Expecting: {expected_columns}"
        )
    return ""


def check_dups(pred):
    """Check for duplicate participant IDs."""
    duplicates = pred.duplicated(subset=['participant'])
    if duplicates.any():
        return (
            f"Found {duplicates.sum()} duplicate participant ID(s): "
            f"{pred[duplicates].participant.to_list()}"
        )
    return ""


def check_missing(gold, pred):
    """Check for missing participant IDs."""
    pred.set_index('participant', inplace=True)
    missing_rows = gold.index.difference(pred.index)
    if missing_rows.any():
        return (
            f"Found {missing_rows.shape[0]} missing participant ID(s): "
            f"{missing_rows.to_list()}"
        )
    return ""


def check_values(pred):
    """Check that predictions column is binary."""
    if not pred.iloc[:, 0].isin([0, 1]).all():
        return f"'{pred.columns[0]}' column should only contain 0 and 1."
    return ""


def validate(gold_file, pred_file, task_number):
    """Validate predictions file against goldstandard."""
    errors = []

    gold = pd.read_csv(gold_file,
                       usecols=COLNAMES[task_number],
                       index_col="participant")
    pred = pd.read_csv(pred_file)

    errors.append(check_colnames(pred, task_number))
    errors.append(check_dups(pred))
    errors.append(check_missing(gold, pred))
    errors.append(check_values(pred))
    return errors


def main():
    """Main function."""
    args = get_args()

    invalid_reasons = validate(
        gold_file=args.goldstandard_file,
        pred_file=args.predictions_file,
        task_number=args.task
    )

    status = "INVALID" if invalid_reasons else "VALIDATED"
    invalid_reasons = "\n".join(filter(None, invalid_reasons))

    # truncate validation errors if >500 (character limit for sending email)
    if len(invalid_reasons) > 500:
        invalid_reasons = invalid_reasons[:496] + "..."
    res = json.dumps({
        "submission_status": status,
        "submission_errors": invalid_reasons
    })

    if args.output:
        with open(args.output, "w") as out:
            out.write(res)
    else:
        print(res)


if __name__ == "__main__":
    main()