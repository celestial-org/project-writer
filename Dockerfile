FROM python

RUN useradd -m -u 1000 user
COPY . /home/user/bot
WORKDIR /home/user/bot
RUN chown -R user:user /home/user/bot

RUN chmod +x lite start.sh
RUN pip install -r requirements.txt

USER user
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
