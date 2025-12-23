site
====

# Disposable Email Domains List

This repository contains a comprehensive list of disposable/temporary email domains commonly used by temporary email services.

## Files

- **disposable_domains.py**: Python module containing the `DISPOSABLE_DOMAINS` set with 687+ disposable email domains
- **disposable_domains.txt**: Plain text file with one domain per line (sorted alphabetically)

## Usage

### Python

```python
from disposable_domains import DISPOSABLE_DOMAINS, is_disposable, get_disposable_domains_list

# Check if an email uses a disposable domain
if is_disposable("test@mailinator.com"):
    print("This is a disposable email!")

# Get the set of all disposable domains
all_domains = DISPOSABLE_DOMAINS

# Get a sorted list of all domains
sorted_domains = get_disposable_domains_list()
```

### Text File

The `disposable_domains.txt` file can be used directly by any application:

```bash
# Count total domains
wc -l disposable_domains.txt

# Search for a specific domain
grep "mailinator" disposable_domains.txt

# Use in your application
cat disposable_domains.txt
```

## Coverage

The list includes domains from major disposable email services:

- **Temporary email services**: 10minutemail, tempmail, temp-mail, etc.
- **Guerrilla mail services**: guerrillamail, sharklasers, grr.la
- **Mailinator and variants**: mailinator, mailinator2, mailinator3
- **Trash/throwaway services**: trashmail, throwaway, yopmail
- **Burner email services**: burnermail, spamgourmet, spambox
- **German disposable services**: wegwerfmail, wegwerfemail, etc.
- **French disposable services**: jetable, yopmail.fr, etc.
- And 600+ more domains

## Total Domains

Currently includes **687 disposable email domains**.

## Maintenance

This list is compiled from various sources and includes the most commonly used disposable email services. The list can be updated by editing the `DISPOSABLE_DOMAINS` set in `disposable_domains.py` and regenerating the text file:

```bash
python3 -c "from disposable_domains import get_disposable_domains_list; print('\n'.join(get_disposable_domains_list()))" > disposable_domains.txt
```