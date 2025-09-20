FROM python:2-slim

# Set working directory
WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start development server by default
ENTRYPOINT ["python", "build.py"]
CMD ["test"]
