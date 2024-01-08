FROM php:apache


RUN  useradd -u 1001 valera
USER valera

USER root

RUN apt-get update && apt-get install nano -y 

USER valera


COPY ./index.html /var/www/html/

RUN echo "<?php phpinfo(); ?>" > /var/www/html/info.php

CMD ["apache2-foreground"]

