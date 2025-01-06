#!/bin/bash

# Define variables
RELEASES_DIR="$(pwd)/releases"
REPO_URL="https://github.com/tobytwigger/when-is-bins.git"
CURRENT_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
CURRENT_TIME="2025-01-06_22-45-07"
TARGET_DIR="$RELEASES_DIR/$CURRENT_TIME"
CURRENT_DIR="$(pwd)"



# Create the 'releases' folder if it doesn't exist
if [ ! -d "$RELEASES_DIR" ]; then
  echo "Creating 'releases' directory..."
  mkdir "$RELEASES_DIR"
fi

# Clone the repository into the timestamped directory
echo "Cloning repository into $TARGET_DIR..."
git clone "$REPO_URL" "$TARGET_DIR"

if [ $? -eq 0 ]; then
  echo "Repository cloned successfully into $TARGET_DIR."
else
  echo "Failed to clone repository."
  exit 1
fi

# Change to the target directory
cd "$TARGET_DIR" || exit

# Call build-node.sh
cd js

npm install

npm run build

cd ../

cd python

# Remove .venv if exists
if [ -d ".venv" ]; then
  echo "Removing .venv directory..."
  rm -rf .venv
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3.12 -m venv .venv

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

# Exit the python directory
cd ../

# Stop supervisor
echo "Stopping supervisor..."
sudo supervisorctl stop all

echo "Copying supervisor config"
sudo cp "$TARGET_DIR/scripts/supervisor/bins.conf" /etc/supervisor/conf.d/bins.conf

# Move files to the 'current' directory
echo "Moving files to $CURRENT_DIR..."
mkdir -p "$CURRENT_DIR/when-is-bins-new"
cp -r "$TARGET_DIR/js/.output" "$CURRENT_DIR/when-is-bins-new/js"
cp -r "$TARGET_DIR/python" "$CURRENT_DIR/when-is-bins-new/python"

# move when-is-bins if exists
if [ -d "$CURRENT_DIR/when-is-bins" ]; then
  echo "Moving $CURRENT_DIR/when-is-bins to $CURRENT_DIR/when-is-bins-old..."
  mv "$CURRENT_DIR/when-is-bins" "$CURRENT_DIR/when-is-bins-old"
fi

# Rename the 'new' directory to 'current'
echo "Renaming $CURRENT_DIR/when-is-bins-new to $CURRENT_DIR/when-is-bins..."
mv "$CURRENT_DIR/when-is-bins-new" "$CURRENT_DIR/when-is-bins"

# Remove the timestamped directory
echo "Removing $TARGET_DIR..."
sudo rm -rf "$TARGET_DIR"

# Set up new supervisor scripts
echo "Setting up supervisor..."
sudo supervisorctl reread
sudo supervisorctl update

# Restart supervisor
echo "Restarting supervisor..."
sudo supervisorctl start all

echo "Script completed successfully."