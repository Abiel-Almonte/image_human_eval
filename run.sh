#!/bin/bash

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

echo "Running streamlit client ..."
    pip3 install -U -quiet pandas
    pip3 install -U --quiet streamlit
    streamlit run ./utils/rate.py
