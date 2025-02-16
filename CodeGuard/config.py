import configparser
import os
import pathlib
from setuptools._distutils.util import strtobool
from typing import Union
from sqlalchemy.engine.url import URL
from datetime import timedelta


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        envvar = os.getenv(option)
        if value == "" and envvar:
            return process_string_var(envvar)
        else:
            return value


def process_string_var(value):
    if value == "":
        return None

    if value.isdigit():
        return int(value)
    elif value.replace(".", "", 1).isdigit():
        return float(value)

    try:
        return bool(strtobool(value))
    except ValueError:
        return value


def process_boolean_str(value):
    if type(value) is bool:
        return value

    if value is None:
        return False

    if value == "":
        return None

    return bool(strtobool(value))


def empty_str_cast(value, default=None):
    if value == "":
        return default
    return value

def get_secret_key():
    try:
        with open(".secret_key", "rb") as secret:
            secret_key = secret.read()
    except OSError:
        secret_key = None

    if not secret_key:
        secret_key = os.urandom(64)
        try:
            with open(".secret_key", "wb") as secret:
                secret.write(secret_key)
                secret.flush()
        except OSError:
            pass

    return secret_key

def get_security_password_salt():
    try:
        with open(".security_salt", "rb") as salt:
            security_salt = salt.read()
    except OSError:
        security_salt = None

    if not security_salt:
        security_salt = os.urandom(64)
        try:
            with open(".security_salt", "wb") as secret:
                secret.write(security_salt)
                secret.flush()
        except OSError:
            pass
    
    return security_salt


config_ini = configparser.ConfigParser(interpolation=EnvInterpolation())
config_ini.optionxform = str
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config_ini.read(path)


class ProductionConfig(object):
    # Server
    SECRET_KEY: str = empty_str_cast(config_ini["server"]["SECRET_KEY"]) or get_secret_key()

    SECURITY_PASSWORD_SALT: str = empty_str_cast(config_ini["server"]["SECURITY_PASSWORD_SALT"]) or get_security_password_salt()

    # Cookie
    SESSION_COOKIE_SECURE: bool = process_boolean_str(config_ini["server"]["SESSION_COOKIE_SECURE"]) or False
    
    SESSION_COOKIE_HTTPONLY: bool = process_boolean_str(config_ini["server"]["SESSION_COOKIE_HTTPONLY"]) or True
    
    PERMANENT_SESSION_LIFETIME: int = config_ini["server"].getint("PERMANENT_SESSION_LIFETIME") \
        or timedelta(days=2).total_seconds()

    DATABASE_URL: str = empty_str_cast(config_ini["server"]["DATABASE_URL"])
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # Email
    MAIL_DEFAULT_SENDER: str = empty_str_cast(config_ini["email"]["MAIL_DEFAULT_SENDER"])

    MAIL_SERVER: str = empty_str_cast(config_ini["email"]["MAIL_SERVER"])

    MAIL_PORT: int = empty_str_cast(config_ini["email"]["MAIL_PORT"])

    MAIL_USE_TLS: bool = process_boolean_str(config_ini["email"]["MAIL_USE_TLS"])

    MAIL_USE_SSL: bool = process_boolean_str(config_ini["email"]["MAIL_USE_SSL"])

    MAIL_DEBUG: bool = process_boolean_str(config_ini["email"]["MAIL_DEBUG"])

    MAIL_USERNAME: str = empty_str_cast(config_ini["email"]["MAIL_USERNAME"])

    MAIL_PASSWORD: str = empty_str_cast(config_ini["email"]["MAIL_PASSWORD"])

    # Uploads
    UPLOADED_PHOTOS_DEST: str = empty_str_cast(config_ini["uploads"]["UPLOADED_PHOTOS_DEST"])

    UPLOAD_PROVIDER: str = empty_str_cast(config_ini["uploads"]["UPLOAD_PROVIDER"]) \
        or "filesystem"

    if UPLOAD_PROVIDER in ("s3", "minio"):
        AWS_S3_ENDPOINT_URL: str = empty_str_cast(config_ini["uploads"]["AWS_S3_ENDPOINT_URL"])

        AWS_S3_BUCKET: str = empty_str_cast(config_ini["uploads"]["AWS_S3_BUCKET"])

        AWS_ACCESS_KEY_ID: str = empty_str_cast(config_ini["uploads"]["AWS_ACCESS_KEY_ID"])

        AWS_SECRET_ACCESS_KEY: str = empty_str_cast(config_ini["uploads"]["AWS_SECRET_ACCESS_KEY"])

        AWS_S3_REGION: str = empty_str_cast(config_ini["uploads"]["AWS_S3_REGION"])

    # Semgrep
    SEMGREP_APP_TOKEN: str = empty_str_cast(config_ini['semgrep']["SEMGREP_APP_TOKEN"])

    SEMGREP_PATH: str = empty_str_cast(config_ini['semgrep']["SEMGREP_PATH"])

class DevelopmentConfig(object):
    # SERVER
    SECRET_KEY='devtesthings'
    SECURITY_PASSWORD_SALT = '474e09ff10b75e34dc1745b1890339f2ee93355b892266590adac68ad84849bc'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=2).total_seconds()
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://codeguard:codeguard@127.0.0.1:7306/CodeGuard?charset=utf8mb4"
    # MAIL
    MAIL_DEFAULT_SENDER = ""
    MAIL_SERVER = ""
    MAIL_PORT = 0
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    # UPLOADS
    UPLOADED_PHOTOS_DEST='uploads'
    UPLOAD_PROVIDER = "minio"
    AWS_S3_ENDPOINT_URL = "http://127.0.0.1:9000"
    AWS_S3_BUCKET = "codeguard"
    AWS_ACCESS_KEY_ID = "minioadmin"
    AWS_SECRET_ACCESS_KEY = "minioadmin"
    AWS_S3_REGION = "us-east-1"
    # SEMGREP
    SEMGREP_APP_TOKEN = ""
    SEMGREP_PATH = os.path.join(pathlib.Path().resolve(), 'semgrep_rules')

config = ProductionConfig()
devconfig = DevelopmentConfig()
