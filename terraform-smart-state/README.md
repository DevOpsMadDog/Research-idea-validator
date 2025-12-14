# Terraform Smart State (TSS)

A powerful companion tool for Terraform that enhances state management, improves plan visualization, and provides comprehensive tracking of apply operations—especially useful for handling partial failures.

## 🎯 Key Features

### 1. **Enhanced State Management**
- Add custom metadata to Terraform resources
- Track resource creation timestamps and status
- Maintain enhanced state files with additional context

### 2. **Beautiful Plan Visualization**
- Color-coded, grouped plan output that's easy to read
- Group changes by action (create, update, delete, replace)
- Group changes by provider
- Dependency graph visualization
- Summary statistics

### 3. **Comprehensive Apply Tracking**
- Track apply operations in real-time
- Handle partial failures gracefully
- See **all** resources (succeeded, failed, pending) in one view
- Never miss what was created when apply fails mid-way
- Detailed error reporting for failed resources

### 4. **Partial Failure Recovery**
- Clear visibility into what succeeded vs failed
- Track multiple apply attempts
- Comprehensive status reports
- Easy identification of resources that need attention

## 🚀 Installation

```bash
pip install -r requirements.txt
pip install -e .
```

Or install directly:
```bash
pip install terraform-smart-state
```

## 📖 Usage

### Visualize Terraform Plan

Make Terraform plans readable and organized:

```bash
# Generate and visualize plan
tss visualize-plan --generate

# Or visualize existing plan file
tss visualize-plan --plan-file plan.json
```

**Output includes:**
- Summary statistics
- Changes grouped by action (create/update/delete/replace)
- Changes grouped by provider
- Dependency information

### Track Apply Operations

Track your apply operations to never lose sight of what's happening:

```bash
# Start tracking and run apply
tss apply --generate --auto-apply

# Or track manually (run terraform apply separately)
tss apply --generate
terraform apply
tss status
```

### Check Apply Status

After an apply (successful or failed), see comprehensive status:

```bash
# Show status of current apply session
tss status

# Generate detailed report
tss report

# Generate JSON report
tss report --format json
```

### Enhance State Files

Add metadata to your Terraform state:

```bash
tss enhance-state --state-file terraform.tfstate --output terraform.enhanced.tfstate
```

## 🎨 Example Output

### Plan Visualization

```
┌─────────────────────────────────────────┐
│ Plan Summary                            │
├─────────────────────────────────────────┤
│ Total Changes: 15                       │
│ To Create: 8                            │
│ To Update: 3                            │
│ To Delete: 2                            │
│ To Replace: 2                           │
│ Providers: aws, kubernetes             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ + CREATE (8 resources)                                     │
├─────────────────────────────────────────────────────────────┤
│ Resource Address    │ Type              │ Provider │ ...  │
│ aws_instance.web    │ aws_instance      │ aws      │ ...  │
│ aws_s3_bucket.data  │ aws_s3_bucket     │ aws      │ ...  │
└─────────────────────────────────────────────────────────────┘
```

### Apply Status

```
┌─────────────────────────────────────────┐
│ Apply Status                            │
├─────────────────────────────────────────┤
│ Session ID: 2024-01-15T10:30:00         │
│ Started: 2024-01-15T10:30:00           │
│                                         │
│ Progress: 73.3%                         │
│ ✓ Succeeded: 11                        │
│ ✗ Failed: 2                            │
│ ⏳ Pending: 2                           │
│ Total: 15                               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ❌ Failed Resources (2)                 │
├─────────────────────────────────────────┤
│ Resource Address    │ Error             │
│ aws_instance.db     │ Instance type...  │
│ aws_s3_bucket.logs  │ Bucket name...    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ✅ Succeeded Resources (11)             │
├─────────────────────────────────────────┤
│ Resource Address    │ Completed At      │
│ aws_instance.web    │ 2024-01-15T10:31  │
│ aws_s3_bucket.data  │ 2024-01-15T10:32  │
└─────────────────────────────────────────┘
```

## 🔧 How It Solves Your Problems

### Problem 1: Terraform Plan is Hard to Read
**Solution:** `tss visualize-plan` provides:
- Color-coded output
- Grouped by action and provider
- Clear summary statistics
- Dependency visualization

### Problem 2: Missing Things in Plan Output
**Solution:** Enhanced visualization shows:
- All changes in organized tables
- Grouped views (by action, by provider)
- Dependency relationships
- Summary statistics

### Problem 3: Partial Apply Failures
**Solution:** `tss apply` and `tss status` provide:
- Complete tracking of all resources
- Clear separation of succeeded/failed/pending
- Detailed error messages for failures
- Progress tracking
- Session persistence across re-runs

### Problem 4: Only Seeing Failed Resources on Re-run
**Solution:** Comprehensive status shows:
- **All** resources: succeeded, failed, and pending
- Historical tracking across multiple apply attempts
- Clear identification of what needs fixing
- Complete context in one view

## 📁 Project Structure

```
terraform-smart-state/
├── terraform_smart_state/
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── state_parser.py     # State file parsing
│   ├── plan_parser.py      # Plan output parsing
│   ├── apply_tracker.py    # Apply operation tracking
│   └── visualizer.py       # Rich output formatting
├── requirements.txt
├── setup.py
└── README.md
```

## 🛠️ Development

```bash
# Install in development mode
pip install -e .

# Run tests (when available)
pytest

# Run CLI
tss --help
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## ⚠️ Notes

- This tool reads Terraform state and plan files but does not modify Terraform's core functionality
- Always backup your state files before using enhanced state features
- The apply tracker creates a `.terraform-apply-session.json` file to track operations
- Works with Terraform 0.12+ (JSON plan format)
