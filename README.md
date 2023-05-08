# TrailersPlus Documentation


*** Documentation for manOS BigSur Version 11.1. The documentation is also 
    suitable for Linux systems.


## Prerequisites
- Docker
- Docker-compose

## Setup
To set up the project, please follow these steps:

### Clone the project repository to your local machine:

```bash
git clone  https://github.com/mwaterous/trailersplus_website.git
```
### Navigate into the project backend directory:

```bash
cd trailersplus_website/trailersplus
```
### Create .env file with the help of .env.example file:

```bash
cp .env.example .env
```
### Edit environment variables:
```bash
nano .env
```
### Create .env file for docker with the help of .env.example file:
```
cp ./docker/.env.example ./docker/.env
```
### Edit environment variables:
```bash
nano ./docker/.env
```
### Create a directory for storing certificates:
```bash
mkdir ./trailersplus/certs
```
### Copy the certificate file to the directory:
```bash
cp /path/to/certificate ./trailersplus/certs
```
### Create a directory for storing location mindmax database:
```bash
mkdir ./trailersplus/locations
```
### Copy the location mindmax database file to the directory:
```bash
cp /path/to/mindmaxdb/*.mmdb ./trailersplus/locations
```
### Build the Docker images:
```bash
make build
```

### Start the Docker containers:
```bash
make up
```
### Run migrations:
```bash
make migrate
```
### Create a superuser:
```bash
make superuser
```
### Collect static files:
```bash
make collectstatic
```

### Finally, start the development server:
```bash
make server
```
You can now access the application by navigating to http://localhost:8000 in your web browser. The pgAdmin interface can be accessed at http://localhost:16543. You can log in to pgAdmin using the credentials specified in the `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` environment variables in the `.env` file.

## Additional Management Commands
### Here are some additional management commands that you may find useful:

- **make stop**: Stop the Docker containers.
- **make down**: Stop and remove the Docker containers, networks, images, and volumes.
- **make restart**: Restart the Docker containers.
- **make ssh**: SSH into the web container.
- **make ssh-db**: SSH into the database container.
- **make migrations**: Create new database migrations.
- **make shell**: Open the Django shell.
- **make test**: Run the Django test suite.
- **make flake8**: Run Flake8 code linter.
- **make logs**: View the web container logs.
- **make logs-celery**: View the Celery container logs.
- **make logs-db**: View the database container logs.
## Conclusion
Congratulations! You have successfully set up the "trailersplus" project on your machine. If you encounter any issues or have any questions, please feel free to reach out to "mark@temeritystudios.com"