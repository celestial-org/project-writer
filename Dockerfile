FROM python:latest

RUN useradd -m -u 1000 useradd
COPY . /home/user
WORKDIR /home/user
RUN pip install -r requirements.txt
RUN chown -R user:user /home/user
RUN chmod +x ./start.sh
USER user
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
