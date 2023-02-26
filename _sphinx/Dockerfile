# Base Image
FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y nginx python3 python3-pip \
                    fonts-ipafont fonts-ipaexfont && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    apt-get clean -y

RUN pip3 install sphinx sphinx_rtd_theme \
        sphinxcontrib-actdiag \
        sphinxcontrib-blockdiag \
        sphinxcontrib-nwdiag \
        sphinxcontrib-seqdiag \
        sphinx_markdown_tables \
        cloud-sptheme \
        recommonmark

WORKDIR /tmp
COPY ./source/ ./source/
COPY Makefile ./
RUN make html && rm -rf /var/www/html && cp -R /tmp/build/* /var/www/

