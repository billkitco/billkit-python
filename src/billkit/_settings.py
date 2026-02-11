from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class Settings:
    api_key: str | None = None
    base_url: str = "https://api.billkit.co/v1"

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "Settings":
        if env_file:
            dotenv_path = Path(env_file)
            if dotenv_path.exists():
                for line in dotenv_path.read_text().splitlines():
                    line = line.strip()
                    if line and "=" in line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        
        return cls(
            api_key=os.getenv("BILLKIT_SECRET_KEY"),
            base_url=os.getenv(
                "BILLKIT_BASE_URL",
                "https://api.billkit.co/v1"
            )
        )


# Module-level singleton
_settings: Settings | None = None


def get_settings(env_file: str | None = None) -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env(env_file)
    return _settings
