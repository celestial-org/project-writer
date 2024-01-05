FROM python:latest

COPY . .
RUN curl -L -o lite.gz https://github.com/xxf098/LiteSpeedTest/releases/download/v0.15.0/lite-linux-amd64-v0.15.0.gz && gunzip -d lite.gz
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 8080
ENTRYPOINT ["./start.sh"]
