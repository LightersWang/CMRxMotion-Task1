#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Score predictions file

requirements:
  - class: InlineJavascriptRequirement

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

baseCommand: ["python3", "/usr/local/bin/score.py"]
arguments:
  - prefix: -f
    valueFrom: $(inputs.input_file.path)
  - prefix: -g
    valueFrom: $(inputs.goldstandard.path)
  - prefix: -r
    valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn32407772/valid-repo:latest