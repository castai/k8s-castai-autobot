FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY src/ .

# Install curl
RUN apk --no-cache add curl

# Make the script executable
RUN chmod +x script.sh

# Set the entry point to the bash script
ENTRYPOINT ["./script_example.sh"]
