#!/bin/bash
# AWS Lambda Container Layer Provisioner for PocketGull Font Superfamily
# Configures system fonts for headless Chromium (Puppeteer/Playwright), WeasyPrint, and LibreOffice on AWS Lambda.

set -euo pipefail

LAYER_DIR="pocketgull-fonts-layer"
FONT_DIR="${LAYER_DIR}/fonts"

echo "📦 Creating AWS Lambda font layer structure..."
rm -rf "${LAYER_DIR}" pocketgull-lambda-fonts.zip
mkdir -p "${FONT_DIR}"

echo "🚚 Copying production TrueType binaries into font layer..."
cp fonts/ttf/PocketGull-Regular.ttf "${FONT_DIR}/"
cp fonts/ttf/PocketGull-Bold.ttf "${FONT_DIR}/"
cp fonts/ttf/PocketGull-Fineliner.ttf "${FONT_DIR}/"
cp fonts/ttf/PocketGullMono-Regular.ttf "${FONT_DIR}/"
cp fonts/ttf/PocketGullMono-Bold.ttf "${FONT_DIR}/"
cp fonts/ttf/PocketGull-Math.ttf "${FONT_DIR}/"
cp OFL.txt "${LAYER_DIR}/"

# Generate local fontconfig fonts.conf for Lambda runtime (/opt/fonts)
mkdir -p "${LAYER_DIR}/fontconfig"
cat << 'EOF' > "${LAYER_DIR}/fontconfig/fonts.conf"
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/opt/fonts</dir>
  <cachedir>/tmp/fonts-cache</cachedir>
  <config></config>
</fontconfig>
EOF

echo "🗜️ Compressing font layer into ZIP archive..."
(cd "${LAYER_DIR}" && zip -r ../pocketgull-lambda-fonts.zip .)

echo "✅ Generated pocketgull-lambda-fonts.zip successfully!"
echo "🚀 Deploy to AWS with:"
echo "   aws lambda publish-layer-version \\"
echo "     --layer-name pocketgull-fonts \\"
echo "     --description 'PocketGull clinical and monospace fonts for Lambda PDF & report generation' \\"
echo "     --zip-file fileb://pocketgull-lambda-fonts.zip \\"
echo "     --compatible-runtimes nodejs20.x nodejs22.x python3.11 python3.12 provided.al2023"
