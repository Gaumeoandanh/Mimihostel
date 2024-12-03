# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container to /src
WORKDIR /src

# Add the current directory contents into the container at /src
ADD . /src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["streamlit", "run", "main.py", "--server.port", "8000"]