import keyring
import random
import webbrowser
import socket
import sys

import praw
from praw.util.token_manager import BaseTokenManager


class KeyringTokenManager(BaseTokenManager):
    def __init__(self):
        super().__init__()
        self.token = keyring.get_password("reddy", "reddy")

    def post_refresh_callback(self, authorizer):
        """Update the saved copy of the refresh token."""
        self.token = authorizer.refresh_token
        keyring.set_password("reddy", "reddy", authorizer.refresh_token)

    def pre_refresh_callback(self, authorizer):
        """Load the refresh token from the file."""
        if authorizer.refresh_token is None:
            if not self.token:
                self.token = keyring.get_password("reddy", "reddy")
            authorizer.refresh_token = self.token

    def set_token(self, token: str):
        self.token = token
        keyring.set_password("reddy", "reddy", token)


def get_refresh_token(reddit: praw.Reddit):
    """
    It opens a browser window, waits for the user to log in, and then returns the refresh token

    @param reddit The Reddit instance to use for the OAuth dance.

    @return The refresh token is being returned.
    """
    scopes: list[str] = ["*"]
    state: str = str(random.randint(0, 65000))
    url: str = reddit.auth.url(duration="permanent", scopes=scopes, state=state)
    webbrowser.open(url)

    client = receive_connection()
    data: str = client.recv(1024).decode("utf-8")
    param_tokens: list[str] = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params: dict = dict([token.split("=") for token in param_tokens])

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected: {state} Received: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token: str = reddit.auth.authorize(params["code"])  # type: ignore
    send_message(
        client, "Authorized. You may now close this tab and continue in the app"
    )

    return refresh_token


def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 13456, and waits for a single client.

    """
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 13456))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()
