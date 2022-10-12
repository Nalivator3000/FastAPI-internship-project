FROM python

COPY ./scr /app/scr
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "scr.main:app", "--host=0.0.0.0", "--port", "8000", "--reload"]