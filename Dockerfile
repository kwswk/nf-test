FROM --platform=linux/amd64 ubuntu as base

ENV GET_ALL_DETAILS=0
ENV S3_BUCKET=sample_bucket
ENV S3_PREFIX=bags-data.json

WORKDIR /usr/src/app

ADD app ./
COPY requirements.txt .

RUN apt-get update \
&& apt-get install -y libglib2.0-0 libnss3 libxcb1 python3 python3-pip python3.12-venv xvfb wget

RUN apt -f install -y
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y --fix-missing

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN venv/bin/pip3 install -r requirements.txt

RUN echo "source /usr/src/app/venv/bin/activate" >> /root/.bashrc

ENTRYPOINT ["/bin/bash", "-l", "-c"]
CMD /usr/src/app/venv/bin/python -m main --get_all_details $GET_ALL_DETAILS --s3_bucket $S3_BUCKET --s3_prefix $S3_PREFIX
