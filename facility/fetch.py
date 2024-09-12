import logging
import random
import time
from io import BytesIO
from typing import Callable, Dict, Optional, Tuple, Union

from curl_cffi import requests

from external_api.proxy import get_proxy


def requests_retry(
    url: str,
    params: dict = None,
    retry: int = 1,
    impersonate: str = "chrome110",
    headers: dict = None,
    hook: Callable[[str], Tuple[bool, str]] = None,
    disable_proxy: bool = False,
    http_version=None,
    http_method: str = "GET",
    data: Optional[Union[Dict[str, str], str, BytesIO, bytes]] = None,
    json: Optional[dict] = None,
    timeout: Union[float, Tuple[float, float]] = 30,
    dynamic_uas: list = None,
    proxy_name: str = "offline",
    return_response: bool = False,
    allow_redirects: bool = True,
) -> Union[str, dict, bytes, list]:
    c = 0
    proxies = None
    while c <= retry:
        start_t = time.time() * 1000
        r = None
        try:
            logging.info(f"requests_get_retry. c : {c} ; url : {url}")
            if not disable_proxy:
                if proxy_name == "random":
                    proxy_name = random.choice(
                        ["offline", "online", "deadlink-check", "google"]
                    )
                proxies = get_proxy(proxy_name)
            if dynamic_uas:
                headers = headers if headers else {}
                headers["user-agent"] = dynamic_uas[
                    random.randint(0, len(dynamic_uas) - 1)
                ]
            r = requests.request(
                method=http_method,
                url=url,
                params=params,
                impersonate=impersonate,
                proxies=proxies,
                headers=headers,
                http_version=http_version,
                data=data,
                json=json,
                timeout=timeout,
                allow_redirects=allow_redirects,
            )

            if return_response:
                return r
            r.raise_for_status()
            ret = None
            content_type = r.headers.get("content-type")
            content_type = content_type.lower() if content_type else content_type
            if http_method == "HEAD":
                ret = r.headers._list
            elif content_type and (
                content_type in ["application/pdf", "application/octet-stream"]
                or any(
                    [
                        content_type.startswith(kw)
                        for kw in ["image/", "video/", "audio/"]
                    ]
                )
            ):
                ret = r.content
            else:
                ret = r.text
            if hook:
                ok, ret = hook(ret)
                if not ok:
                    raise ValueError(f"hook opt fail, proxies : {proxies} ; url={url}")
            return ret
        except Exception as e:
            if c < retry:
                c += 1
                continue
            if r:
                logging.error(
                    f"requests_retry fail. proxies : {proxies} ; url : {url} ; status code : {r.status_code} ; html : {r.text} ; err : {e}"
                )
            else:
                logging.error(
                    f"requests_retry fail. proxies : {proxies} url : {url} ; err : {e}"
                )
            raise e
        finally:
            end_t = time.time() * 1000
            logging.info(
                f"requests_{http_method}_retry. c : {c} ; proxies : {proxies} ; url : {url} ; headers: {headers} ; cost : {'%.2f' % (end_t - start_t)}ms"
            )


def requests_get_retry(
    url: str,
    params: dict = None,
    retry: int = 1,
    impersonate: str = "chrome110",
    headers: dict = None,
    hook: Callable[[str], Tuple[bool, str]] = None,
    disable_proxy: bool = False,
    http_version=None,
    timeout: Union[float, Tuple[float, float]] = 30,
    dynamic_uas: list = None,
    proxy_name: str = "offline",
    return_response: bool = False,
    allow_redirects: bool = True,
) -> Union[str, dict, bytes]:
    return requests_retry(
        url=url,
        params=params,
        retry=retry,
        impersonate=impersonate,
        headers=headers,
        hook=hook,
        disable_proxy=disable_proxy,
        http_version=http_version,
        timeout=timeout,
        dynamic_uas=dynamic_uas,
        proxy_name=proxy_name,
        return_response=return_response,
        allow_redirects=allow_redirects,
    )


def requests_post_retry(
    url: str,
    retry: int = 1,
    impersonate: str = "chrome110",
    headers: dict = None,
    hook: Callable[[str], Tuple[bool, str]] = None,
    disable_proxy: bool = False,
    http_version=None,
    data: Optional[Union[Dict[str, str], str, BytesIO, bytes]] = None,
    json: Optional[dict] = None,
    timeout: Union[float, Tuple[float, float]] = 30,
    dynamic_uas: list = None,
    proxy_name: str = "offline",
    allow_redirects: bool = True,
    return_response: bool = False,
) -> Union[str, dict, bytes]:
    return requests_retry(
        url=url,
        retry=retry,
        impersonate=impersonate,
        headers=headers,
        hook=hook,
        disable_proxy=disable_proxy,
        http_version=http_version,
        http_method="POST",
        data=data,
        json=json,
        timeout=timeout,
        dynamic_uas=dynamic_uas,
        proxy_name=proxy_name,
        allow_redirects=allow_redirects,
        return_response=return_response,
    )


def requests_head_retry(
    url: str,
    retry: int = 1,
    impersonate: str = "chrome110",
    headers: dict = None,
    hook: Callable[[str], Tuple[bool, str]] = None,
    disable_proxy: bool = False,
    http_version=None,
    data: Optional[Union[Dict[str, str], str, BytesIO, bytes]] = None,
    json: Optional[dict] = None,
    timeout: Union[float, Tuple[float, float]] = 30,
    dynamic_uas: list = None,
    proxy_name: str = "offline",
    return_response: bool = False,
    allow_redirects: bool = True,
) -> Union[str, dict, bytes]:
    return requests_retry(
        url=url,
        retry=retry,
        impersonate=impersonate,
        headers=headers,
        hook=hook,
        disable_proxy=disable_proxy,
        http_version=http_version,
        http_method="HEAD",
        data=data,
        json=json,
        timeout=timeout,
        dynamic_uas=dynamic_uas,
        proxy_name=proxy_name,
        return_response=return_response,
        allow_redirects=allow_redirects,
    )
