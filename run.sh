#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed on this system."
    echo "Please install Python 3 before running this script."
    exit 1
fi

output_images_src="./images/output_images"

if [ -d "$output_images_src" ]; then
    echo "Processing output images in '$output_images_src'..."

    find "$output_images_src" -mindepth 1 -type d -print0 | while IFS= read -r -d '' folder; do
        foldername=$(basename "$folder")
        output_file="./data/image_name_output_${foldername}.txt"

        > "$output_file"

        find "$folder" -type f \( -iname "*.png" -o -iname "*.jpg" \) | sort >> "$output_file"

        echo "Generated $output_file"
    done
else
    echo "Warning: '$output_images_src' does not exist. Skipping output images."
fi

input_images_src="./images/input_images"
input_output_file="./data/image_name_input.txt"

if [ -d "$input_images_src" ]; then
    echo "Processing input images in '$input_images_src'..."

    > "$input_output_file"

    find "$input_images_src" -mindepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" \) | sort >> "$input_output_file"

    echo "Generated $input_output_file"
else
    echo "Warning: '$input_images_src' does not exist. Skipping input images."
fi

echo "Populating Prompts_Final_Categories_with_Image_Paths.csv ..."
    python3 ./utils/populate_df.py

rm ./data/*.txt
echo "All processing complete."

if [ -z "$VIRTUAL_ENV" ]; then
    echo "No active virtual environment detected."

    if [ -d ".venv" ]; then
        echo "Found existing virtual environment in '.venv'. Activating it..."
        source .venv/bin/activate
    else
        echo "No virtual environment found. Creating one in '.venv'..."
        if ! python3 -m venv .venv; then
            echo "Error: Failed to create a virtual environment. Please ensure python3-venv is installed."

            read -p "Do you want to proceed with the global Python environment? (y/n): " user_choice
            if [[ "$user_choice" =~ ^[Yy]$ ]]; then
                echo "Proceeding with global Python environment. Note: This may cause dependency conflicts."
            else
                echo "Exiting. Please install python3-venv and re-run the script."
                exit 1
            fi
        else
            echo "Virtual environment created successfully. Activating it..."
            source .venv/bin/activate
        fi
    fi
else
    echo "Already inside a virtual environment: $VIRTUAL_ENV"
fi

echo "Installing dependencies..."
pip install --quiet -r requirements.txt

echo "Starting the Streamlit application..."
streamlit run ./utils/rate.py
