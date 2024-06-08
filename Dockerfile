FROM python

RUN useradd -m -u 1000 user

WORKDIR /home/user/bot

RUN chown -R user:user /home/user/bot

USER user

EXPOSE 8080

ENTRYPOINT ["./start.sh"]
