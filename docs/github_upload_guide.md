# GitHub Upload Guide

## Step 1: Create GitHub Account
1. Go to https://github.com
2. Click "Sign up"
3. Fill in details
4. Verify email

## Step 2: Install Git
1. Download: https://git-scm.com/download/win
2. Install with default settings
3. Restart PowerShell

## Step 3: Create Repository
1. Login to GitHub
2. Click "+" (top right) → "New repository"
3. Fill in:
   - Name: `ai-customer-intelligence-system`
   - Description: "AI-Powered Customer Intelligence, Segmentation and Churn Prediction System"
   - Public
   - Check "Add a README file"
4. Click "Create repository"

## Step 4: Upload Files
Open PowerShell and run:

```powershell
# Go to project folder
cd "C:\Users\palak\OneDrive\Documents\major_project1"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Complete AI Customer Intelligence System"

# Connect to GitHub (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/ai-customer-intelligence-system.git

# Push
git branch -M main
git push -u origin main
```

## Step 5: Verify
1. Go to your GitHub repository
2. Check all files are uploaded
3. Add topics: machine-learning, python, react, fastapi, churn-prediction

## Step 6: Add Badges to README
Add these lines to top of README.md:

```markdown
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB)](https://reactjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## Common Issues

### Issue: "remote origin already exists"
Solution: `git remote remove origin`

### Issue: "nothing to commit"
Solution: `git add .` then `git commit -m "message"`

### Issue: Large files
Solution: Add to .gitignore:
```
backend/venv/
backend/customer_intelligence.db
backend/ml/models/*.pkl
node_modules/
```

## After Upload
1. Add topics/tags
2. Add description
3. Add website URL (if deployed)
4. Star your own repo
5. Share on LinkedIn
