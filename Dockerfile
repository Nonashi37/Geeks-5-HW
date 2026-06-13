# 1. Use an official, lightweight Python image
FROM python:3.12-slim

# 2. Set environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project code into the container
COPY . /app/

# 7. Expose the port Django runs on
EXPOSE 8000

# 8. Default command to run our server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# just to ckeck