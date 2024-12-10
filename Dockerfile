FROM python:latest
WORKDIR /myapp
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app","--reload","--port=8000","--host=0.0.0.0"]