import base64
import falcon
import os

class HTTPBasicAuth:
    def process_request(self, req, resp):
        auth = req.get_header("Authorization")

        if not auth or not auth.startswith("Basic "):
            raise falcon.HTTPUnauthorized(
                title="Authentication Required",
                description="Provide valid credentials",
                challenges=["Basic realm='Access to the Falcon API'"]
            )

        encoded_credentials = auth.split(" ")[1]
        try:
            decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        except Exception:
            raise falcon.HTTPUnauthorized(
                title="Invalid auth encoding",
                challenges=["Basic realm='Access to the Falcon API'"]
            )

        username, password = decoded.split(":", 1)

        expected_user = os.environ.get("FALCON_USER")
        expected_pass = os.environ.get("FALCON_PASSWORD")

        if username != expected_user or password != expected_pass:
            raise falcon.HTTPUnauthorized(
                title="Invalid credentials",
                challenges=["Basic realm='Access to the Falcon API'"]
            )
