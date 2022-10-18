FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000