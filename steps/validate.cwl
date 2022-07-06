#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Validate predictions file

requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
    - entryname: validate.py
      entry: |
        #!/usr/bin python3
        import argparse
        import json
        try:
            import pandas
        except:
            import os
            os.system("pip3 install pandas")
            os.system("which python3")
        import pandas as pd
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--results", required=True, help="validation results")
        parser.add_argument("-e", "--entity_type", required=True, help="synapse entity type downloaded")
        parser.add_argument("-s", "--submission_file", help="Submission File")

        args = parser.parse_args()

        if args.submission_file is None:
            prediction_file_status = "INVALID"
            invalid_reasons = ['Expected FileEntity type but found ' + args.entity_type]
        else:
            required_shape = (160, 1)
            invalid_reasons = []
            prediction_file_status = "VALIDATED"
            try:
                submission_df = pd.read_csv(args.submission_file, index_col=0)
                if not (submission_df.shape == required_shape):
                    invalid_reasons.append(f"Submission csv is not in right shape (i.e. {required_shape})")
                    invalid_reasons.append(f"Actual shape is {submission_df.shape}")
                    prediction_file_status = "INVALID"
            except:
                invalid_reasons.append("Cannot open submission file with pandas.read_csv()")
                invalid_reasons.append(f"Path is {args.submission_file}")
                prediction_file_status = "INVALID"
        result = {'submission_errors': "\n".join(invalid_reasons),
                  'submission_status': prediction_file_status}
        with open(args.results, 'w') as o:
            o.write(json.dumps(result))

inputs:
  - id: input_file
    type: File?
  - id: entity_type
    type: string

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
  - id: invalid_reasons
    type: string
    outputBinding:
      glob: results.json
      outputEval: $(JSON.parse(self[0].contents)['submission_errors'])
      loadContents: true

baseCommand: python3
arguments:
  - valueFrom: validate.py
  - prefix: -s
    valueFrom: $(inputs.input_file)
  - prefix: -e
    valueFrom: $(inputs.entity_type)
  - prefix: -r
    valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: python:3.9.1-slim-buster
