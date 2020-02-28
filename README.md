# Serverless training

## Preparing the package

Project required some additional dependencies to be installed:
* python requirements
* libcairo
* libpango

All dependencies should be packaged in a zip file that will be sent to lambda.
In order to do that use [lambci/lambda:build-python3.8](https://hub.docker.com/r/lambci/lambda) image.

Run
```
docker run --rm -it -v "$(pwd):/code" lambci/lambda:build-python3.8 sh 
```

Inside the container, install all required dependencies and copy them to root directory of your project.
This includes all python's modules (located in `site-packages`) as well as shared libraries.

In case of this project, follow those steps:
```
cd /code/h2p
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp -r venv/lib/ ./
yum install cairo pango
cp /usr/lib64/libpango-1.0.so.0 .
cp /usr/lib64/libcairo.so.2 ./
# repoquery -l command was helpful here - `yum install yum-utils` to get that
```



## Creating a lambda layer package for WeasyPrint with Python3.8

**Dockerfile**

```Dockerfile
FROM lambci/lambda:build-python3.7 AS py37
FROM lambci/lambda:build-python3.8

# download libraries
RUN yum install -y yum-utils rpmdevtools
WORKDIR /tmp
RUN yumdownloader --resolve \
    expat \
    glib2 \
    libffi \
    libffi-devel \
    cairo \
    pango && \
    rpmdev-extract *rpm

# install libraries and set links
RUN mkdir /opt/lib
WORKDIR /opt/lib
RUN cp -P -R /tmp/*/usr/lib64/* /opt/lib
RUN ln libgobject-2.0.so.0 libgobject-2.0.so && \
    ln libcairo.so.2 libcairo.so && \
    ln libpango-1.0.so.0 pango-1.0 && \
    ln libpangoft2-1.0.so.0 pangoft2-1.0 && \
    ln libpangocairo-1.0.so.0 pangocairo-1.0

# copy fonts and set environment variable
COPY --from=py37 /usr/share/fonts/default /opt/fonts/default
COPY --from=py37 /etc/fonts/fonts.conf /opt/fonts/fonts.conf
RUN sed -i s:/usr/share/fonts:/opt/fonts: /opt/fonts/fonts.conf
ENV FONTCONFIG_PATH="/opt/fonts"

# install weasyprint and dependencies
WORKDIR /opt
RUN pipenv install weasyprint
RUN mkdir -p python/lib/python3.8/site-packages
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt --no-deps -t python/lib/python3.8/site-packages

# remove warning about cairo < 1.15.4
WORKDIR /opt/python/lib/python3.8/site-packages/weasyprint
RUN sed -i.bak '34,40d' document.py

# run test
WORKDIR /opt
ADD test.py .
RUN pipenv run python test.py

# package lambda layer
WORKDIR /opt
RUN zip -r weasyprint-py38x.zip fonts lib python
```

[OG gist](https://gist.github.com/cpmech/b48729ea07e575d678698bb116d1cbba#file-build-weasyprint-python3-8-lambda-layer-md)
https://github.com/Kozea/WeasyPrint/issues/1003
