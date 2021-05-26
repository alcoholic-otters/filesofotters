# Files of Otters - API Guide

> **NOTE**: This document is a work in progress.

Files of Otters comes with a default web client. However, if you wish you
implement your own front-end client, you can interact with the server using
the calls documented here.

## Authentication

Most operations require you to be logged in. These calls help you create an
account and log in.

### `GET /filesharing/register`

Responds with an HTML file used to register a new account.

### `POST /filesharing/register`

Registers a new account and redirects to a relevant page.

The POST request body must contain the following parameters:

- `username`: plaintext username
- `password1`: plaintext password of the new user.
- `password2`: same as `password1` (must match)

### `GET /filesharing/login`

Responds with an HTML file used to log in.

### `POST /filesharing/login`

Logs a user in and redirects to a relevant page.

The POST request body must contain the following parameters:

- `username`: plaintext username
- `password`: plaintext password of the user.

### `POST /filesharing/logout`

Logs the user out and redirects to the login page.

## File transfer

TODO: Write this.

### `POST /filesharing/upload`

### `POST /filesharing/delete/<int:id>`
