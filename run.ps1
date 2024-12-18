if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python 3 is not installed on this system."
    Write-Host "Please install Python 3 before running this script."
    exit 1
}

# Check for virtual environment
if (-not $env:VIRTUAL_ENV) {
    Write-Host "No active virtual environment detected."

    if (Test-Path ".venv") {
        Write-Host "Found existing virtual environment in '.venv'. Activating it..."
        . .\.venv\Scripts\activate
    } else {
        Write-Host "No virtual environment found. Creating one in '.venv'..."
        python -m venv .venv
        Write-Host "Activating the newly created virtual environment..."
        . .\.venv\Scripts\activate
    }
} else {
    Write-Host "Already inside a virtual environment: $env:VIRTUAL_ENV"
}

$output_images_src = "./images/output_images"

# Process output images
if (Test-Path $output_images_src) {
    Write-Host "Processing output images in '$output_images_src'..."

    Get-ChildItem -Path $output_images_src -Directory | ForEach-Object {
        $foldername = $_.Name
        $output_file = "./data/image_name_output_${foldername}.txt"

        # Create an empty file
        New-Item -ItemType File -Path $output_file -Force | Out-Null

        # Find all image files and append them to the output file
        Get-ChildItem -Path $_.FullName -Recurse -File |
        Where-Object { $_.Extension -match "(\.png|\.jpg)$" } |
        Sort-Object FullName |
        ForEach-Object { $_.FullName } >> $output_file

        Write-Host "Generated $output_file"
    }
} else {
    Write-Host "Warning: '$output_images_src' does not exist. Skipping output images."
}

$input_images_src = "./images/input_images"
$input_output_file = "./data/image_name_input.txt"

# Process input images
if (Test-Path $input_images_src) {
    Write-Host "Processing input images in '$input_images_src'..."

    # Create an empty file
    New-Item -ItemType File -Path $input_output_file -Force | Out-Null

    # Find all image files and append them to the input file
    Get-ChildItem -Path $input_images_src -Recurse -File |
    Where-Object { $_.Extension -match "(\.png|\.jpg)$" } |
    Sort-Object FullName |
    ForEach-Object { $_.FullName } >> $input_output_file

    Write-Host "Generated $input_output_file"
} else {
    Write-Host "Warning: '$input_images_src' does not exist. Skipping input images."
}

Write-Host "Populating Prompts_Final_Categories_with_Image_Paths.csv ..."
python ./utils/populate_df.py

# Clean up temporary files
Remove-Item "./data/*.txt" -Force
Write-Host "All processing complete."

# Install dependencies
Write-Host "Installing dependencies..."
pip install --quiet -r requirements.txt

# Start the Streamlit application
Write-Host "Starting the Streamlit application..."
streamlit run ./utils/rate.py