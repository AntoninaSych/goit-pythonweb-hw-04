FROM python:3.10
WORKDIR /app
COPY requirements.txt .
COPY sort_files.py .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "sort_files.py"]
