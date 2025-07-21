FROM python:3.13.5-slim-bookworm
WORKDIR /app
COPY . .
RUN pip install -r req.txt
CMD ["waitress-serve", "--port=8000", "wsgi:app"]
