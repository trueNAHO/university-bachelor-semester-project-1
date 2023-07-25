# Set base image.
FROM python:3-slim

# Install dependencies.
RUN apt-get update && apt-get install --yes gnupg
RUN pip install npyscreen python-gnupg

# Set the working directory.
WORKDIR /root/src

# Copy entire code base.
ADD src .

# Execute the application.
CMD ["python", "main.py"]
