import os
import sys
import subprocess
import logging
import secrets
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import tempfile
import shutil


LOG_FILE = Path.home() / "secure_automation.log"
AUDIT_FILE = Path.home() / "secure_automation_audit.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SecurityError(Exception):
    pass


class SecureAutomation:

    def __init__(self):
        self.temp_dir: Optional[Path] = None
        self._setup_temp_dir()

    def _setup_temp_dir(self) -> None:
        try:
            self.temp_dir = Path(tempfile.mkdtemp(prefix='secure_auto_'))
            os.chmod(self.temp_dir, 0o700)
            logger.info(f"Created secure temp directory: {self.temp_dir}")
        except Exception as e:
            raise SecurityError("Cannot initialize secure environment") from e

    def cleanup(self) -> None:
        if self.temp_dir and self.temp_dir.exists():
            for file_path in self.temp_dir.rglob('*'):
                if file_path.is_file():
                    self._secure_delete(file_path)
            shutil.rmtree(self.temp_dir)
            logger.info("Secure cleanup completed")

    def _secure_delete(self, file_path: Path, passes: int = 3) -> None:
        if not file_path.exists():
            return

        file_size = file_path.stat().st_size

        for _ in range(passes):
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_size))
                f.flush()

        with open(file_path, 'wb') as f:
            f.write(b'\x00' * file_size)
            f.flush()

        file_path.unlink()

    def validate_path(self, path: str, allowed_base: Optional[Path] = None) -> Path:
        resolved = Path(path).resolve()

        if '..' in str(path):
            raise SecurityError("Path traversal detected")

        if allowed_base:
            allowed_base = allowed_base.resolve()
            resolved.relative_to(allowed_base)

        return resolved

    def generate_secure_token(self, length: int = 32) -> str:
        return secrets.token_hex(length)

    def hash_data(self, data: str, algorithm: str = 'sha256') -> str:
        hasher = hashlib.new(algorithm)
        hasher.update(data.encode('utf-8'))
        return hasher.hexdigest()

    def execute_command(
        self,
        command: list,
        timeout: int = 300,
        allowed_commands: Optional[set] = None
    ) -> Dict[str, Any]:

        if not command or not isinstance(command, list):
            raise SecurityError("Command must be a non-empty list")

        cmd_name = command[0]

        if allowed_commands and cmd_name not in allowed_commands:
            raise SecurityError(f"Command '{cmd_name}' not allowed")

        logger.info(f"Executing command: {cmd_name}")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }

    def write_secure_file(
        self,
        file_path: Path,
        content: str,
        permissions: int = 0o600
    ) -> None:

        temp_path = self.temp_dir / f"temp_{secrets.token_hex(8)}"

        with open(temp_path, 'w') as f:
            f.write(content)

        os.chmod(temp_path, permissions)
        temp_path.replace(file_path)

        logger.info(f"Securely wrote file: {file_path}")

    def read_secure_file(self, file_path: Path) -> str:
        validated_path = self.validate_path(str(file_path))

        if not validated_path.exists():
            raise SecurityError("File does not exist")

        with open(validated_path, 'r') as f:
            return f.read()

    def audit_log(self, action: str, details: Dict[str, Any]) -> None:

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "details": details,
            "session_id": self.generate_secure_token(16)
        }

        with open(AUDIT_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

        logger.info("Audit log entry created")


def main():
    print("Secure Automation Script (Android Version)")
    print("=" * 50)

    automation = SecureAutomation()

    print("\n1. Secure Token Generation:")
    token = automation.generate_secure_token()
    print("Generated token:", token[:16], "...")

    print("\n2. Secure Hashing:")
    print("SHA-256:",
          automation.hash_data("sensitive_data_123"))

    print("\n3. Path Validation:")
    try:
        automation.validate_path("../../../etc/passwd")
    except SecurityError as e:
        print("Blocked traversal:", e)

    print("\n4. Secure Command Execution:")
    allowed = {"echo", "pwd", "date"}
    result = automation.execute_command(
        ["echo", "Hello from Termux"],
        allowed_commands=allowed
    )
    print(result["stdout"].strip())

    print("\n5. Audit Logging:")
    automation.audit_log("test_run", {"status": "success"})
    print("Audit log written.")

    automation.cleanup()


if __name__ == "__main__":
    main()