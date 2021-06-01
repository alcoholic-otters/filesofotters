# Files of Otters - API Guide

> **NOTE**: This document is a work in progress.

Files of Otters comes with a default web client. However, if you wish you
implement your own front-end client, you can interact with the server using
the calls documented here.

**Table of contents**:

- [Authentication](#authentication)
- [File transfer](#file-transfer)
- [Group management](#group-management)
- [File management](#file-management)
- [Search](#search)

## Authentication

Most operations require you to be logged in. These calls help you create an
account and log in.

### `GET /filesharing/register`

Responds with an HTML file used to register a new account.

### `POST /filesharing/register`

Registers a new account.

The POST request body must contain the following parameters:

- `username`: plaintext username
- `password1`: plaintext password of the new user
- `password2`: same as `password1` (must match).

### `GET /filesharing/login`

Responds with an HTML file used to log in.

### `POST /filesharing/login`

Logs a user in.

The POST request body must contain the following parameters:

- `username`: plaintext username
- `password`: plaintext password of the user.

### `POST /filesharing/logout`

Logs the user out.

## File transfer

These calls allow users to upload, delete and download files.

### `POST /filesharing/upload`

Uploads a file to the server.

**The user should be logged in.**

The user should not already have a file with the same name. The file size
shouldn't exceed the maximum allowed size.

The POST request body must contain the following parameters:

- `the_file`: the file to be uploaded.

### `POST /filesharing/delete/<int:id>`

Deletes a file from the server.

**The user should be logged in and should be the owner of the file**.

The URL parts have the following meanings:

- `id` - the id of the file.

The POST request body **must** contain a `_method` parameter with the value of
`delete`.

## Group management

### `GET /filesharing/group/manage`

Returns an HTML page which allows a user to manage their groups.

**The user should be logged in.**

### `POST /filesharing/group/create`

Creates a new group for the user.

**The user should be logged in.**

The POST request body must contain the following parameters:

- `name`: the name of the new group.

### `GET /filesharing/group/delete/<int:id>`

Deletes a group belonging to the user.

**The user should be logged in and should be the owner of the group.**

The URL parts have the following meanings:

- `id` - the id of the group.

### `POST /filesharing/group/member/add`

Adds a member to a group.

**The user should be logged in and should own the group.**

The group owner does not need to become a member, they have special status.

The POST request body must contain the following parameters:

- `group_id`: the id of the group
- `username`: the username of the new member.

### `GET /filesharing/group/member/remove/<int:id>/<str:username>`

Removes a member from a group.

**The user should be logged in and should own the group.**

The URL parts have the following meanings:

- `id` - the id of the group
- `username` - the username of the member to be removed.

## File management

### `POST /filesharing/file/groups/set/<int:id>`

Sets the list of groups a file is exposed to.

**The user should be logged in and should own the file.**

The URL parts have the following meanings:

- `id` - the id of the file.

The POST request body must contain the following parameters:

- `groups`: list of the group ids to be used.

### `GET /filesharing/detail/file/<int:id>`

Returns an HTML page with details about the file and controls for it.

**The user should be logged in and should own the file.**

The URL parts have the following meanings:

- `id` - the id of the file.

### `POST /filesharing/tag/attach/<int:file_id>`

Attaches a tag to a file.

**The user should be logged in and should own the file.**

The URL parts have the following meanings:

- `id` - the id of the file.

The POST request body must contain the following parameters:

- `tag_name`: the name of the tag.

### `POST /filesharing/tag/detach/<int:file_id>/<int:tag_id>`

Detaches a tag from a file.

**The user should be logged in and should own the file.**

The URL parts have the following meanings:

- `file_id` - the id of the file
- `tag_id` - the id of the tag.

## Search

### `POST /filesharing/search`

Returns an HTML page which only displays files that meet certain criteria.

**The user should be logged in.**

Files can be searched both by name and by the tags attached.

The POST request body should contain the following parameters:

- `search`: query string which can include hashtags
- `search_tags`: list of tag ids.
