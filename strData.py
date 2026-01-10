import json
import random
import re
import time
from py_mini_racer import py_mini_racer


def LzwCompress(data: str) -> list[int]:
    dictionary = {chr(i): i for i in range(256)}
    bitPosition = 0
    tempBuffer = 0
    resultList = []
    bitSize = 8
    nextIndex = 256

    def _flush_buffer():
        nonlocal tempBuffer, bitPosition, resultList
        resultList.append(tempBuffer)
        tempBuffer = 0
        bitPosition = 0

    def _write_bits(codeValue: int, length: int):
        nonlocal tempBuffer, bitPosition
        for _ in range(length):
            if codeValue & 1:
                tempBuffer |= 1 << bitPosition
            codeValue >>= 1
            bitPosition += 1
            if bitPosition == 8:
                _flush_buffer()

    position = 0
    while position < len(data):
        substring = data[position]
        while position + 1 < len(data) and substring + data[position + 1] in dictionary:
            position += 1
            substring += data[position]

        codeValue = dictionary[substring]
        _write_bits(codeValue, bitSize)

        if position + 1 < len(data):
            nextIndex += 1
            newSubstring = substring + data[position + 1]
            dictionary[newSubstring] = nextIndex

            if (nextIndex & (nextIndex - 1)) == 0:
                bitSize += 1

        position += 1

    if bitPosition > 0:
        _flush_buffer()

    return resultList

def BytesCompress(data: str) -> bytes:
    return bytes(LzwCompress(data))


def EncodeBase64(inputStr):
    base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encodedList = []

    padding = (3 - len(inputStr) % 3) % 3
    inputStr += "\x00" * padding  # 填充空字节

    for i in range(0, len(inputStr), 3):
        combined = (ord(inputStr[i]) << 16) + (ord(inputStr[i + 1]) << 8) + ord(inputStr[i + 2])
        encodedList.append(base64chars[(combined >> 18) & 63])
        encodedList.append(base64chars[(combined >> 12) & 63])
        encodedList.append(base64chars[(combined >> 6) & 63])
        encodedList.append(base64chars[combined & 63])

    if padding:
        encodedList = encodedList[:-padding]
        encodedList += ["="] * padding

    return "".join(encodedList)


def ShiftBase64(base64Str):
    return re.sub(
        r"[A-Za-z0-9+/=]",
        lambda replacement: "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="[
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".index(
                replacement.group(0)
            )
        ],
        base64Str,
    )


jsScript = """
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
    r = e['slice']()
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


def RetrieveStrData(raw):

    jsEngine = py_mini_racer.MiniRacer()
    jsEngine.eval(jsScript)
    jsonString = json.dumps(raw, ensure_ascii=False, separators=(",", ":"))
    compressedBytes = BytesCompress(jsonString)

    encryptionKey = [
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

    encodedResult = chr(76) + jsEngine.call("encode", encryptionKey, [i for i in compressedBytes])

    return ShiftBase64(EncodeBase64(encodedResult))

BROWSER_DATA = {
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


if __name__ == "__main__":
    print(RetrieveStrData(BROWSER_DATA))