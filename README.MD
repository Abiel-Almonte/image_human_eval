# How to Use

This guide provides instructions for setting up and running the project on Ubuntu/Debian, macOS, and Windows systems.

## Prerequisites

### Common Requirements
- Python 3.11 or higher
- Git
- Bash shell

### System-Specific Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip
```

#### macOS
First install Homebrew if you haven't already:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Git, Python, and ensure Bash is available:
```bash
brew install git python bash
```

#### Windows
- Install Python 3.11 from the Microsoft Store
- Install Git Bash from [https://git-scm.com/downloads](https://git-scm.com/downloads)

## Installation and Setup

> [!IMPORTANT]  
>  **Windows Users**: Always run these commands through Git Bash, not Command Prompt or PowerShell.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Abiel-Almonte/image_human_eval.git
   cd ./image_human_eval
   ```

2. **Run the Project**
   ```bash
   ./run.sh
   ```

## Troubleshooting

If you encounter permission issues with run.sh:
```bash
chmod +x run.sh
```

## Additional Notes

- Windows users: Always run the script through Git Bash
- macOS users: While the default shell is Zsh, the script will automatically use Bash due to the shebang line
- The script will automatically create a virtual environment
- The script requires Bash (`#!/bin/bash`)
- Just ensure the file has execute permissions (`chmod +x run.sh`)