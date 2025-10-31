#!/usr/bin/env python3
"""
Setup script for Financial Analysis Dashboard
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False
    return True

def setup_gemini_api():
    """Guide user to set up Gemini API key"""
    print("\n" + "="*60)
    print("GEMINI API SETUP REQUIRED")
    print("="*60)
    print("To use the AI chatbot feature, you need to:")
    print("1. Go to https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Create a .env file in the project root")
    print("4. Add your API key to the .env file")
    print("\nExample .env file content:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    print("\nNote: The .env file should be in the same directory as app.py")
    print("="*60)

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("# Financial Analysis Dashboard Environment Variables\n")
            f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
        print("Created .env file - please update it with your actual API key")
    else:
        print(".env file already exists")

def main():
    print("Setting up Financial Analysis Dashboard...")
    print("="*50)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install packages manually.")
        return
    
    # Generate sample data
    print("\nGenerating sample financial data...")
    try:
        subprocess.check_call([sys.executable, "generate_synthetic_data.py"])
        print("Sample data generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error generating sample data: {e}")
    
    # Setup instructions
    setup_gemini_api()
    
    print("\nSetup completed!")
    print("\nTo run the application:")
    print("1. Update the Gemini API key in app.py")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\nHappy analyzing!")

if __name__ == "__main__":
    main()
