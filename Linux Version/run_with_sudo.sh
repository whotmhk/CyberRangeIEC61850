#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <script_path>"
    exit 1
fi

script_path="$1"
script_name=$(basename "$script_path")

# Match the script name and execute accordingly
case "$script_name" in
    GooseSniff.py|GooseAttack.py)
        sudo python3 "$script_path"
        ;;
    Publisher)
        sudo "$script_path"
        ;;
    *)
        python3 "$script_path"
        ;;
esac
