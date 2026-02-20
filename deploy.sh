#!/bin/bash
# Render Deployment Quick Start Script
# Run this before pushing to Render

set -e

echo "🚀 Ethereal Jewelry - Render Deployment Setup"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual values:"
    echo "   - SECRET_KEY (generate: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
    echo "   - DATABASE_URL (from your database provider)"
    echo "   - EMAIL credentials"
    echo "   - ALLOWED_HOSTS and domain names"
fi

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
echo "👤 Would you like to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review and update .env file with your actual values"
echo "2. Test locally: python manage.py runserver"
echo "3. Commit changes: git add . && git commit -m 'Ready for Render deployment'"
echo "4. Push to Render: git push origin main"
echo ""
echo "📖 For more details, see DEPLOYMENT_GUIDE.md"
