FROM node:latest AS static_build
RUN corepack enable
WORKDIR /build/
COPY package.json yarn.lock ./
RUN yarn install
COPY www www
RUN yarn run jshint

FROM httpd:2.4
RUN apt-get update \
    && apt-get install -y \
        libapache2-mod-wsgi-py3 \
        build-essential \
        python3-venv \
        python3-dev \
        default-mysql-server  \
        default-libmysqlclient-dev  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
ENV VIRTUAL_ENV=/build/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY webapp/requirements.txt .
RUN pip install -r requirements.txt
ENV NLTK_DATA="/build/nltk_data"
RUN python3 -c "import nltk; nltk.download('omw-1.4', download_dir='/build/nltk_data')"

COPY webapp/wsgi.py /var/www/buzzword-ipsum-wsgi/
COPY webapp/setup.py ./
COPY webapp/buzzwordipsum ./buzzwordipsum
RUN python3 setup.py develop
RUN pytest --cov buzzwordipsum --cov-report term-missing

COPY --from=static_build /build/www /usr/local/apache2/htdocs

COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf