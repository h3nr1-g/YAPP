FROM debian:stable-slim 

RUN apt-get update -y

RUN apt-get install -y \
  python3-dev \
  python3-pip \
  git

COPY docker/entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

COPY yapp /root/yapp
WORKDIR /root/yapp
RUN rm -rf presenter/migrations bots/migrations db.sqlite3
RUN mkdir db
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN python3 manage.py makemigrations --settings yapp.settings.build bots presenter
RUN python3 manage.py migrate --settings yapp.settings.build
RUN python3 manage.py collectstatic --settings yapp.settings.build

CMD /root/entrypoint.sh
