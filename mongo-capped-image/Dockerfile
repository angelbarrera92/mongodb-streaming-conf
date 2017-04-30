FROM mongo:3.4

ENV AUTH yes
ENV STORAGE_ENGINE wiredTiger
ENV JOURNALING no

ADD run.sh /run.sh
ADD set_mongodb_password.sh /set_mongodb_password.sh

RUN chmod +x /run.sh
RUN chmod +x /set_mongodb_password.sh

ENTRYPOINT ["/bin/bash"]
CMD ["/run.sh"]