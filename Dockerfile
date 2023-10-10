FROM ubuntu

## Install Base Packages
RUN apt-get update && apt-get -y install \
    apache2

RUN a2enmod rewrite

RUN apt-get update && apt-get -y install \
    libapache2-mod-perl2 \
    perl \
    libcgi-session-perl
RUN a2enmod cgi
RUN a2enmod rewrite

EXPOSE 80

COPY ./cgi-bin /usr/lib/cgi-bin
COPY ./www /var/www/html
COPY ./flag.txt /flag.txt

RUN chmod +x /usr/lib/cgi-bin/search.cgi

CMD /usr/sbin/apache2ctl -D FOREGROUND