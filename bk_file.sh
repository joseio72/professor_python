#!/bin/bash

# Check if an argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "File $1 does not exist."
    exit 1
fi

# Create a backup filename with .bak extension
backup_file="$1.bak"

# Copy the original file to the backup file
cp "$1" "$backup_file"

echo "Backup created: $backup_file"

