FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Set WORKDIR to djproject directly
WORKDIR /app/djproject

# ✅ Copy only djproject folder contents
COPY . /app/djproject

# ✅ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# ✅ manage.py is NOW in the working directory
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
