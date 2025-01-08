#!/bin/bash

# Define variables
RELEASES_DIR="$(pwd)/releases"
REPO_URL="https://github.com/tobytwigger/when-is-bins.git"
CURRENT_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
BUILD_DIR="$RELEASES_DIR/$CURRENT_TIME"
ROOT_DIR="$(pwd)"



# Create the 'releases' folder if it doesn't exist
if [ ! -d "$RELEASES_DIR" ]; then
  echo "Creating 'releases' directory..."
  mkdir "$RELEASES_DIR"
fi

# Clone the repository into the timestamped directory
echo "Cloning repository into $BUILD_DIR..."
git clone "$REPO_URL" "$BUILD_DIR"

if [ $? -eq 0 ]; then
  echo "Repository cloned successfully into $BUILD_DIR."
else
  echo "Failed to clone repository."
  exit 1
fi

# Change to the target directory
cd "$BUILD_DIR" || exit

# Call build-node.sh
cd js

npm update

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
sudo cp "$BUILD_DIR/scripts/supervisor/bins.conf" /etc/supervisor/conf.d/bins.conf

echo "Copying boot scripts"
sudo cp "$BUILD_DIR/scripts/boot/whenisbins.service" /etc/systemd/system/whenisbins.service

shopt -s dotglob

# Move files to the 'current' directory
echo "Moving files to $ROOT_DIR..."
cp -r "$BUILD_DIR" "$ROOT_DIR/when-is-bins-new"
rm -rf "$ROOT_DIR/when-is-bins-new/.git"
rm -rf "$ROOT_DIR/when-is-bins-new/.gitignore"
rm -rf "$ROOT_DIR/when-is-bins-new/.github"
#mkdir -p "$ROOT_DIR/when-is-bins-new"
#mkdir -p "$ROOT_DIR/when-is-bins-new/scripts"
#cp -r "$BUILD_DIR/js/.output" "$ROOT_DIR/when-is-bins-new/js"
#mkdir -p "$ROOT_DIR/when-is-bins-new/js/.drizzle"
#cp -r "$BUILD_DIR/js/server/database/migrations" "$ROOT_DIR/when-is-bins-new/js/.drizzle/migrations"
#cp -r "$BUILD_DIR/js/package.json" "$ROOT_DIR/when-is-bins-new/package.json"
#cp -r "$BUILD_DIR/js/package-lock.json" "$ROOT_DIR/when-is-bins-new/package-lock.json"
#cp -r "$BUILD_DIR/python" "$ROOT_DIR/when-is-bins-new/python"
#cp -r "$BUILD_DIR/scripts/update.sh" "$ROOT_DIR/when-is-bins-new/scripts/update.sh"
#cp -r "$BUILD_DIR/scripts/hostjs.sh" "$ROOT_DIR/when-is-bins-new/scripts/hostjs.sh"

shopt -u dotglob

# delete the old directory
if [ -d "$ROOT_DIR/when-is-bins" ]; then
  echo "Removing $ROOT_DIR/when-is-bins..."
  sudo rm -rf "$ROOT_DIR/when-is-bins"
fi


# Rename the 'new' directory to 'current'
echo "Renaming $ROOT_DIR/when-is-bins-new to $ROOT_DIR/when-is-bins..."
mv "$ROOT_DIR/when-is-bins-new" "$ROOT_DIR/when-is-bins"

# Remove the timestamped directory
echo "Removing $BUILD_DIR..."
sudo rm -rf "$BUILD_DIR"

# Make the scripts executable
echo "Making scripts executable..."
sudo chmod a+x "$ROOT_DIR/when-is-bins/python/src/main.py"
sudo chmod a+x "$ROOT_DIR/when-is-bins/python/src/api.py"
sudo chmod a+x "$ROOT_DIR/when-is-bins/scripts/hostjs.sh"
sudo chmod a+x "$ROOT_DIR/when-is-bins/scripts/boot/onboot.sh"

# Set up new supervisor scripts
echo "Setting up supervisor..."
sudo supervisorctl reread
sudo supervisorctl update

## Check the database exists
 if [ ! -f "$ROOT_DIR/database.sqlite" ]; then
   echo "Checking the database exists..."
   touch "$ROOT_DIR/database.sqlite"
 fi

# Reloading boot script directory
echo "Reloading boot scripts..."
sudo systemctl daemon-reload
sudo systemctl start whenisbins
sudo systemctl enable whenisbins

# Restart supervisor
echo "Restarting supervisor..."
sudo supervisorctl start all

echo "Script completed successfully."