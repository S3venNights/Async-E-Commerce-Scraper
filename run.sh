#!/bin/bash

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Colors for output
BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Starting Async E-Commerce Scraper ===${NC}"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment 'venv' not found.${NC}"
    echo -e "Please run 'python3 setup.py' first."
    exit 1
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Run the bot
echo -e "${GREEN}Scraper is launching...${NC}"
python3 src/main.py

# Deactivate venv on exit
deactivate