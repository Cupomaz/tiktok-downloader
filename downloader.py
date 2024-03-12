import requests as req
import codecs
import headers as h

def getWebId(defPage):
    webIdIndex = defPage.text.find("webIdCreatedTime") + 19
    webIdCreatedTime = ""
    i = 0
    while defPage.text[webIdIndex + i] != '"':
        webIdCreatedTime = webIdCreatedTime + defPage.text[webIdIndex + i]
        i += 1
    return webIdCreatedTime

def getWid(defPage):
    widIndex = defPage.text.find('"wid"') + 7
    wid = ""
    i = 0
    while defPage.text[widIndex + i] != '"':
        wid = wid + defPage.text[widIndex + i]
        i += 1
    return wid

def getVideoUrl(defPage):
    videoIndex = defPage.text.find('"playAddr"') + 12
    videoUrl = ""
    i = 0
    while defPage.text[videoIndex + i] != '"':
        videoUrl = videoUrl + defPage.text[videoIndex + i]
        i += 1
    return codecs.decode(videoUrl, 'unicode-escape')

def downloadVideo(url): 
    s = req.Session()
    defPage = s.get(url, headers=h.defPageHeaders)
    
    print("Downloading video")

    aid = 1459

    # WebIdLastTime, aid, device_id
    odinUrl = 'https://www.tiktok.com/passport/web/account/info/?WebIdLastTime={}&aid={}&app_language=cs-CZ&app_name=tiktok_web&browser_language=cs-CZ&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F121.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_id={}&device_platform=web_pc&focus_state=true&from_page=video&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=CZ&screen_height=930&screen_width=1926&tz_name=Europe%2FPrague&webcast_language=cs-CZ'

    ttwid = s.cookies['ttwid']
    tt_csrf_token = s.cookies['tt_csrf_token']
    tt_chain_token = s.cookies['tt_chain_token']
    ak_bmsc = s.cookies['ak_bmsc']

    odinCookies = {
        "ttwid":ttwid,
        "tt_csrf_token":tt_csrf_token,
        "tt_chain_token":tt_chain_token,
        "ak_bmsc":ak_bmsc
    }

    odinCookiePage = s.get(odinUrl.format(getWebId(defPage), aid, getWid(defPage)), cookies=odinCookies)
    odin_tt = s.cookies["odin_tt"]

    # videoCookies = "ttwid={}; tt_csrf_token={}; tt_chain_token={}; ak_bmsc={}; odin_tt={}".format(ttwid, tt_csrf_token, tt_chain_token, ak_bmsc, odin_tt)

    videoCookies = {
        "ttwid":ttwid,
        "tt_csrf_token":tt_csrf_token,
        "tt_chain_token":tt_chain_token,
        "ak_bmsc":ak_bmsc,
        "odin_tt":odin_tt
    }

    file = s.get(getVideoUrl(defPage), headers=h.videoHeaders, cookies=videoCookies)
    
    return file