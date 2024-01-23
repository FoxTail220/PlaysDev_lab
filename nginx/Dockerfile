FROM nginx:1.25.3

USER root

RUN apt-get update && \
    apt-get install -y nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i '6 a\load_module modules/ngx_http_image_filter_module.so;' /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx

RUN mkdir -p html/secondpage \
    mkdir -p /etc/letsencrypt/live/etc/letsencrypt/live/task18.hopto.org \
    music \
    redblue \
    images && \
    chown -R nginx:nginx /usr/share/nginx && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./html /usr/share/nginx
COPY ./ssl/fullchain.pem /etc/letsencrypt/live/etc/letsencrypt/live/task18.hopto.org
COPY ./ssl/privkey.pem /etc/letsencrypt/live/etc/letsencrypt/live/task18.hopto.org  
