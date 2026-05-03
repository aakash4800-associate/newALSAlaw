#!/bin/bash

# Find node in all common macOS locations
NODE=$(find /opt/homebrew/bin /usr/local/bin /usr/bin "$HOME/.nvm/versions/node" "$HOME/.nodenv/shims" /usr/local/n/versions/node -name "node" -type f 2>/dev/null | head -1)

if [ -z "$NODE" ]; then
  echo ""
  echo "❌ Node.js is not installed on this machine."
  echo "   Please install it from https://nodejs.org and try again."
  echo ""
  read -p "Press Enter to exit..."
  exit 1
fi

NPM="$(dirname "$NODE")/npm"
echo "✅ Found Node.js at: $NODE"
echo ""

cd "$(dirname "$0")"
"$NPM" install && "$NPM" run dev
