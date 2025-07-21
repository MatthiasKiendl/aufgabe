# This Dockerfile sets up a Python 3.13.5 environment using the slim Bookworm image.
# It sets the working directory to /app and copies all files from the build context into the container.
# The required Python packages are installed from req.txt.
# The container starts a WSGI application using waitress-serve on port 8000, with the entry point defined in wsgi:app.
FROM python:3.13.5-slim-bookworm
WORKDIR /app
COPY . .
RUN pip install -r req.txt
CMD ["waitress-serve", "--port=8000", "wsgi:app"]
