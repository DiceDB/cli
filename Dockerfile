FROM dicedb/dice:latest

COPY . /cli

RUN apt-get update --fix-missing
RUN apt-get install -yqq python3 python3-pip python-is-python3
RUN python3 -m pip install poetry
WORKDIR /cli
RUN poetry config virtualenvs.create false
RUN poetry build
RUN pip install dist/cli*.tar.gz
WORKDIR /
RUN rm -rf .cache /var/cache/apt
RUN rm -rf /cli

CMD ["sh", "-c", "/opt/redis-stack/bin/redis-stack-server --daemonize yes && diceroll"]
