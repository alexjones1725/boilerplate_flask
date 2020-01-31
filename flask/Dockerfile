FROM tiangolo/uwsgi-nginx:python3.7

RUN apt-get update -y

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Set working directory to /usr/src/app
WORKDIR /app

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]