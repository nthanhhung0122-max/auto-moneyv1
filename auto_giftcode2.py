#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
  BOT QUET VA NAP GIFTCODE TELEPET 24/7 (BO LOC VIP: CHI NHAT CODE >= 9,000 XU)
  Tai khoan: ACC 2 (@gaylobucu - ID: 8431197387)
====================================================================
"""

import time
import requests
import urllib.parse
import re
import os
import random
import string
import asyncio
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

API_ID = 39182276
API_HASH = "f02b155d895a3a3fbf8a1cbe810b5338"

DEFAULT_STRING_SESSION = "1BVtsOHIBuzoeRtBOmpNGh2sdyxpZ5e0nY4MrFe-6KKbmJPaM0YnCJiKRI0L9mEh1C5rwqLQqucj456LRF7vV1YIPjZNqL6JevLM0Ww3FTml1NoKdwsiPINfsy9MbBlBhKOvha7py44L4pK5aEXjwpjpoNj4LaSmtWaPiQPufJuTwPB86f4gYjSeXM3HtxhnFU7MtHR5vbZPBa9N2HQSlt2BMB47q00DbQVtvYA37R3R-TrtV2MtwixL9ozChADFq38NYcw4eRyRwKrkobVLccvz0_hvqgHXiQbrfcFLLRkRGwGlRCB-Ew4YhLLdnCbG1hjGEfxUrp9MRmF0JvS-u20MfAuvlcgQ="
FALLBACK_INIT_DATA = ""

CURRENT_INIT_DATA = ""
MIN_REWARD_VALUE = 9000
TARGET_CODES_COUNT = 200
HIGH_VALUE_TASKS = [1, 16, 24, 25, 27, 31]

PROCESSED_CODES = set()
COINS_EARNED_TODAY = 0
CODES_SUCCESS_TODAY = 0
IS_DAILY_LIMIT = False

API_URL = "https://kien.kiemtienngay.us/public/api.php"

HEADERS_TELEPET = {
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://kien.kiemtienngay.us",
    "referer": "https://kien.kiemtienngay.us/public/nhiemvu.php",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "accept": "*/*",
}

DEFAULT_WEB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://kiemtienngay.us/'
}

def log(tag, msg, color=Fore.WHITE):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] [{tag}] {color}{msg}{Style.RESET_ALL}", flush=True)

async def fetch_fresh_init_data():
    global CURRENT_INIT_DATA
    log("+", "Dang ket noi Telegram de lay init_data ACC 2 (@gaylobucu)...", Fore.CYAN)
    session_str = os.getenv("TELEGRAM_STRING_SESSION") or DEFAULT_STRING_SESSION
    if session_str:
        try:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            await client.connect()
            if await client.is_user_authorized():
                bot = await client.get_input_entity("kiemtien6789_bot")
                web_view = await client(RequestWebViewRequest(
                    peer=bot,
                    bot=bot,
                    platform="android",
                    from_bot_menu=False,
                    url="https://kien.kiemtienngay.us/public/"
                ))
                fragment = urllib.parse.urlparse(web_view.url).fragment
                params = urllib.parse.parse_qs(fragment)
                CURRENT_INIT_DATA = params.get("tgWebAppData", [None])[0]
                await client.disconnect()
                log("OK", "Da cap nhat init_data thanh cong tu Telegram!", Fore.GREEN)
                return CURRENT_INIT_DATA
            await client.disconnect()
        except Exception as e:
            log("WARN", f"Loi lay init_data qua StringSession: {e}", Fore.YELLOW)

    if FALLBACK_INIT_DATA:
        CURRENT_INIT_DATA = FALLBACK_INIT_DATA
        return CURRENT_INIT_DATA
    return None

def get_fresh_init_data_sync():
    return asyncio.run(fetch_fresh_init_data())

def refresh_profile():
    try:
        r = requests.post(API_URL, headers=HEADERS_TELEPET, data={"action": "me", "init_data": CURRENT_INIT_DATA}, timeout=8)
        res = r.json()
        if res.get("ok"):
            return res.get("user")
    except:
        pass
    return None

def create_fresh_web_session():
    s = requests.Session()
    s.headers.update(DEFAULT_WEB_HEADERS)
    uname = "farm_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    pwd = "Pass123456@"
    try:
        r = s.post("https://kiemtienngay.us/register.php", data={
            "username": uname,
            "password": pwd,
            "confirm_password": pwd,
            "referrer": ""
        }, timeout=8)
        if r.status_code == 200:
            return s, uname
    except:
        pass
    return None, None

def extract_giftcode_target_url(loc, session):
    if not loc:
        return None
    if "giftcode.php?key=" in loc:
        return loc
    try:
        parsed = urllib.parse.urlparse(loc)
        target = urllib.parse.parse_qs(parsed.query).get("url", [None])[0]
        if target and "giftcode.php?key=" in target:
            return target
    except:
        pass

    try:
        r = session.get(loc, headers=DEFAULT_WEB_HEADERS, timeout=8, allow_redirects=True)
        m_orig = re.search(r"var\s+originalUrl\s*=\s*['\"]([^'\"]+)['\"]", r.text)
        if m_orig:
            return m_orig.group(1)
        m_url = re.search(r"https?://(?:kien\.)?kiemtienngay\.us/giftcode\.php\?key=[a-zA-Z0-9]+", r.text)
        if m_url:
            return m_url.group(0)
    except:
        pass
    return None

def fetch_code_from_task(session, tid):
    url = f"https://kiemtienngay.us/nbk222/giftcode.php?task_id={tid}"
    try:
        r = session.get(url, allow_redirects=False, timeout=8)
        if r.status_code == 200 and "BẠN ĐÃ LẤY GIFTCODE NÀY RỒI" in r.text:
            return None, 0

        loc = r.headers.get("Location", "")
        if not loc:
            return None, 0
        target_url = extract_giftcode_target_url(loc, session)
        if not target_url:
            return None, 0

        headers_gift = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': target_url
        }
        r_claim = session.post(target_url, data="confirm_gift=1", headers=headers_gift, timeout=8)
        data = r_claim.json()
        if data.get("status") == "ok":
            code = data.get("code")
            rew_str = str(data.get("reward", "0")).replace(",", "").replace(".", "").strip()
            reward_val = int(rew_str) if rew_str.isdigit() else 0
            return code, reward_val
    except:
        pass
    return None, 0

def redeem_code(code, reward_val):
    global COINS_EARNED_TODAY, CODES_SUCCESS_TODAY, IS_DAILY_LIMIT
    if not code or code in PROCESSED_CODES:
        return

    if reward_val < MIN_REWARD_VALUE:
        log("SKIP", f"Bo qua ma [{code}] vi chi co {reward_val:,} xu (< {MIN_REWARD_VALUE:,} xu)", Fore.YELLOW)
        return

    PROCESSED_CODES.add(code)
    curr_idx = len(PROCESSED_CODES)

    if IS_DAILY_LIMIT:
        log("LIMIT", f"[{curr_idx}/{TARGET_CODES_COUNT}] Ma 9K [{code}] (Acc da cham nguong ngay, tiep tuc chay cho du 200 ma)", Fore.YELLOW)
        time.sleep(0.5)
        return

    try:
        redeem_data = {
            "action": "giftcode",
            "code": code,
            "init_data": CURRENT_INIT_DATA
        }
        r = requests.post(API_URL, headers=HEADERS_TELEPET, data=redeem_data, timeout=8)
        res = r.json()
        if res.get("ok"):
            amt = res.get("amount", reward_val or 9000)
            COINS_EARNED_TODAY += amt
            CODES_SUCCESS_TODAY += 1
            log("VIP", f"[{curr_idx}/{TARGET_CODES_COUNT}] Ma 9K [{code}] -> +{amt:,} Xu! (Tong: {COINS_EARNED_TODAY:,} Xu)", Fore.GREEN)
        else:
            err = str(res.get("error", ""))
            if "chào cậu" in err.lower() or "hi chào" in err.lower() or "tối đa" in err.lower():
                log("LIMIT", f"[{curr_idx}/{TARGET_CODES_COUNT}] Acc cham gioi han ngay: '{err}'! (Tiep tuc quet du 200 ma...)", Fore.YELLOW)
                IS_DAILY_LIMIT = True
            else:
                log("INFO", f"[{curr_idx}/{TARGET_CODES_COUNT}] Ma [{code}] ({reward_val:,} xu) -> {err}", Fore.WHITE)
    except Exception as e:
        log("ERR", f"[{curr_idx}/{TARGET_CODES_COUNT}] Loi nap code [{code}]: {e}", Fore.RED)
    time.sleep(1)

def scan_web_tasks_until_target():
    log("START", f"Bat dau quet CHUYEN MA VIP >= {MIN_REWARD_VALUE:,} XU cho den khi DU {TARGET_CODES_COUNT} MA...", Fore.MAGENTA)

    s_main = requests.Session()
    s_main.headers.update(DEFAULT_WEB_HEADERS)
    uname_main = "hung_acc2_2026"
    s_main.post("https://kiemtienngay.us/register.php", data={"username": uname_main, "password": "Pass123456@", "confirm_password": "Pass123456@", "referrer": ""}, timeout=8)
    s_main.post("https://kiemtienngay.us/login.php", data={"username": uname_main, "password": "Pass123456@"}, timeout=8)

    for round_num in range(1, 3):
        for tid in HIGH_VALUE_TASKS:
            if len(PROCESSED_CODES) >= TARGET_CODES_COUNT:
                break
            code, rew = fetch_code_from_task(s_main, tid)
            if code:
                redeem_code(code, rew)

    farm_cycle = 1
    while len(PROCESSED_CODES) < TARGET_CODES_COUNT:
        farm_cycle += 1
        s_fresh, fresh_user = create_fresh_web_session()
        if not s_fresh:
            time.sleep(3)
            continue

        log("FARM", f"Tao tai khoan ao #{farm_cycle} ({fresh_user}). Dang quet ma 9,000 xu...", Fore.MAGENTA)
        for round_num in range(1, 3):
            for tid in HIGH_VALUE_TASKS:
                if len(PROCESSED_CODES) >= TARGET_CODES_COUNT:
                    break
                code, rew = fetch_code_from_task(s_fresh, tid)
                if code:
                    redeem_code(code, rew)
        time.sleep(1)

    log("DONE", f"DA HOAN THANH DU {len(PROCESSED_CODES)}/{TARGET_CODES_COUNT} MA GIFTCODE 9,000 XU!", Fore.GREEN)

def get_seconds_until_midnight_vn():
    vn_tz = timezone(timedelta(hours=7))
    now_vn = datetime.now(vn_tz)
    tomorrow = now_vn.date() + timedelta(days=1)
    midnight = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 5, tzinfo=vn_tz)
    return int((midnight - now_vn).total_seconds())

def sleep_until_midnight():
    sec_left = get_seconds_until_midnight_vn()
    hrs, remainder = divmod(sec_left, 3600)
    mins, secs = divmod(remainder, 60)
    log("SLEEP", f"Da chay DU 200 ma 9,000 xu! Se nghi {hrs}h {mins}p cho den 00:00:05 GMT+7 de reset ngay moi...", Fore.MAGENTA)
    while sec_left > 5:
        chunk = min(sec_left, 300)
        time.sleep(chunk)
        sec_left = get_seconds_until_midnight_vn()
        h, r = divmod(sec_left, 3600)
        m, s = divmod(r, 60)
        log("SLEEP", f"Dang nghi ngoi cho 00:00 GMT+7 (con lai {h}h {m}p)...", Fore.MAGENTA)

def main():
    print(f"""
{Fore.CYAN}====================================================================
|  BOT QUET VA NAP GIFTCODE 24/7 (ACC 2 (@gaylobucu))
|  BO LOC DAC BIET: CHI NHAT MA >= {MIN_REWARD_VALUE:,} XU (BO QUA MA 5K)
|  MUC TIEU: QUET DU {TARGET_CODES_COUNT} MA CODE DU CO BI GIOI HAN HAY KHONG
===================================================================={Style.RESET_ALL}
    """)
    get_fresh_init_data_sync()
    u = refresh_profile()
    if u:
        log("LOGIN", f"Ket noi: {u.get('name')} (@{u.get('username') or ''}) | Xu: {u.get('coins'):,}", Fore.GREEN)

    while True:
        global PROCESSED_CODES, COINS_EARNED_TODAY, CODES_SUCCESS_TODAY, IS_DAILY_LIMIT
        PROCESSED_CODES.clear()
        COINS_EARNED_TODAY = 0
        CODES_SUCCESS_TODAY = 0
        IS_DAILY_LIMIT = False

        scan_web_tasks_until_target()

        print("\n" + "="*60)
        print(f"{Fore.GREEN}TONG KET PHIEN 200 GIFTCODE 9,000 XU - ACC 2 (@gaylobucu){Style.RESET_ALL}")
        print(f"- Tong ma da quet: {len(PROCESSED_CODES)} / {TARGET_CODES_COUNT}")
        print(f"- Nap thanh cong: {CODES_SUCCESS_TODAY} ma | Xu kiem duoc: +{COINS_EARNED_TODAY:,} Xu")
        print("="*60 + "\n")

        sleep_until_midnight()
        get_fresh_init_data_sync()

if __name__ == "__main__":
    main()
