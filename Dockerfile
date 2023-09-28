FROM --platform=linux/amd64 python:3.9-slim

RUN apt-get update -y && apt-get install wget gnupg2 -y && rm -rf /var/lib/{apt,dpkg,cache,log}

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

RUN mkdir -p $HOME/app/data/output/ca && chown 1000:1000 $HOME/app/data/output/ca
RUN mkdir -p $HOME/app/data/output/es && chown 1000:1000 $HOME/app/data/output/es
 

ENTRYPOINT [ "python", "-u" ]