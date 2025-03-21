# CodeGuard

A platform to learn secure coding.  

## Dependencies

This app requires python>=3.12 to run. If you don't have python, install it first.  
Other dependencies are listed in requirements.txt

## Quickstart

1. Clone this repository and switch directory to the cloned repo
```console
git clone https://github.com/Xovert/CodeGuard.git
cd CodeGuard
```

2. Set up the config.ini file inside the CodeGuard app folder
Copy config.ini.example and rename it into config.ini

3. In your terminal, enter the following commands
Run the production config script.

Linux/MacOS:
```console
./production.sh
```
Windows:
```console
./production.bat
```

## Notes/Config

##### Config
Several things that you can configure (config must be created at `CodeGuard/config.ini`):
<details>
<summary>Server</summary>

```ini
[server]
SECRET_KEY = ; A specified secret key for app secrets, can be left empty, will be auto-generated.
SECURITY_PASSWORD_SALT = ; A salt for extra security measures, can be left empty, will be auto-generated.
SESSION_COOKIE_SECURE = ; A configuration to only send cookies over https connections. Set this to 'true' if you have https connection set, otherwise leave empty.
SESSION_COOKIE_HTTPONLY = ; A configuration to only allow http connection to access the cookie. Default to 'true', set to 'false' if you need to access cookie from javascript.
PERMANENT_SESSION_LIFETIME = 604800 ; Login session lifetime expiry, defaults to 7 days before expired.
DATABASE_URL = ; The Database URL in the format of `dialect+driver://username:password@host:port/database`, if not customised, leave empty.
```
</details>
<details>
<summary>Email for outgoing Mails</summary>

```ini
[email]
MAIL_DEFAULT_SENDER = ; The default name for sender that will be used when sending emails.
MAIL_SERVER = ; The mail server address, may be a relay server.
MAIL_PORT = ; The port of the mail server that will be used to send the email.
MAIL_USE_TLS = ; The cryptographic protocol for sending mails, TLS is updated version of SSL. Using TLS over SSL is recommended.
MAIL_USE_SSL = ; The cryptographic protocol for sending mails, SSL is an outdated version. Using TLS over SSL is recommended.
MAIL_DEBUG = ; Enable Mail Debugging for Development. Set it to False in production builds.
MAIL_USERNAME = ; Username for Authentication with Mail Server
MAIL_PASSWORD = ; Password for Authentication with Mail Server
```
</details>
<details>
<summary>File Uploads</summary>

```ini
[uploads]
UPLOADED_PHOTOS_DEST = uploads ; Default location for image uploads, default, leave unchanged.
UPLOAD_PROVIDER = minio ; Default Provider for File Uploads, Compatible with S3 object storage. If use docker, default to 'minio'. Leave unchanged if not customised.
AWS_S3_ENDPOINT_URL = ; Address of S3 Object Storage including port
AWS_S3_BUCKET = ; Name of Bucket
AWS_ACCESS_KEY_ID = ; Key ID / Username
AWS_SECRET_ACCESS_KEY = ; Access Key / Password
AWS_S3_REGION = ; Region for S3
```
</details>
<details>
<summary>Semgrep</summary>

```ini
[semgrep]
SEMGREP_APP_TOKEN = ; Your personal Semgrep Token
SEMGREP_PATH = semgrep_rules ; Directory of custom semgrep rules. Root directoryis the CodeGuard app directory. If not customised, leave unchanged.
```
</details>

##### Guide
1. By default, there are 6 default users:

    |No.| Username | Email | Password | Role |
    |---| -------- | ----- | -------- | ---- |
    | 1.| Admin    | admin@gmail.com | 4dm!n | Admin |
    | 2.| john    | john@gmail.com | j0hn# | User |
    | 3.| jane    | jane@gmail.com | j4ne# | User |
    | 4.| user1    | user1@gmail.com | user1 | User |
    | 5.| user2    | user2@gmail.com | user2 | User |
    | 6.| user3    | user3@gmail.com | user3 | User |

2. You can login using any of the accounts above, or register a new user and login.
