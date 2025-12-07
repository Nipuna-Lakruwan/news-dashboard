# Base Image
FROM python:3.9-slim

# Working Directory
WORKDIR /app

# Added prometheus-client for monitoring
RUN pip install streamlit redis prometheus-client

# Copy the app code
COPY app.py .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]