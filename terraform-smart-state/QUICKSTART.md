# Quick Start Guide

## Installation

```bash
cd terraform-smart-state
pip install -r requirements.txt
pip install -e .
```

## Common Use Cases

### 1. Make Terraform Plan Readable

Instead of scrolling through hundreds of lines of plan output:

```bash
# Old way (hard to read)
terraform plan

# New way (beautiful and organized)
tss visualize-plan --generate
```

**What you get:**
- Color-coded changes (green=create, yellow=update, red=delete)
- Grouped by action type
- Grouped by provider
- Summary statistics
- Dependency information

### 2. Track Apply Operations

Never lose track of what happened during apply:

```bash
# Start tracking
tss apply --generate --auto-apply

# Or track manually
tss apply --generate
terraform apply
tss status
```

**What you get:**
- Real-time progress tracking
- Complete list of succeeded resources
- Complete list of failed resources
- Detailed error messages
- Pending resources status

### 3. Handle Partial Failures

When `terraform apply` fails mid-way:

**Problem:** You only see the failed resources, not what succeeded.

**Solution:**
```bash
# After a failed apply
tss status

# You'll see:
# - All succeeded resources (even if apply failed overall)
# - All failed resources with errors
# - All pending resources
# - Progress percentage
```

### 4. Get Comprehensive Reports

```bash
# Table format (default)
tss report

# JSON format (for automation)
tss report --format json
```

## Workflow Example

```bash
# 1. Plan your changes
tss visualize-plan --generate

# 2. Review the beautiful output
#    - See what will be created/updated/deleted
#    - Check dependencies
#    - Review by provider

# 3. Apply with tracking
tss apply --generate --auto-apply

# 4. If it fails partially:
tss status  # See everything: succeeded + failed

# 5. Fix issues and re-apply
#    (tss will track the new attempt)

# 6. Get final report
tss report
```

## Key Benefits

✅ **Never miss what was created** - Even if apply fails, you see all succeeded resources  
✅ **Beautiful plan output** - Color-coded, grouped, easy to read  
✅ **Complete visibility** - See succeeded, failed, and pending resources in one view  
✅ **Better debugging** - Detailed error messages and resource status  
✅ **Progress tracking** - Know exactly how far your apply got  

## Tips

- Use `tss status` after any apply (successful or failed) to see comprehensive status
- The session file (`.terraform-apply-session.json`) persists across re-runs
- Use `tss clear-session` to start fresh
- Enhanced state files can be used for custom metadata tracking
