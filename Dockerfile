FROM python:3.9-slim-buster

WORKDIR /app

COPY requirementsfastapi.txt .

RUN pip install --no-cache-dir -r requirementsfastapi.txt

COPY api.py .

EXPOSE 8080

# Set the command to run the FastAPI server when the container starts
CMD ["python api.py"]
