#!/bin/bash

echo "🔧 Fixing Git Issues..."

# Remove node_modules from git tracking
echo "📁 Removing node_modules from git tracking..."
git rm -r --cached frontend/node_modules 2>/dev/null || echo "node_modules not tracked"

# Clean git index
echo "🧹 Cleaning git index..."
git reset --hard HEAD

# Add .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production builds
/build
/dist

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Training data (large files)
training_data/
*.model
*.bin
*.safetensors

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
EOF
fi

# Force add .gitignore
git add .gitignore

echo "✅ Git cleanup complete!"
echo "🚀 Now you can run: git status" 