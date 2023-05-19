FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV PYTHONPATH /code
# Set the working directory in the container
WORKDIR /code


# Install virtual environment tool
RUN pip install virtualenv

# Create and activate a virtual environment
RUN virtualenv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file
COPY requirements.txt /code/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . /code/

# Run any additional setup commands (if needed)
# For example, you can run migrations or collect static files here
EXPOSE 8000
# Start the application
CMD ["python", "manage.py", "runserver", "--settings=NoraWallet.Settings.staging", "0.0.0.0:8000"]
