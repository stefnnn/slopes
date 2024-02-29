from mountaineer import ConfigBase
from mountaineer.database import DatabaseConfig
from pydantic_settings import SettingsConfigDict
from .plugins.auth.config import AuthConfig

class AppConfig(ConfigBase, DatabaseConfig, AuthConfig):

    model_config = SettingsConfigDict(env_file=(".env",))