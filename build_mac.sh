#!/bin/bash
# MacOS Build Script for Unisis Bot

echo "Setting up environment..."
cd "$(dirname "$0")"

# Clean previous builds (keep venv so downloads don't repeat unnecessarily)
echo "Cleaning old files..."
rm -rf build dist "Unisis Bot.spec"

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
  --volname "Unisis Bot Kurulum" \
  --volicon "app_icon.icns" \
  --background "dmg_background.png" \
  --window-pos 200 120 \
  --window-size 800 538 \
  --icon-size 100 \
  --icon "Unisis Bot.app" 172 270 \
  --app-drop-link 628 270 \
  "dist/Unisis_Bot.dmg" \
  "dist/dmg_staging/"

rm -rf dist/dmg_staging
echo "Build complete. Check the 'dist' folder for 'Unisis_Bot.dmg'"
