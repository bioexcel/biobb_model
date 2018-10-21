#!/usr/bin/env bash

BIOBB_MODEL=$HOME/projects/biobb_model/biobb_model
cwltool $BIOBB_MODEL/cwl/model/mutate.cwl $BIOBB_MODEL/cwl/test/model/mutate.yml
cwltool $BIOBB_MODEL/cwl/model/fix_side_chain.cwl $BIOBB_MODEL/cwl/test/model/fix_side_chain.yml
