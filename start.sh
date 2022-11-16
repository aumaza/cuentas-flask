#!/bin/bash

DIRE=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

$DIRE
. venv/bin/activate
python3 main.py