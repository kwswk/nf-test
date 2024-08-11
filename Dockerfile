FROM ubuntu as base

WORKDIR /usr/src/app

ADD app ./
COPY requirements.txt .

RUN apt-get update \
&& apt-get install -y --no-install-recommends firefox python3 python3-pip python3.12-venv

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN venv/bin/pip3 install -r requirements.txt

RUN echo "source /usr/src/app/venv/bin/activate" >> /root/.bashrc

ENTRYPOINT ["/bin/bash", "-l", "-c"]
CMD ["bash"]
