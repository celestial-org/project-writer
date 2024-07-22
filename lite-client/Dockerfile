FROM python

WORKDIR /app
COPY . /app
RUN pip install pyrogram tgcrypto requests
RUN chmod +x lite

ENV BOT_TOKEN=${BOT_TOKEN}
ENTRYPOINT python -u main.py