#!/bin/bash

# Define variables
RELEASES_DIR="releases"
REPO_URL="https://github.com/tobytwigger/when-is-bins.git"
CURRENT_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET_DIR="$RELEASES_DIR/$CURRENT_TIME"
CURRENT_DIR="$(pwd)/when-is-bins"

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

# Stop supervisor
echo "Stopping supervisor..."
sudo supervisorctl stop all

# Move files to the 'current' directory
mkdir -p "$CURRENT_DIR/when-is-bins-new"
cp -r "$TARGET_DIR/js/.output" "$CURRENT_DIR/when-is-bins-new/js"
cp -r "$TARGET_DIR/python" "$CURRENT_DIR/python"

mv "$CURRENT_DIR/when-is-bins" "$CURRENT_DIR/when-is-bins-old"
mv "$CURRENT_DIR/when-is-bins-new" "$CURRENT_DIR/when-is-bins"

# Remove the timestamped directory
echo "Removing $TARGET_DIR..."
sudo rm -rf "$TARGET_DIR"

# Set up new supervisor scripts
echo "Setting up supervisor..."
sudo cp "$TARGET_DIR/scripts/supervisor/bins.conf" /etc/supervisor/conf.d/bins.conf
sudo supervisorctl reread
sudo supervisorctl update

# Restart supervisor
echo "Restarting supervisor..."
sudo supervisorctl start all

echo "Script completed successfully."