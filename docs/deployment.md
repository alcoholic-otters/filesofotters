# Files of Otters - Deployment Guide

> **NOTE**: This document is a work in progress.

The application uses an AWS S3 bucket to store files. Because of this, we
recommend also using other AWS services to host this web app. In this guide,
we will use AWS Lightsail.

TODO: Complete this guide.

0. **Create an AWS account** (if you don't have one)

    You can use a free trial account, which lasts a year. You can see which
    services are offered for free [here](https://aws.amazon.com/free/). From
    this page, you can also create a new account.

1. **Create an S3 bucket**

    While most data is stored on the server itself, the file contents are stored
    in an S3 bucket. To create one, write `S3` in the search bar, and click on
    the first option that comes up.

2. **Create a Lightsail instance**

3. **Copy the S3 credentials on the Lightsail instance**

4. **Clone the repo on Lightsail**

5. **Set up the database (`makemigrations`)**

6. **Configure your server**

7. **Start the server**
