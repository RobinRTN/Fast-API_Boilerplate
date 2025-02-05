FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# ENTRYPOINT ["./entrypoint.sh"]

# CMD ["gunicorn", "--worker-class", "eventlet", "-b", "0.0.0.0:5000", "app:app"]
# RUN THIS IF DB NOT THE SAME IN DEVELOPMENT AND PRODUCTION
# CMD ["sh", "-c", "flask db upgrade && gunicorn --worker-class eventlet -b 0.0.0.0:5000 app:app"]

#RUN THIS IF DB THE SAME BETWEEN BOTH
CMD ["sh", "-c", "flask db stamp head && gunicorn --worker-class eventlet -b 0.0.0.0:5000 app:app"]


# CMD ["python", "app.py"]