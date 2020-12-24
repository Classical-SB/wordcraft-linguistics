# Wordcraft Linguistics

A Dockerized [spaCy](https://spacy.io/) application purposed for mining properties and other NLP assisted tasks.

## Development

1.  Build the container.

        % docker build -t wl .

2.  Run the container.

        % docker run -p 80:80 wl

## Deployment

The app is deployed on an Amazon EC2 instance. To make changes and deploy the app, follow the steps below.

1.  Get the `.pem` file from Oliver.

2.  SSH into the instance.

        % ssh -i <PEM_FILE> ec2-user@<EC2_PUBLIC_URL> -oStrictHostKeyChecking=no

3.  Make any changes.

4.  Rebuild the container.

        % docker build -t wl .

5.  Run the container.

        % docker run -p 80:80 wl