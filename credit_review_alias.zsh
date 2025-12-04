# Add this function to your ~/.zshrc file to use the 'credit_review' command

credit_review() {
    # Path to the repository
    local REPO_DIR="/Users/tomery/Library/CloudStorage/OneDrive-Mobileye/Documents/Personal/Credit_Research/https:/github.com/TomerY-f/credit_follow_up.git"
    local BILLS_DIR="$REPO_DIR/bills"
    local INPUT_FILE="$1"

    # Check if argument is provided
    if [[ -z "$INPUT_FILE" ]]; then
        echo "Usage: credit_review <path_to_bill_file>"
        return 1
    fi

    # Check if input file exists
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "Error: File '$INPUT_FILE' not found."
        return 1
    fi

    # Create bills directory if it doesn't exist
    mkdir -p "$BILLS_DIR"

    local BASE_NAME=$(basename "$INPUT_FILE")
    local TARGET_FILE="$BILLS_DIR/$BASE_NAME"

    # Check if the input file and target file are the same (to avoid cp error on self-copy)
    if [[ "$INPUT_FILE" -ef "$TARGET_FILE" ]]; then
        echo "File is already in the bills directory. Skipping copy."
    else
        # Check if target already exists
        if [[ -f "$TARGET_FILE" ]]; then
            echo "Note: '$BASE_NAME' already exists in bills directory. Overwriting..."
        fi
        
        # Copy the file to bills directory
        cp "$INPUT_FILE" "$BILLS_DIR/"
        echo "Copied '$BASE_NAME' to $BILLS_DIR/"
    fi

    # Run the main script inside a subshell to avoid changing current directory
    (
        cd "$REPO_DIR"
        echo "Starting dashboard..."
        python main.py "bills/$BASE_NAME"
    )
}

