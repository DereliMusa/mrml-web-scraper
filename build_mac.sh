#!/bin/bash
# MacOS Build Script for Unisis Bot

echo "Setting up environment..."
cd "$(dirname "$0")"

# Clean previous builds and virtual environments
echo "Cleaning old files..."
rm -rf venv build dist "Unisis Bot.spec"

if [ ! -d "venv" ]; then
    /opt/homebrew/bin/python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

echo "Building macOS application..."
pyinstaller --noconfirm --onedir --windowed --name "Unisis Bot" --icon "app_icon.icns" "unisis_bot.py"

echo "Building DMG installer with create-dmg..."
mkdir -p dist/dmg_staging
cp -r "dist/Unisis Bot.app" dist/dmg_staging/

test -f "dist/Unisis_Bot.dmg" && rm "dist/Unisis_Bot.dmg"

create-dmg \
  --volname "Unisis Bot Setup" \
  --volicon "app_icon.icns" \
  --background "dmg_background.png" \
  --window-pos 200 120 \
  --window-size 400 244 \
  --icon-size 80 \
  --icon "Unisis Bot.app" 100 120 \
  --app-drop-link 300 120 \
  "dist/Unisis_Bot.dmg" \
  "dist/dmg_staging/"

rm -rf dist/dmg_staging
echo "Build complete. Check the 'dist' folder for 'Unisis_Bot.dmg'"
