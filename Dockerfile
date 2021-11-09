FROM python:3.8.8-slim-buster

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
