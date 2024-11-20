FROM python:3.12

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# FROM python:3.10-slim

# WORKDIR /app

# COPY . .

# EXPOSE 8000

# RUN pip install -r requirements.txt

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
