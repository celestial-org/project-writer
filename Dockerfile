FROM python:3.10

COPY . .
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
