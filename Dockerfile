FROM python:3.10-alpine

EXPOSE 5000

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]