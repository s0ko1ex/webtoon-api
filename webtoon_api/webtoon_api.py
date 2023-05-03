from __future__ import annotations

import json
import urllib.parse

import requests
import requests.models
from Crypto.Hash import HMAC, SHA1

from .exceptions import *

api_key = b"gUtPzJFZch4ZyAGviiyH94P99lQ3pFdRTwpJWDlSGFfwgpr6ses5ALOxWHOIT7R1"
user_agent = "nApps (Android 13; linewebtoon; 2.12.2)"


class WebtoonApiCall:
    def __init__(self, api: WebtoonApi, name: str) -> None:
        self.api = api
        self.name = name

    def __call__(self, **kwargs) -> dict:
        url = f"https://global.apis.naver.com/lineWebtoon/webtoon/{self.name}"
        request = requests.models.PreparedRequest()
        request.prepare(url=url, params=kwargs)

        if request.url is None:
            raise ValueError("Error in parameters")

        return self.api.get_request(request.url)


class WebtoonApi:
    def __m26922a(self, bArr: bytes) -> str:
        length = len(bArr)
        i = length // 3
        i2 = length - (i * 3)
        stringBuffer = []
        cArr = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "+",
            "/",
        ]
        i3 = 0
        i4 = 0

        NETWORK_LOAD_LIMIT_DISABLED = 255

        while i3 < i:
            i5 = i4 + 1
            i6 = bArr[i4] & NETWORK_LOAD_LIMIT_DISABLED
            i7 = i5 + 1
            i8 = bArr[i5] & NETWORK_LOAD_LIMIT_DISABLED
            i9 = i7 + 1
            i10 = bArr[i7] & NETWORK_LOAD_LIMIT_DISABLED
            stringBuffer.append(cArr[i6 >> 2])
            stringBuffer.append(cArr[((i6 << 4) & 63) | (i8 >> 4)])
            stringBuffer.append(cArr[((i8 << 2) & 63) | (i10 >> 6)])
            stringBuffer.append(cArr[i10 & 63])
            i3 += 1
            i4 = i9

        if i2 != 0:
            i11 = i4 + 1
            i12 = bArr[i4] & NETWORK_LOAD_LIMIT_DISABLED
            stringBuffer.append(cArr[i12 >> 2])
            if i2 == 1:
                stringBuffer.append(cArr[(i12 << 4) & 63])
                stringBuffer.append("==")
            else:
                i13 = bArr[i11] & NETWORK_LOAD_LIMIT_DISABLED
                stringBuffer.append(cArr[((i12 << 4) & 63) | (i13 >> 4)])
                stringBuffer.append(cArr[(i13 << 2) & 63])
                stringBuffer.append("=")

        return "".join(stringBuffer)

    def __m2969c(self, s: bytes) -> str:
        mac = HMAC.new(api_key, s, digestmod=SHA1)
        return self.__m26922a(mac.digest())

    def get_signed_url(self, webtoon_url: str) -> str:
        url = webtoon_url.encode("utf-8")
        time = requests.get(
            "https://global.apis.naver.com/currentTime",
            headers={
                "User-Agent": user_agent,
            },
        ).content
        encode = self.__m2969c(url[:255] + time)

        request = requests.models.PreparedRequest()
        request.prepare(
            url=webtoon_url, params={"msgpad": time.decode(), "md": encode}
        )

        if request.url is None:
            raise ValueError("Error in parameters")

        return request.url

    def get_request(self, unsigned_url: str) -> dict:
        signed_url = self.get_signed_url(unsigned_url)
        response = json.loads(requests.get(signed_url).text)

        if response.get("error_code") is not None:
            if response["error_code"] == "025":
                raise TimeLimitError(response["message"])
            elif response["error_code"] == "024":
                raise AuthError(response["message"])

        return response["message"]["result"]

    def get_static_content(self, path: str) -> bytes:
        url = urllib.parse.urljoin("https://webtoon-phinf.pstatic.net", path)
        return requests.get(
            url,
            headers={
                "Referer": "http://m.webtoons.com/",
                "User-Agent": user_agent,
            },
        ).content

    def __getattr__(self, name: str) -> WebtoonApiCall:
        return WebtoonApiCall(self, name)
