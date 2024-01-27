ARG PYTHON_VERSION=3.11.3-slim-bullseye
FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . /code/

# just as a backup, they're already executable and already work
RUN chmod +x /code/run_indexer.sh /code/startup.sh

# do not need procps (htop already has uptime)
RUN apt-get update -qq && apt-get upgrade -y -qq && \
apt-get install -y -qq --no-install-recommends git htop nano rsync sqlite3 && \
apt-get clean && rm -rfv /var/lib/apt/lists/*

# do not need glances (already installing htop)
RUN set -ex && \
pip install --root-user-action=ignore --upgrade pip && \
pip install --root-user-action=ignore --requirement etc/reqs_base.pip && \
rm -rf /root/.cache/

RUN git clone https://github.com/venteto/vps-misc.git && \
mv vps-misc/.bashrc /root/.bashrc

EXPOSE 8080
CMD ./startup.sh
