# Personal Data Security Project

This project implements secure handling of personal data with proper logging, database connectivity, and password encryption following security best practices.

## Overview

The project consists of two main modules:
- `filtered_logger.py`: Handles secure logging with PII filtering and database connectivity
- `encrypt_password.py`: Provides password hashing and validation functionality

## Features

### Secure Logging (`filtered_logger.py`)
- **Data Obfuscation**: Automatically filters sensitive fields in log messages
- **Custom Formatter**: RedactingFormatter class that extends logging.Formatter
- **Database Connectivity**: Secure connection to MySQL database using environment variables
- **PII Protection**: Identifies and protects 5 key PII fields (name, email, phone, ssn, password)

### Password Security (`encrypt_password.py`)
- **Password Hashing**: Uses bcrypt for secure password hashing with salt
- **Password Validation**: Validates passwords against stored hashes
- **Industry Standards**: Follows security best practices for password storage

## Requirements

- Ubuntu 18.04 LTS
- Python 3.7
- MySQL database
- Required Python packages:
  - `mysql-connector-python`
  - `bcrypt`

## Environment Variables

The following environment variables are used for database connectivity:

- `PERSONAL_DATA_DB_USERNAME`: Database username (default: "root")
- `PERSONAL_DATA_DB_PASSWORD`: Database password (default: "")
- `PERSONAL_DATA_DB_HOST`: Database host (default: "localhost")
- `PERSONAL_DATA_DB_NAME`: Database name

## Installation

1. Install required packages:
   \`\`\`bash
   pip3 install mysql-connector-python bcrypt
   \`\`\`

2. Set up environment variables:
   \`\`\`bash
   export PERSONAL_DATA_DB_USERNAME=your_username
   export PERSONAL_DATA_DB_PASSWORD=your_password
   export PERSONAL_DATA_DB_HOST=localhost
   export PERSONAL_DATA_DB_NAME=your_database
   \`\`\`

3. Make files executable:
   \`\`\`bash
   chmod +x filtered_logger.py encrypt_password.py
   \`\`\`

## Usage

### Running the Logger
\`\`\`bash
./filtered_logger.py
\`\`\`

### Using Password Functions
\`\`\`python
from encrypt_password import hash_password, is_valid

# Hash a password
password = "MySecurePassword"
hashed = hash_password(password)

# Validate a password
is_valid_password = is_valid(hashed, password)
\`\`\`

## Security Features

1. **PII Field Protection**: Automatically obfuscates sensitive fields including:
   - Name
   - Email
   - Phone number
   - Social Security Number (SSN)
   - Password

2. **Secure Database Connection**: Uses environment variables to avoid hardcoded credentials

3. **Password Security**: 
   - Salted password hashing using bcrypt
   - Secure password validation
   - No plain text password storage

4. **Logging Security**: 
   - Custom formatter prevents PII leakage in logs
   - Configurable redaction patterns
   - Structured logging format

## Code Style

- Follows pycodestyle (version 2.5) standards
- All functions include type annotations
- Comprehensive documentation for all modules, classes, and functions
- Proper error handling and security practices

## Database Schema

Expected `users` table structure:
\`\`\`sql
CREATE TABLE users (
    name VARCHAR(256),
    email VARCHAR(256),
    phone VARCHAR(16),
    ssn VARCHAR(16),
    password VARCHAR(256),
    ip VARCHAR(64),
    last_login TIMESTAMP,
    user_agent VARCHAR(512)
);
\`\`\`

## Testing

The project includes comprehensive testing capabilities:
- Unit tests for all functions
- Integration tests for database connectivity
- Security validation tests for password handling

## Contributing

When contributing to this project:
1. Follow the established code style
2. Include proper documentation
3. Add type annotations to all functions
4. Ensure all security practices are maintained
5. Test thoroughly before submitting changes

## License

This project is part of the ALX Backend User Data curriculum and follows educational use guidelines.

