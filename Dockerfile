# Set base image
FROM python:3.7-buster

# Set working directory
# WORKDIR /app

# Copy project requirements file
COPY requirements.txt .

# Install packages from the requirements file
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy project
COPY . .

# Set default startup command
CMD python dash/__init__.py