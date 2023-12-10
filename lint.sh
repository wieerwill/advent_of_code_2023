#!/bin/bash

# Define paths to the directories for each language
PYTHON_DIRS="Day*/python"
JAVASCRIPT_DIRS="Day*/javascript"
TYPESCRIPT_DIRS="Day*/typescript"
RUST_DIRS="Day*/rust"

# File to store linting results
LINTING_MD="Linting.md"
> "$LINTING_MD"  # Clear the file contents

# Prettify and Lint Python files
prettify_lint_python() {
    echo "Prettifying and Linting Python files..."
    for dir in $PYTHON_DIRS; do
        if [ -d "$dir" ]; then
            echo "# Prettifying and Linting $dir" >> "$LINTING_MD"
            # Prettify
            black "$dir" >> "$LINTING_MD" 2>&1
            # Lint
            flake8 "$dir" --count --select=E9,F63,F7,F82 --show-source --statistics >> "$LINTING_MD" 2>&1
            flake8 "$dir" --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics >> "$LINTING_MD" 2>&1
        fi
    done
}

# Prettify and Lint JavaScript files
prettify_lint_js() {
    echo "Prettifying and Linting JavaScript files..."
    for dir in $JAVASCRIPT_DIRS; do
        if [ -d "$dir" ]; then
            echo "# Prettifying and Linting $dir" >> "$LINTING_MD"
            # Prettify
            (cd "$dir" && npx prettier --write .) >> "$LINTING_MD" 2>&1
            # Lint
            (cd "$dir" && npm run lint) >> "$LINTING_MD" 2>&1
        fi
    done
}

# Prettify and Lint TypeScript files
prettify_lint_ts() {
    echo "Prettifying and Linting TypeScript files..."
    for dir in $TYPESCRIPT_DIRS; do
        if [ -d "$dir" ]; then
            echo "# Prettifying and Linting $dir" >> "$LINTING_MD"
            # Prettify
            (cd "$dir" && npx prettier --write .) >> "$LINTING_MD" 2>&1
            # Lint
            (cd "$dir" && npm run lint) >> "$LINTING_MD" 2>&1
        fi
    done
}

# Prettify and Lint Rust files
prettify_lint_rust() {
    echo "Prettifying and Linting Rust files..."
    for dir in $RUST_DIRS; do
        if [ -d "$dir" ]; then
            echo "# Prettifying and Linting $dir" >> "$LINTING_MD"
            # Prettify
            (cd "$dir" && cargo fmt) >> "$LINTING_MD" 2>&1
            # Lint
            (cd "$dir" && cargo clippy -- -D warnings) >> "$LINTING_MD" 2>&1
        fi
    done
}

# Run the prettifying and linting functions
prettify_lint_python
prettify_lint_js
prettify_lint_ts
prettify_lint_rust

# Run the performance measurement script
echo "Running performance measurement..."
chmod +x ./measure_performance.sh
./measure_performance.sh