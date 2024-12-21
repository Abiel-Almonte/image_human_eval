#!/bin/bash

check_python3() {
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is not installed. Please install it before running this script."
        exit 1
    fi
}

handle_venv() {
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "No active virtual environment detected."

        if [ -d ".venv" ]; then
            echo "Activating existing virtual environment..."

            if source .venv/Scripts/activate 2>/dev/null; then
                echo "Virtual environment activated successfully."
            elif source .venv/bin/activate 2>/dev/null; then
                echo "Virtual environment activated successfully."
            else
                echo "Error: Failed to activate virtual environment."
                exit 1
            fi

        else
            echo "Creating virtual environment in '.venv'..."

            if python3 -m venv .venv; then
                echo "Virtual environment created successfully."

                if source .venv/Scripts/activate 2>/dev/null; then
                    echo "Virtual environment activated successfully."
                elif source .venv/bin/activate 2>/dev/null; then
                    echo "Virtual environment activated successfully."
                else
                    echo "Error: Failed to activate virtual environment after creation."
                    exit 1
                fi

            else
                echo "Error: Failed to create virtual environment. Ensure 'python3-venv' is installed."
                read -p "Proceed with global Python environment? (y/n): " user_choice

                if [[ "$user_choice" =~ ^[Yy]$ ]]; then
                    echo "Proceeding with global Python environment."
                else
                    echo "Exiting."
                    exit 1
                fi
            fi
        fi
    else
        echo "Already inside a virtual environment: $VIRTUAL_ENV"
    fi
}

install_dependencies() {
    echo "Installing dependencies..."

    if pip install --quiet -r requirements.txt; then
        echo "Dependencies installed successfully."
    else
        echo "Error: Failed to install dependencies."
        exit 1
    fi
}

define_process_images() {
    local src_dir="$1"
    local output_file="$2"

    find "$src_dir" -type f \( -iname "*.png" -o -iname "*.jpg" \) > "$output_file"
}

process_images() {
    for folder in ./images/output_images/*/; do
      foldername=$(basename "$folder")
      define_process_images "$folder" "./data/image_name_output_${foldername}.txt"
    done
    
    define_process_images "./images/input_images" "./data/image_name_input.txt"
}

populate_csv() {
    echo "Populating Prompts_Final_Categories_with_Image_Paths.csv..."

    VENV_PYTHON=$(find $(pwd)/.venv -name python3 -o -name python | head -n 1)

    if "$VENV_PYTHON" ./utils/populate_df.py 2>/dev/null; then
        echo "CSV populated successfully using python virtual environment."
    elif python3 ./utils/populate_df.py 2>/dev/null; then
        echo "CSV populated successfully using python global environment."
    else
        echo "Error: Failed to populate CSV."
        exit 1
    fi
}

clean_up() {
    echo "Cleaning up temporary files..."
    rm -f ./data/*.txt
    echo "Temporary files removed."
}

start_streamlit() {
    echo "Starting the Streamlit application..."
    echo -e "\n" | streamlit run ./utils/rate.py
}

main() {
    check_python3
    handle_venv
    install_dependencies
    process_images
    populate_csv
    clean_up
    start_streamlit
}

main
