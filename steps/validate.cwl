#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Validate predictions file

requirements:
- class: InlineJavascriptRequirement
  
inputs:
- id: input_file
  type: File
- id: goldstandard
  type: File
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

baseCommand: ["python3", "/usr/local/bin/validate.py"]
arguments:
- prefix: -s
  valueFrom: $(inputs.input_file)
- prefix: -g
  valueFrom: $(inputs.goldstandard)
- prefix: -e
  valueFrom: $(inputs.entity_type)
- prefix: -r
  valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn32407772/valid-repo:latest
