# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Prevent Python from writing .pyc files and make logs unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8082

# Set working directory
WORKDIR /app

# Copy your app file into the container
COPY python.py /app/

# Create a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# Expose the port
EXPOSE 8082

# Healthcheck (optional but good practice)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,os,sys; p=os.getenv('PORT','8082'); \
try: r=urllib.request.urlopen(f'http://127.0.0.1:{p}/', timeout=2); sys.exit(0 if r.status==200 else 1) \
except Exception: sys.exit(1)"

# Command to run your app
CMD ["python", "python.py"]
