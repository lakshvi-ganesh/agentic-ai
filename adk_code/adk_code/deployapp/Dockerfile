FROM python:3.13-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

ENTRYPOINT ["uvicorn"]

CMD ["deployapp:app","--host","0.0.0.0","--port","8085"]