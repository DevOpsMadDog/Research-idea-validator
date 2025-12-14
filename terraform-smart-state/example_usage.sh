#!/bin/bash
# Example usage script for Terraform Smart State

set -e

echo "=== Terraform Smart State - Example Usage ==="
echo ""

# Check if terraform is available
if ! command -v terraform &> /dev/null; then
    echo "⚠️  Terraform not found. Please install Terraform first."
    exit 1
fi

# Check if tss is installed
if ! command -v tss &> /dev/null; then
    echo "📦 Installing Terraform Smart State..."
    pip install -e .
fi

echo "1️⃣  Visualizing Terraform Plan"
echo "   Command: tss visualize-plan --generate"
echo "   This will generate a plan and show it in a beautiful, organized format"
echo ""

echo "2️⃣  Tracking Apply Operations"
echo "   Command: tss apply --generate --auto-apply"
echo "   This will track your apply and show comprehensive status"
echo ""

echo "3️⃣  Checking Apply Status"
echo "   Command: tss status"
echo "   Shows all resources: succeeded, failed, and pending"
echo ""

echo "4️⃣  Generating Reports"
echo "   Command: tss report"
echo "   Get detailed reports in table or JSON format"
echo ""

echo "✅ Setup complete! Try running 'tss --help' for more options"
