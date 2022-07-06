#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Score predictions file

requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
    - entryname: score.py
      entry: |
        #!/usr/bin/env python
        import argparse
        import json
        try:
            import sklearn
        except:
            import os
            os.system("pip3 install sklearn")
        import sklearn.metrics as metrics
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--submissionfile", required=True, help="Submission File")
        parser.add_argument("-r", "--results", required=True, help="Scoring results")
        parser.add_argument("-g", "--goldstandard", required=True, help="Goldstandard for scoring")

        args = parser.parse_args()

        pred_df = pd.read_csv(args.submissionfile, index_col=0).sort_index()
        gt_df = pd.read_csv(args.goldstandard, index_col=0).sort_index()
        pred = pred_df.iloc[:, 0].to_numpy()
        gt = gt_df.iloc[:, 0].to_numpy()
        acc = metrics.accuracy_score(gt, pred)
        kappa = metrics.cohen_kappa_score(gt, pred)
        prediction_file_status = "SCORED"

        result = {'acc': acc,
                  'kappa': kappa,
                  'submission_status': prediction_file_status}
        with open(args.results, 'w') as o:
            o.write(json.dumps(result))

inputs:
  - id: input_file
    type: File
  - id: goldstandard
    type: File
  - id: check_validation_finished
    type: boolean?

outputs:
  - id: results
    type: File
    outputBinding:
      glob: results.json
  - id: status
    type: string
    outputBinding:
      glob: results.json
      outputEval: $(JSON.parse(self[0].contents)['submission_status'])
      loadContents: true

baseCommand: python
arguments:
  - valueFrom: score.py
  - prefix: -f
    valueFrom: $(inputs.input_file.path)
  - prefix: -g
    valueFrom: $(inputs.goldstandard.path)
  - prefix: -r
    valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: python:3.9.1-slim-buster
