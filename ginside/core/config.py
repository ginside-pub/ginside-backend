from pydantic import BaseSettings, PostgresDsn


class BaseSettingsConfig:
    env_file = '.env'


class DatabaseSettings(BaseSettings):
    test: bool = False
    host: str = '127.0.0.1'
    port: int = 5432
    username: str = 'ginside'
    password: str = 'ginside'
    database: str = 'ginside'
    url: PostgresDsn | None

    def get_url(self) -> str:
        if self.url is not None:
            return self.url

        return (
            f'postgresql://{self.username}:{self.password}'
            f'@{self.host}:{self.port}/{self.database}'
        )

    class Config(BaseSettingsConfig):
        env_prefix = 'ginside_database_'


class SecuritySettings(BaseSettings):
    secret_key: str = 'SECRET'
    hashing_algorithm: str = 'HS256'
    access_token_ttl: int = 30

    class Config(BaseSettingsConfig):
        env_prefix = 'ginside_security_'


class Settings(BaseSettings):
    debug: bool = True
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()

    class Config(BaseSettingsConfig):
        env_prefix = 'ginside_'


cfg = Settings()
