FROM python:3.9.2

WORKDIR app

ENV TZ=Asia/Shanghai
ENV FLASK_CONFIG=production

COPY . /app

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && apt-get update \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt update && apt install freetds-dev build-essential -y && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoclean

RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 80
CMD ["uwsgi", "--ini", "/app/app-uwsgi.ini"]
