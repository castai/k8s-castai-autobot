# Use the latest available version of libexpat
FROM python:3.12.2-alpine

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY src/ .

# Remove existing version of libexpat
RUN apk --no-cache del expat \
# Install the desired version
&& apk --no-cache add expat=2.6.0-r0

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script
CMD ["sh", "-c", "python main.py && tail -f /dev/null"]
