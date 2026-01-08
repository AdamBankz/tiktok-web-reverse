import json
import random
import re
import time
import requests

X_BOGUS = "fill"
X_GNARLY = "fill"


def CompressLzw(data: str) -> list[int]:
    codebook = {chr(i): i for i in range(256)}
    bit_index = 0
    buffer = 0
    output = []
    bit_length = 8
    next_code = 256

    def _flush_buffer():
        nonlocal buffer, bit_index, output
        output.append(buffer)
        buffer = 0
        bit_index = 0

    def _write_bits(code: int, length: int):
        nonlocal buffer, bit_index
        for _ in range(length):
            if code & 1:
                buffer |= 1 << bit_index
            code >>= 1
            bit_index += 1
            if bit_index == 8:
                _flush_buffer()

    index = 0
    while index < len(data):
        chunk = data[index]
        while index + 1 < len(data) and chunk + data[index + 1] in codebook:
            index += 1
            chunk += data[index]

        code = codebook[chunk]
        _write_bits(code, bit_length)

        if index + 1 < len(data):
            next_code += 1
            new_chunk = chunk + data[index + 1]
            codebook[new_chunk] = next_code

            if (next_code & (next_code - 1)) == 0:
                bit_length += 1

        index += 1

    if bit_index > 0:
        _flush_buffer()

    return output

def CompressBytes(data: str) -> bytes:
    return bytes(CompressLzw(data))


def Bb64(s):
    base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    b64 = []

    pad = (3 - len(s) % 3) % 3
    s += "\x00" * pad  # 填充空字节

    for i in range(0, len(s), 3):
        b = (ord(s[i]) << 16) + (ord(s[i + 1]) << 8) + ord(s[i + 2])
        b64.append(base64chars[(b >> 18) & 63])
        b64.append(base64chars[(b >> 12) & 63])
        b64.append(base64chars[(b >> 6) & 63])
        b64.append(base64chars[b & 63])

    if pad:
        b64 = b64[:-pad]
        b64 += ["="] * pad

    return "".join(b64)


def B64Shift(b64_string):
    return re.sub(
        r"[A-Za-z0-9+/=]",
        lambda shift_table: "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="[
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".index(
                shift_table.group(0)
            )
        ],
        b64_string,
    )
from py_mini_racer import py_mini_racer



js_code = """
function yg18(e, t, r, n, o) {
    var ob;
    ob = [16, 12, 8, 7],
        (e[t] += e[r],
            e[o] = yg41(e[o] ^ e[t], ob[0]),
            e[n] += e[o],
            e[r] = yg41(e[r] ^ e[n], ob[1]),
            e[t] += e[r],
            e[o] = yg41(e[o] ^ e[t], ob[2]),
            e[n] += e[o],
            e[r] = yg41(e[r] ^ e[n], ob[3]))
}
function yg23(e) {
    var pb;
    pb = [12, 4294967295, 1],
        e[pb[0]] = e[pb[0]] + pb[2] & pb[1]
}

function yg33(e, t) {
    var r;
    r = e['slice'](),
        !function (e, t) {
            for (var r = 0; r < t && (yg18(e, 0, 4, 8, 12),
                yg18(e, 1, 5, 9, 13),
                yg18(e, 2, 6, 10, 14),
                yg18(e, 3, 7, 11, 15),
                !(++r >= t)); ++r)
                yg18(e, 0, 5, 10, 15),
                    yg18(e, 1, 6, 11, 12),
                    yg18(e, 2, 7, 12, 13),
                    yg18(e, 3, 4, 13, 14)
        }(r, t);
    for (var n = 0; n < 16; ++n)
        r[n] += e[n];
    return r
}

function yg41(e, t) {
    var nb;
    return nb = [32],
        e << t | e >>> nb[0] - t
}

function vvv(e, t, r) {
    var qb;
    qb = [0];
    for (var n = Math['floor'](r['length'] / 4), o = r['length'] % 4, i = Math['floor']((r['length'] + 3) / 4), u = Array(i), a = 0; a < n; ++a) {
        var s = 4 * a;
        u[a] = r[s] | r[s + 1] << 8 | r[s + 2] << 16 | r[s + 3] << 24
    }
    if (o > qb[0]) {
        u[a] = 0;
        for (var c = 0; c < o; ++c)
            u[a] |= r[4 * a + c] << 8 * c
    }
    for (function (e, t, r) {
        for (var n = e['slice'](), o = 0; o + 16 < r['length']; o += 16) {
            var i = yg33(n, t);
            yg23(n);
            for (var u = 0; u < 16; ++u)
                r[o + u] ^= i[u]
        }
        for (var a = r['length'] - o, s = yg33(n, t), c = 0; c < a; ++c)
            r[o + c] ^= s[c]
    }(e, t, u),
        a = 0; a < n; ++a) {
        var f = 4 * a;
        r[f] = 255 & u[a],
            r[f + 1] = u[a] >>> 8 & 255,
            r[f + 2] = u[a] >>> 16 & 255,
            r[f + 3] = u[a] >>> 24 & 255
    }
    if (o > qb[0])
        for (var d = 0; d < o; ++d)
            r[4 * a + d] = u[a] >>> 8 * d & 255
}

function encode(key, d) {
    m = [
        1196819126,
        600974999,
        3863347763,
        1451689750,
    ].concat(key)

    c = 0

    for (let i of m.slice(4,)) {
        c += i & 15
        c &= 15
    }
    c += 5

    vvv(m, c, d)

    lst = []

    for (let i of m.slice(4,)) {
        lst.push(i & 255)
        lst.push(i >> 8 & 255)
        lst.push(i >> 16 & 255)
        lst.push(i >> 24 & 255)
    }

    subIndex = 0

    for (let i of lst) {
        subIndex += i
        subIndex %= d.length + 1
    }

    for (let i of d) {
        subIndex += i
        subIndex %= d.length + 1
    }

    _str = String.fromCharCode.apply(String, d)

    v = _str.substring(0, subIndex)
    vv = _str.slice(subIndex)
    lst_str = String.fromCharCode.apply(String, lst)

    new_str = v + lst_str + vv

    return new_str
}
"""


def GetStrData(raw):

    com = py_mini_racer.MiniRacer()
    com.eval(js_code)
    raw_str = json.dumps(raw, ensure_ascii=False, separators=(",", ":"))
    raw_str_bytes = CompressBytes(raw_str)

    key = [
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
        int(random.random() * 4294967296),
    ]

    _e = chr(76) + com.call("encode", key, [i for i in raw_str_bytes])

    return B64Shift(Bb64(_e))

RAW = {
        "tokenList": [],
        "navigator": {
            "appCodeName": "Mozilla",
            "appMinorVersion": "undefined",
            "appName": "Netscape",
            "appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "buildID": "undefined",
            "doNotTrack": "null",
            "msDoNotTrack": "undefined",
            "oscpu": "undefined",
            "platform": "Win32",
            "product": "Gecko",
            "productSub": "20030107",
            "cpuClass": "undefined",
            "vendor": "Google Inc.",
            "vendorSub": "",
            "deviceMemory": "8",
            "language": "en-US",
            "systemLanguage": "undefined",
            "userLanguage": "undefined",
            "webdriver": "false",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "hardwareConcurrency": 16,
            "maxTouchPoints": 0,
            "cookieEnabled": 1,
            "vibrate": 3,
            "credentials": 99,
            "storage": 99,
            "requestMediaKeySystemAccess": 3,
            "bluetooth": 99,
            "languages": "en-US",
            "online": "true",
            "touchEvent": 2,
            "touchstart": 2,
        },
        "wID": {
            "permState": "",
            "load": 3,
            "nativeLength": 33,
            "nativeName": 2,
            "jsFontsList": "3f",
            "syntaxError": "-1",
            "timestamp": "1747298188984",
            "timezone": 8,
            "magic": 3,
            "canvas": "4064376428",
            "wProps": 374198,
            "dProps": 2,
            "jsv": "",
            "browserType": 16,
            "iframe": 2,
            "pppt": 2,
            "rtt": 2,
            "notifyPerm": "default",
            "sdkVersion": "5.1.0",
            "scmVersion": "1.0.0.290",
            "aid": 1988,
            "msgType": 1,
            "privacyMode": 516,
            "aidList": [1988, 368462],
            "isf": 2,
            "env": "1111111111111111111111111",
            "propLength": {"a": 1218, "b": 1181, "c": 976, "d": 10, "e": 979, "f": 0},
            "objProx": "11111111111111111",
            "sri": 1,
            "ucwd": "111",
            "dups": 1,
            "hl": 2,
            "tz": "Asia/Shanghai",
            "tzS": "latn",
            "tzC": "gregory",
            "tzL": "en-US",
            "perf": {
                "cE": "1747298184496",
                "cS": "1747298184108",
                "dC": "0",
                "dCEE": "1747298185113",
                "dCES": "1747298185113",
                "dI": "1747298185113",
                "dL": "1747298184897",
                "dLE": "1747298184107",
                "dLS": "1747298184107",
                "fS": "1747298184107",
                "lEE": "0",
                "lES": "0",
                "nS": "1747298184088",
                "rE": "0",
                "rS": "0",
                "reqS": "1747298184497",
                "resE": "1747298184971",
                "resS": "1747298184893",
                "sCS": "1747298184108",
                "uEE": "0",
                "uES": "0",
            },
            "iframeInfo": {
                "iFrameNP": {
                    "uA": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                    "platform": "Win32",
                    "hC": 16,
                    "lang": "en-US",
                    "wd": "false",
                },
                "iFrameSP": {"aH": 1440, "aW": 3440, "h": 1440, "w": 3440, "pD": 24},
                "propHash": "93475812381",
            },
            "bb": {"a": 953, "b": 912, "c": 1},
            "aFP": "1038527147",
            "intP": 1.1459861526630101e23,
            "index": 79,
        },
        "window": {
            "Image": 3,
            "isSecureContext": 1,
            "ActiveXObject": 4,
            "toolbar": 99,
            "locationbar": 99,
            "external": 99,
            "mozRTCPeerConnection": 4,
            "postMessage": 3,
            "webkitRequestAnimationFrame": 3,
            "BluetoothUUID": 3,
            "netscape": 4,
            "localStorage": 99,
            "sessionStorage": 99,
            "indexedDB": 99,
            "devicePixelRatio": 1,
            "devicePixelRatioFloat": 1,
            "location": "https://www.tiktok.com/en/",
        },
        "webgl": {
            "supportedExtensions": [
                "ANGLE_instanced_arrays",
                "EXT_blend_minmax",
                "EXT_clip_control",
                "EXT_color_buffer_half_float",
                "EXT_depth_clamp",
                "EXT_disjoint_timer_query",
                "EXT_float_blend",
                "EXT_frag_depth",
                "EXT_polygon_offset_clamp",
                "EXT_shader_texture_lod",
                "EXT_texture_compression_bptc",
                "EXT_texture_compression_rgtc",
                "EXT_texture_filter_anisotropic",
                "EXT_texture_mirror_clamp_to_edge",
                "EXT_sRGB",
                "KHR_parallel_shader_compile",
                "OES_element_index_uint",
                "OES_fbo_render_mipmap",
                "OES_standard_derivatives",
                "OES_texture_float",
                "OES_texture_float_linear",
                "OES_texture_half_float",
                "OES_texture_half_float_linear",
                "OES_vertex_array_object",
                "WEBGL_blend_func_extended",
                "WEBGL_color_buffer_float",
                "WEBGL_compressed_texture_s3tc",
                "WEBGL_compressed_texture_s3tc_srgb",
                "WEBGL_debug_renderer_info",
                "WEBGL_debug_shaders",
                "WEBGL_depth_texture",
                "WEBGL_draw_buffers",
                "WEBGL_lose_context",
                "WEBGL_multi_draw",
                "WEBGL_polygon_mode",
            ],
            "antialias": 1,
            "blueBits": 8,
            "depthBits": 24,
            "greenBits": 8,
            "maxAnisotropy": 16,
            "maxCombinedTextureImageUnits": 32,
            "maxCubeMapTextureSize": 16384,
            "maxFragmentUniformVectors": 1024,
            "maxRenderbufferSize": 16384,
            "maxTextureImageUnits": 16,
            "maxTextureSize": 16384,
            "maxVaryingVectors": 30,
            "maxVertexAttribs": 16,
            "maxVertexTextureImageUnits": 16,
            "maxVertexUniformVectors": 4095,
            "shadingLanguageVersion": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
            "stencilBits": 0,
            "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
            "vendor": "Google Inc. (NVIDIA)",
            "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 (0x00001C81) Direct3D11 vs_5_0 ps_5_0, D3D11)",
        },
        "document": {
            "characterSet": "UTF-8",
            "compatMode": "CSS1Compat",
            "documentMode": "undefined",
            "URL": "https://www.tiktok.com/en/",
            "layers": 4,
            "all": 12,
            "images": 99,
        },
        "screen": {
            "innerWidth": 3440,
            "innerHeight": 1351,
            "outerWidth": 3440,
            "outerHeight": 1440,
            "screenX": 0,
            "screenY": 0,
            "pageXOffset": 0,
            "pageYOffset": 0,
            "availWidth": 3440,
            "availHeight": 1440,
            "sizeWidth": 3440,
            "sizeHeight": 1440,
            "clientWidth": 3440,
            "clientHeight": 1351,
            "colorDepth": 24,
            "pixelDepth": 24,
            "focus": 2,
            "hidden": 2,
            "visibilityState": "visible",
            "location": 1,
            "menubar": 1,
            "scrollbar": 0,
            "orientation": "landscape-primary",
        },
        "plugins": {
            "plugin": [
                "internal-pdf-viewer|application/pdf|pdf",
                "internal-pdf-viewer|text/pdf|pdf",
                "internal-pdf-viewer|application/pdf|pdf",
                "internal-pdf-viewer|text/pdf|pdf",
                "internal-pdf-viewer|application/pdf|pdf",
                "internal-pdf-viewer|text/pdf|pdf",
                "internal-pdf-viewer|application/pdf|pdf",
                "internal-pdf-viewer|text/pdf|pdf",
                "internal-pdf-viewer|application/pdf|pdf",
                "internal-pdf-viewer|text/pdf|pdf",
            ],
            "pv": "0",
            "proto": 1,
        },
        "custom": {},
        "canvasIntegrity": {
            "a": 1,
            "b": 1,
            "c": 1,
            "d": ["1199217862", "1199217862"],
            "e": 1,
        },
        "mediaQuery": {
            "dppx": 1,
            "orientation": "landscape",
            "hover": "hover",
            "anyPointer": "fine",
            "maxHeight": 1351,
            "maxWidth": 3440,
            "dpi": 96,
        },
        "battery": {
            "charging": 1,
            "level": 100,
            "chargingTime": "0",
            "dischargingTime": "Infinity",
        },
        "msgMeta": {
            "msgType": 1,
            "msgSrcProp": 1,
            "msgProtocol": 1,
            "aid": 1988,
            "aidList": [1988, 368462],
        },
        "customInit": {"ttwid": "7504192365256590856"},
    }











        

        
    




    








    





    











    


    

    


import requests
import json
import time

DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://www.tiktok.com",
    "Referer": "https://www.tiktok.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="139", "Google Chrome";v="139", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

def BuildPayload():
    return {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": GetStrData(RAW),
        "tspFromClient": int(time.time() * 1000)
    }

def BuildQueryParams(ms_token, user_agent, canvas_value, sdk_version):
    query = f"msToken={ms_token}" if ms_token else "msToken="
    x_bogus_val = X_BOGUS.get_x_bougs(query, user_agent, canvas_value)
    body = json.dumps(BuildPayload(), separators=(',', ':'))
    x_gnarly_val = X_GNARLY.get_X_Gnarly(
        f"msToken={ms_token}&X-Bogus={x_bogus_val}" if ms_token else f"msToken=&X-Bogus={x_bogus_val}",
        body,
        user_agent,
        canvas_value,
        int(time.time()),
        sdk_version
    )
    return {
        "msToken": ms_token or "",
        "X-Bogus": x_bogus_val,
        "X-Gnarly": x_gnarly_val
    }

def SendTikTokReport():
    url = "https://mssdk-va.tiktok.com/web/report"
    headers = {**DEFAULT_HEADERS, "Host": "mssdk-va.tiktok.com"}
    user_agent = RAW["navigator"]["userAgent"]
    canvas_value = int(RAW["wID"].get("canvas", 0))
    sdk_version = RAW["wID"].get("sdkVersion", "5.1.0")

    params = BuildQueryParams(None, user_agent, canvas_value, sdk_version)
    full_url = f"{url}?msToken={params['msToken']}&X-Bogus={params['X-Bogus']}&X-Gnarly={params['X-Gnarly']}"
    
    try:
        response = requests.post(full_url, headers=headers, json=BuildPayload(), timeout=10)
        token = response.headers.get("X-Ms-Token")
        if not token:
            set_cookie = response.headers.get("Set-Cookie", "")
            for part in set_cookie.split(";"):
                if part.strip().startswith("msToken="):
                    token = part.strip().split("=", 1)[1]
                    break
        print("Extracted msToken:", token)
        return token
    except Exception as e:
        print("Request failed:", e)
        return None

def GetMsToken(tt_csrf_token, ttwid, passport_csrf_token):
    url = "https://mssdk-sg.tiktok.com/web/report"
    user_agent = RAW["navigator"]["userAgent"]
    canvas_value = int(RAW["wID"].get("canvas", 0))
    sdk_version = RAW["wID"].get("sdkVersion", "5.1.0")

    try:
        with requests.session() as sess:
            ms_token = SendTikTokReport()
            if not ms_token:
                print("Initial request failed to retrieve msToken")
                return None

            headers = {
                **DEFAULT_HEADERS,
                "Host": "mssdk-sg.tiktok.com",
                "Cookie": (
                    f"tt_csrf_token={tt_csrf_token}; "
                    f"ttwid={ttwid}; "
                    f"passport_csrf_token={passport_csrf_token}; "
                    f"passport_csrf_token_default={passport_csrf_token}; "
                    f"msToken={ms_token}"
                )
            }
            params = BuildQueryParams(ms_token, user_agent, canvas_value, sdk_version)
            response = sess.post(url, headers=headers, params=params, json=BuildPayload(), timeout=10, verify=False)
            ms_token = sess.cookies.get("msToken")
            if not ms_token:
                print("Second request failed to retrieve msToken")
                return None

            headers = {
                **DEFAULT_HEADERS,
                "Host": "mssdk-sg.tiktok.com",
                "Cookie": (
                    f"tt_csrf_token={tt_csrf_token}; "
                    f"ttwid={ttwid}; "
                    f"passport_csrf_token={passport_csrf_token}; "
                    f"passport_csrf_token_default={passport_csrf_token}; "
                    f"msToken={ms_token}"
                )
            }
            params = BuildQueryParams(ms_token, user_agent, canvas_value, sdk_version)
            response = sess.post(url, headers=headers, params=params, json=BuildPayload(), timeout=10, verify=False)
            ms_token = sess.cookies.get("msToken")
            if not ms_token:
                print("Third request failed to retrieve msToken")
                return None

            headers = {
                **DEFAULT_HEADERS,
                "Host": "mssdk-sg.tiktok.com",
                "Cookie": (
                    f"tt_csrf_token={tt_csrf_token}; "
                    f"ttwid={ttwid}; "
                    f"passport_csrf_token={passport_csrf_token}; "
                    f"passport_csrf_token_default={passport_csrf_token}; "
                    f"msToken={ms_token}"
                )
            }
            params = BuildQueryParams(ms_token, user_agent, canvas_value, sdk_version)
            response = sess.post(url, headers=headers, params=params, json=BuildPayload(), timeout=10, verify=False)
            ms_token = sess.cookies.get("msToken")
            if not ms_token:
                print("Fourth request failed to retrieve msToken")
                return None

            return ms_token
    except Exception as e:
        print("Request failed:", e)
        return None

    


    


if __name__ == "__main__":
    print(GetStrData(RAW))
