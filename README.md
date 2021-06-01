# Files of Otters

**Files of Otters** is a file-sharing system, a web app which allows you to
upload files and share them with otter [*sic*] users you trust.

![The main screen of the app in use](docs/img/main-screen.png)

## Main features

- File upload and download
- Privacy control
- File search
- File organization with tags
- Clean, responsive interface

## Quick start

If you want to test the app locally or to work on the code, follow these steps:

1. Install the dependencies (you should probably use `venv` too):

    ```bash
    pip3 install -r requirements.txt --upgrade
    ```

1. Configure the database:

    ```bash
    python3 manage.py migrate
    ```

1. Create an admin account (choose any credentials):

    ```bash
    python3 manage.py createsuperuser
    ```

1. Run the server:

    ```bash
    python3 manage.py runserver
    ```

Visit `localhost:8000/filesharing` in your browser. You can log in using the
admin account created earlier, or you can register a new account.

For full functionality you need to connect to an AWS S3 bucket. Simply copy your
credentials to the `~/.aws/credentials` file and change the region and bucket
name used by the app. Details in the [deployment guide](docs/deployment.md).

## Documentation

If you want to learn how to do something with the app, you can find some docs
[here](docs).

## Development

This app is being developed using git, and the central repo is on Github, at
[this address](https://github.com/alcoholic-otters/filesofotters).

## License

This project is licensed under the terms of the MIT license.
