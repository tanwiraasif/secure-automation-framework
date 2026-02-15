# secure-automation-framework
Security-focused Python automation framework demonstrating defensive programming practices, secure file handling, subprocess allowlisting, and structured audit logging.

## 🔐 Overview

This project demonstrates how to build automation scripts securely using:

- Secure temporary directory handling
- Path traversal protection
- Safe subprocess execution with allowlisting
- Cryptographically secure token generation
- SHA-256 hashing
- Structured audit logging
- Secure file writing with restricted permissions
- Secure cleanup procedures

This is a demonstration framework intended for learning and portfolio purposes.

---

## 🚀 Features

### 1. Secure Temporary Workspace
Creates a restricted-permission temporary directory for isolated operations.

### 2. Path Traversal Protection
Prevents directory traversal attacks such as:

### 3. Safe Command Execution
- Uses subprocess with list arguments (prevents shell injection)
- Optional command allowlist
- Timeout protection
- Structured output

### 4. Secure Token Generation
Uses Python's `secrets` module for cryptographically secure tokens.

### 5. Secure Hashing
Implements SHA-256 hashing using `hashlib`.

### 6. Secure File Operations
- Atomic file writing
- Restricted permissions (0o600)
- Controlled file reading

### 7. Audit Logging
Structured JSON audit logs including:
- Timestamp (UTC)
- Action name
- Details
- Session ID

### 8. Secure Cleanup
Overwrites temporary files before deletion.

---

## 🛠 Requirements

- Python 3.8+

No external libraries required.

---

## ▶️ How to Run

pkg update
pkg upgrade
pkg install python
nano secure_automation.py
python secure_automation.py
