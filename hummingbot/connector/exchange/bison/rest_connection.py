import ssl

import aiohttp

from hummingbot.core.web_assistant.connections.data_types import RESTRequest, RESTResponse


class RESTConnection:
    def __init__(self, aiohttp_client_session: aiohttp.ClientSession, bison_cert_path: str = None):
        self._client_session = aiohttp_client_session
        self.bison_cert_path = bison_cert_path
        self._cookies = {}  # Dictionary to store cookies

    async def call(self, request: RESTRequest) -> RESTResponse:
        # Add stored cookies to the request headers, if any
        if not request.headers:
            request.headers = {}

        if self._cookies:
            cookie_str = "; ".join([f"{key}={value}" for key, value in self._cookies.items()])
            request.headers["Cookie"] = cookie_str

        # Make the HTTP request
        aiohttp_resp = await self._client_session.request(
            method=request.method.value,
            url=request.url,
            ssl=ssl.create_default_context(cafile=self.bison_cert_path),
            params=request.params,
            json=request.data,
            headers=request.headers,
        )

        # Capture and store any Set-Cookie headers from the response
        if "Set-Cookie" in aiohttp_resp.headers:
            cookies = aiohttp_resp.headers.getall("Set-Cookie", [])
            for cookie in cookies:
                cookie_pair = cookie.split(';', 1)[0]  # Take the key-value pair before ';'
                key, value = cookie_pair.split('=')
                self._cookies[key] = value

        resp = await self._build_resp(aiohttp_resp)
        return resp

    @staticmethod
    async def _build_resp(aiohttp_resp: aiohttp.ClientResponse) -> RESTResponse:
        resp = RESTResponse(aiohttp_resp)
        return resp
