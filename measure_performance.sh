#!/bin/bash

# Root directory where DayXX folders are located
ROOT_DIR="$(pwd)"

# Prepare Analytics.md file in the root directory
ANALYTICS_FILE="Analytics.md"
echo "# Performance Analytics" > $ANALYTICS_FILE

# Function to measure and append execution time to the analytics file
measure_execution_time() {
    local day=$1
    local language=$2
    local script_dir=$3
    local script_name=$4
    local runner=$5

    echo "Running $language script for $day: $runner $script_dir$script_name"

    cd "$script_dir"
    if [ -f "$script_name" ] || [ "$language" == "Rust" ]; then
        exec 3>&1 4>&2
        TIME_RESULT=$( { time $runner $script_name 1>&3 2>&4; } 2>&1 )
        EXEC_STATUS=$?
        exec 3>&- 4>&-

        if [ $EXEC_STATUS -eq 0 ]; then
            real_time=$(echo "$TIME_RESULT" | grep real | awk '{print $2}')
            user_time=$(echo "$TIME_RESULT" | grep user | awk '{print $2}')
            sys_time=$(echo "$TIME_RESULT" | grep sys | awk '{print $2}')

            echo "| $language | Success | $real_time | $user_time | $sys_time |" >> "$ROOT_DIR/$ANALYTICS_FILE"
        else
            echo "| $language | Failed | - | - | - |" >> "$ROOT_DIR/$ANALYTICS_FILE"
            echo "Warning: $language script for $day failed with status $EXEC_STATUS"
        fi
    else
        echo "| $language | Not Found or Not Executable | - | - | - |" >> "$ROOT_DIR/$ANALYTICS_FILE"
        echo "Warning: $language script for $day not found or not executable"
    fi
    cd "$ROOT_DIR"
}

# Loop through each DayXX folder
for day_folder in $ROOT_DIR/Day*/; do
    day=$(basename "$day_folder")
    echo "" >> $ANALYTICS_FILE
    echo "## $day" >> $ANALYTICS_FILE
    echo "| Language | Status | Real Time | User Time | Sys Time |" >> $ANALYTICS_FILE
    echo "| --- | --- | --- | --- | --- |" >> $ANALYTICS_FILE

    # Python
    measure_execution_time "$day" "Python" "${day_folder}python/" "solution2.py" "python3"

    # Rust
    RUST_PROJECT_DIR="${day_folder}rust"
    if [ ! -d "$RUST_PROJECT_DIR" ]; then
        echo "Rust project directory not found for $day."
        echo "| Rust | Directory Not Found | - | - | - |" >> "$ROOT_DIR/$ANALYTICS_FILE"
    else
        if [ ! -f "$RUST_PROJECT_DIR/target/release/rust" ]; then
            echo "Compiled Rust binary not found. Building the Rust project in $RUST_PROJECT_DIR..."
            (cd "$RUST_PROJECT_DIR" && cargo build --release)
        fi
        measure_execution_time "$day" "Rust" "$RUST_PROJECT_DIR" "" "cargo run --release" 
    fi

    # JavaScript
    measure_execution_time "$day" "JavaScript" "${day_folder}js/" "solution.js" "node"

    # TypeScript
    measure_execution_time "$day" "TypeScript" "${day_folder}ts/" "solution.ts" "ts-node"

    echo "Processed $day"
done

echo "Performance measurement complete. Results are saved in $ANALYTICS_FILE."
