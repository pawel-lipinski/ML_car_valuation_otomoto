FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional, depending on your packages)
RUN apt-get update && apt-get install -y build-essential

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_otomoto.py", "--server.port=8501", "--server.address=0.0.0.0"]
