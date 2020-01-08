FROM squidfunk/mkdocs-material:4.6.0
LABEL maintainer="Michael Hausenblas, hausenbl@amazon.com"

COPY action.sh /action.sh

RUN apk add --no-cache bash && chmod +x /action.sh
RUN git clone https://github.com/Owen-Liuyuxuan/mkdocs-awesome-pages-plugin.git
RUN python3 ./mkdocs-awesome-pages-plugin/setup.py install --user
ENTRYPOINT ["/action.sh"]