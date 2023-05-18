FROM ubuntu:23.04
RUN apt update && \
	apt upgrade --yes && \
	apt install --yes --no-install-recommends tzdata && \
	ln -fs /usr/share/zoneinfo/Zulu /etc/localtime && \
	dpkg-reconfigure --frontend noninteractive tzdata && \
	apt install --yes --no-install-recommends \
	pylint \
	python3 \
	python3-argcomplete \
	python3-docutils \
	python3-invoke \
	python3-paramiko \
	python3-pip \
	python3-psycopg2 \
	python3-pycodestyle \
	python3-pydocstyle \
	python3-pytest \
	python3-jinja2 \
	python3-sqlalchemy \
	python3-dotenv \
	python3-humanize \
	python3-docker \
	python3-httpx

# Set application dir in container
WORKDIR /app

# Install application files
COPY bin bin
COPY cmon cmon
COPY tests tests

ENV PYTHONPATH=/app
ENV PATH=/app/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Cleanup of installation media
RUN apt clean

# Run the environment automated test
CMD cmon --help
