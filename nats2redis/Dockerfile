FROM ericsson/proxies:latest
LABEL vendor="Ericsson AB" version="0.95" description="Temp Data Aggregator"
MAINTAINER ecejjar
RUN [ "./run_command.sh", "apt-get", "-y", "update" ]
RUN [ "./run_command.sh", "apt-get", "-y", "install", "python2.7", "python2.7-dev", "python-pip" ]
RUN [ "./run_command.sh", "pip", "install", "redis" ]
ADD start.py /app/
ADD test.py /app/
ADD pynats.tgz /app/
ENV PYTHONPATH="/app"
RUN [ "python", "/app/test.py" ]
ENTRYPOINT [ "python", "/app/start.py" ] 
