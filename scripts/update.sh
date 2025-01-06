#!/bin/bash

# Define variables
RELEASES_DIR="releases"
REPO_URL="git@github.com:tobytwigger/when-is-bins"
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