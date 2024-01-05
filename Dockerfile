FROM python:latest

RUN useradd -m -u 1000 user
COPY . /home/user
WORKDIR /home/user
RUN curl -L -o lite.gz https://github.com/xxf098/LiteSpeedTest/releases/download/v0.15.0/lite-linux-amd64-v0.15.0.gz && gunzip -d lite.gz
RUN pip install -r requirements.txt
RUN chown -R user:user /home/user
RUN chmod +x ./start.sh && chmod +x ./lite

USER user
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
