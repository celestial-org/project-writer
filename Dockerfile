FROM python

RUN useradd -m -u 1000 user
WORKDIR /home/user
RUN git clone https://github.com/chantroi/project-writer bot
WORKDIR /home/user/bot
RUN pip install -r requirements.txt
RUN chown -R user:user /home/user/bot
RUN chmod +x ./start.sh && chmod +x ./lite

USER user
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
