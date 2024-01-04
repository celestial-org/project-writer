FROM python:latest

COPY . .
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
