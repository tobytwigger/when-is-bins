#!/bin/bash

# Define variables
RELEASES_DIR="releases"
REPO_URL="https://github.com/tobytwigger/when-is-bins.git"
CURRENT_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET_DIR="$RELEASES_DIR/$CURRENT_TIME"

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
if [ -f "./scripts/install/build-node.sh" ]; then
  echo "Running build-node.sh..."
  ./scripts/install/build-node.sh
  if [ $? -eq 0 ]; then
    echo "build-node.sh executed successfully."
  else
    echo "build-node.sh execution failed."
    exit 1
  fi
else
  echo "build-node.sh not found in $TARGET_DIR."
  exit 1
fi

# Call setup-supervisor.sh
if [ -f "./scripts/install/setup-supervisor.sh" ]; then
  echo "Running setup-supervisor.sh..."
  ./scripts/install/setup-supervisor.sh
  if [ $? -eq 0 ]; then
    echo "setup-supervisor.sh executed successfully."
  else
    echo "setup-supervisor.sh execution failed."
    exit 1
  fi
else
  echo "setup-supervisor.sh not found in $TARGET_DIR."
  exit 1
fi

echo "Script completed successfully."