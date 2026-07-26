#!/bin/bash
# Create new vault with Obsidian defaults
# Usage: ./create-vault.sh ~/path/to/new-vault [--plugins]

VAULT_DIR="${1:?Usage: $0 ~/path/to/new-vault [--plugins]}"
COPY_PLUGINS="${2:-}"
TEMPLATE="/home/ayyan/project/cortex-insight-analytics/Cortex-insight-analytics/.obsidian"
GLOBAL_DEFAULTS="$HOME/.config/obsidian-defaults"

if [ -d "$VAULT_DIR" ]; then
    echo "Error: $VAULT_DIR already exists"
    exit 1
fi

mkdir -p "$VAULT_DIR/.obsidian"

# Always copy general settings (editor, appearance, hotkeys)
cp "$TEMPLATE/app.json" "$VAULT_DIR/.obsidian/" 2>/dev/null
cp "$TEMPLATE/appearance.json" "$VAULT_DIR/.obsidian/" 2>/dev/null
cp "$TEMPLATE/hotkeys.json" "$VAULT_DIR/.obsidian/" 2>/dev/null
cp "$TEMPLATE/core-plugins.json" "$VAULT_DIR/.obsidian/" 2>/dev/null

# Only copy plugins if --plugins flag
if [ "$COPY_PLUGINS" = "--plugins" ]; then
    cp -r "$TEMPLATE/plugins" "$VAULT_DIR/.obsidian/"
    cp "$TEMPLATE/community-plugins.json" "$VAULT_DIR/.obsidian/" 2>/dev/null
    echo "Copied plugins"
fi

echo "Created vault: $VAULT_DIR"
