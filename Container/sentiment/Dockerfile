FROM python:3.10.12-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy the source code into the container.
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Run the application.
CMD ["python", "app.py"]