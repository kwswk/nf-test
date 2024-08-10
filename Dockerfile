FROM python:3.12 as base

WORKDIR /usr/src/app

ADD app ./
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
&& apt-get update \
&& apt-get install -y --no-install-recommends google-chrome-stable \
&& apt-get remove -y google-chrome-stable \
&& rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash", "-c" ]
