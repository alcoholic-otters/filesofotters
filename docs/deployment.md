# Files of Otters - Deployment Guide

> **NOTE**: This document is a work in progress.

The application uses an AWS S3 bucket to store files. Because of this, we
recommend also using other AWS services to host this web app. In this guide,
we will use AWS Lightsail.

If something is unclear, these tutorials might help:

- [Deploy a Django-based app on Lightsail][aws-django-lightsail-tutorial]
- [Control access to an S3 bucket][aws-bucket-access-tutorial]

1. **Create an AWS account** (if you don't have one)

    You can use a free trial account, which lasts a year. You can see which
    services are offered for free [here](https://aws.amazon.com/free/). From
    this page, you can also create a new account.

1. **Create an S3 bucket**

    While most data is stored on the server itself, the file contents are stored
    in an S3 bucket. To create one, write "S3" in the search bar, and click on
    the first option that comes up.

    From here, click on "Create bucket" and choose a name. Also remember the
    region where it gets created, because you'll need it later. Make sure to
    select "Block all public acces", then click on "Create bucket".

1. **Create a Lightsail instance**

    Note: **Lightsail seems to be free only for 30 days**. We'll still use it
    because it's simpler than alternatives.

    We'll need a new Lightsail instance to run the app. Type "Lightsail" in the
    search bar, then click on "Create instance". Select the Linux platform with
    the "Django" blueprint. If you're using a new account, you might need to
    create a new SSH key pair. Choose the free instance plan and give it a name,
    then click on "Create instance".

1. **Copy the S3 credentials on the Lightsail instance**

    Create an IAM user with programmatic access to the S3 service. Follow [this
    tutorial][aws-bucket-access-tutorial].

    From the browser, SSH into the new instance and copy your S3 credentials
    to the `~/.aws` directory.

1. **Clone the repo on Lightsail**

    Issue the following command to create a directory for projects and give
    the current system user write permissions to it.

    ```bash
    sudo mkdir /opt/bitnami/projects && sudo chown $USER /opt/bitnami/projects
    ```

    Move to the new directory and clone the repo here.

    ```bash
    cd /opt/bitnami/projects
    git clone https://github.com/alcoholic-otters/filesofotters
    ```

1. **Set up the database (`makemigrations`)**

    To initialize the database apply the migration files from the repo:

    ```bash
    python3 manage.py migrate
    ```

    You should also create a super user now (an administrator account):

    ```bash
    python3 manage.py createsuperuser
    ```

1. **Configure your server**

    In the `filesofotters/settings.py` file, replace the `AWS_S3_REGION_NAME`
    field to the region where you created your S3 bucket. You can find the short
    name of each region [here](
    https://docs.aws.amazon.com/general/latest/gr/s3.html).

    For security, you should also change the `SECRET_KEY` field in this file.

    Replace the `bucket_name` field of the `FileStorage` class in the
    `filesharing/file_storage.py` file with the name you gave your bucket.

    Then follow **step 4** from [this tutorial][aws-django-lightsail-tutorial].

1. **Start the server**

    To run the server and leave it running, you can enter the following command:

    ```bash
    python3 manage.py runserver 0.0.0.0:8000 &
    ```

    You should be able to access the website even after closing the SSH session.

    The URL you should access is `<your-public-ip>/filesharing`.

This guide uses the debug server included with Django to deploy the app, for
simplicity. You should instead attempt to configure Apache, following **step 5**
of [this tutorial][aws-django-lightsail-tutorial].

[aws-django-lightsail-tutorial]:
https://aws.amazon.com/getting-started/hands-on/deploy-python-application/
[aws-bucket-access-tutorial]:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html
