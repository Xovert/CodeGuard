# Code Guard

A platform to learn secure coding.  

## Dependencies

This app requires python>=3.12 to run. If you don't have python, install it first.  
Other dependencies are listed in requirements.txt

## How-to-run

1. Clone this repository and switch directory to the cloned repo
```console
git clone https://github.com/Xovert/CodeGuard.git
cd CodeGuard
```

2. In your terminal, enter the following commands

Linux/Mac/Windows:
```console
docker compose up --build -d
```

## Notes/Config

##### Config
Several things that you can config (config must be created at `config.ini`):
```
SECRET_KEY='<YOUR_SECRET_KEY>'
SECURITY_PASSWORD_SALT='<YOUR_PASSWORD_SALT>'
```

##### Guide
1. By Default, there's no default user. Create one first.
2. Register user first.
3. Then login using the previously registered user.
