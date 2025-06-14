# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r djangofw.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]