#!/bin/bash

# Function to create a backup
create_backup() {
    local file="$1"
    local backup_file="$file.bak"
    cp "$file" "$backup_file"
    echo "Backup created: $backup_file"
}

# Check if no arguments are provided
if [ $# -eq 0 ]; then
    # Backup files fisj and dpg
    create_backup "./glossary.json"
    create_backup "./highScore.json"
    exit 0
fi

# Check if an argument is provided
if [ $# -eq 1 ]; then
    file="$1"

    # Check if the file exists
    if [ ! -f "$file" ]; then
        echo "File $file does not exist."
        exit 1
    fi

    # Create a backup of the provided file
    create_backup "$file"
else
    echo "Usage: $0 [<filename>]"
    exit 1
fi

