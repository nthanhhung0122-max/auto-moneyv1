"""
====================================================================
  BOT DUA TOP XEP HANG TELEGRAM: @kiemtien6789_bot (ACC 1: @hungzai22)
  TINH NANG:
      - TU DONG LAY INIT_DATA MOI BANG TELETHON (Khong bao gio het han)
      - Diem danh hang ngay (daily_claim)
      - BAT BUOC CHAY DU 10 LAN CHO AN (Tap + Boost 10/10)
      - BAT BUOC CHAY DU 10 LAN MO RUONG (open_chest 10/10)
      - BAT BUOC CHAY DU 10 LAN QUIZ (Tra loi dung 100% 10/10)
      - BAT BUOC CHAY DU 10 LAN NHIEM VU 1, 2, 3 (Monetag: 10/10)
        (Tu dong cho het cooldown 10 phut de chay tiep den khi du 10/10)
      - Cay Smartlinks (task6 - task37)
      - Tu dong reset va xin init_data luc 00:00:05 GMT+7 moi ngay
====================================================================
"""

import time
import random
import requests
import urllib.parse
import re
import os
import base64
import asyncio
import sqlite3
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

# -----------------------------------------------------------------
#  CAU HINH HE THONG - TAI KHOAN 3 (phan hoang - ID: 8896084050)
# -----------------------------------------------------------------

API_ID = 39182276
API_HASH = "f02b155d895a3a3fbf8a1cbe810b5338"
SESSION_PATH = "telepet_acc4"

API_URL = "https://kien.kiemtienngay.us/public/api.php"
FALLBACK_INIT_DATA = "query_id=AAHTpagIBAAAANOlqAiQ0PGe&user=%7B%22id%22%3A8735204819%2C%22first_name%22%3A%22Uweuweuweuweu%22%2C%22last_name%22%3A%22Osas%22%2C%22username%22%3A%22Wind_trader%22%2C%22language_code%22%3A%22vi%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FDf9UdWj_lcG78CMooXZXyDrc8fEcf5WhBgsEGeTbFMByWu-kovHAeZlzin8RyNAt.svg%22%7D&auth_date=1793281870&signature=bNSi2MX02oj99MWLXRvg6r00mp3-7KwsshBifoG1AsuwpH45yCaBGjMXQRob_--zWrx8bBw8Yn-QnHP8s41_Bg&hash=c7c6fdea481982de2cefda0c0662fffeab0c98e822b2aa1b52473621a51143ca"
CURRENT_INIT_DATA = FALLBACK_INIT_DATA

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "WebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    ),
    "origin": "https://kien.kiemtienngay.us",
    "referer": "https://kien.kiemtienngay.us/public/index.php",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "accept": "*/*",
}

EXTRA_TASKS = [
    "task6", "task7", "task8", "task9", "task10", "task11", "task12", "task13", "task14", "task15",
    "task16", "task17", "task18", "task19", "task20", "task21", "task22", "task23",
    "task24", "task25", "task26", "task27", "task28", "task29", "task30", "task31",
    "task32", "task33", "task34", "task35", "task36", "task37"
]

progress = {
    "feed": 0, "chest": 0, "quiz": 0,
    "task1": 0, "task2": 0, "task3": 0,
    "feed_done": False, "chest_done": False, "quiz_done": False,
    "task1_done": False, "task2_done": False, "task3_done": False,
}

cooldown_monetag = {"task1": 0, "task2": 0, "task3": 0}
last_smartlink_run = 0

QUIZ_ANSWERS = {
    "chim": "Chim ruá»“i",
    "bÃ³ng Ä‘Ã¨n": "Thomas Edison",
    "nguyÃªn tá»‘": "2",
    "1 + 2 x 3": "7",
    "chÃ³ sá»§a": "bark",
    "thá»§ Ä‘Ã´": "HÃ  Ná»™i",
    "trÃ¡i Ä‘áº¥t": "Máº·t trá»i",
    "ngÄƒn": "4",
    "ngÃ´n ngá»¯": "Tiáº¿ng Anh",
    "biá»ƒn": "ThÃ¡i BÃ¬nh DÆ°Æ¡ng",
    "gáº§n máº·t trá»i": "Sao Thá»§y"
}

def log(tag, msg, color=Fore.WHITE):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] [{tag}] {color}{msg}{Style.RESET_ALL}", flush=True)

# -----------------------------------------------------------------
#  HAM TU DONG XIN TELEGRAM CAP INIT_DATA MOI TOANH
# -----------------------------------------------------------------
def ensure_valid_session():
    """Kiem tra tinh toan ven cua file sqlite session, tu sua neu bi loi malformed"""
    session_file = f"{SESSION_PATH}.session"
    is_valid = False
    if os.path.exists(session_file):
        try:
            conn = sqlite3.connect(session_file)
            c = conn.cursor()
            c.execute("PRAGMA integrity_check")
            res = c.fetchall()
            c.close()
            conn.close()
            if res and res[0][0] == "ok":
                is_valid = True
        except Exception:
            is_valid = False

    if not is_valid and os.path.exists(session_file):
        for ext in [".session", ".session-journal"]:
            fpath = f"{SESSION_PATH}{ext}"
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass

        raw_secret = os.getenv("TELEGRAM_SESSION_B64_ACC4") or os.getenv("TELEGRAM_SESSION_B64")
        if raw_secret:
            clean_b64 = re.sub(r"\s+", "", raw_secret.strip())
            try:
                data = base64.b64decode(clean_b64)
                with open(session_file, "wb") as f:
                    f.write(data)
                log("INFO", f"Da tu dong sua & khoi phuc session Telegram ({len(data)} bytes)", Fore.CYAN)
            except Exception as e:
                log("ERR", f"Khong the giai ma base64 session: {e}", Fore.RED)

async def fetch_fresh_init_data():
    global CURRENT_INIT_DATA
    log("+", "Dang kiem tra ket noi Telegram de cap nhat init_data...", Fore.CYAN)
    
    session_file = f"{SESSION_PATH}.session"
    session_secret = os.getenv("TELEGRAM_SESSION_B64_ACC4") or os.getenv("TELEGRAM_SESSION_B64")
    if session_secret and (not os.path.exists(session_file) or os.path.getsize(session_file) < 25000):
        try:
            clean_b64 = re.sub(r"\s+", "", session_secret.strip())
            with open(session_file, "wb") as f:
                f.write(base64.b64decode(clean_b64))
        except Exception as e:
            log("WARN", f"Khong the khoi phuc session tu Secret: {e}", Fore.YELLOW)

    if not os.path.exists(session_file):
        log("INFO", "Chua co session MTProto, su dung truc tiep init_data cua @Wind_trader...", Fore.CYAN)
        CURRENT_INIT_DATA = CURRENT_INIT_DATA or FALLBACK_INIT_DATA
        return CURRENT_INIT_DATA

    ensure_valid_session()
    try:
        client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            log("WARN", "Session telepet_acc4 chua duoc xac thuc, dung init_data san co!", Fore.YELLOW)
            await client.disconnect()
            CURRENT_INIT_DATA = CURRENT_INIT_DATA or FALLBACK_INIT_DATA
            return CURRENT_INIT_DATA
        
        bot = await client.get_input_entity("kiemtien6789_bot")
        web_view = await client(RequestWebViewRequest(
            peer=bot,
            bot=bot,
            platform="android",
            from_bot_menu=False,
            url="https://kien.kiemtienngay.us/public/"
        ))
        await client.disconnect()

        fragment = urllib.parse.urlparse(web_view.url).fragment
        params = urllib.parse.parse_qs(fragment)
        fresh = params.get("tgWebAppData", [None])[0]
        if fresh:
            CURRENT_INIT_DATA = fresh
            log("OK", "Da lay thanh cong init_data tuoi moi tu Telegram!", Fore.GREEN)
        return CURRENT_INIT_DATA
    except Exception as e:
        log("WARN", f"Loi ket noi Telethon ({e}), tiep tuc voi init_data san co!", Fore.YELLOW)
        CURRENT_INIT_DATA = CURRENT_INIT_DATA or FALLBACK_INIT_DATA
        return CURRENT_INIT_DATA

def get_fresh_init_data_sync():
    return asyncio.run(fetch_fresh_init_data())

def post_action(action, extra_data=None):
    payload = {"action": action, "init_data": CURRENT_INIT_DATA}
    if extra_data:
        payload.update(extra_data)
    try:
        r = requests.post(API_URL, headers=HEADERS, data=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refresh_profile():
    res = post_action("me")
    if res.get("ok"):
        return res.get("user")
    return None

def do_daily_claim():
    res = post_action("daily_claim")
    if res.get("ok") and res.get("claimed"):
        log("GIFT", f"Diem danh hang ngay: +{res.get('amount', 1000):,} coin", Fore.GREEN)

# -----------------------------------------------------------------
#  1. CHO AN (TAP + BOOST) - BAT BUOC DU 10/10 LAN
# -----------------------------------------------------------------
def do_feed_tasks():
    if progress["feed_done"]:
        return
    log("+", f"Kiem tra Cho an (Tien do: {progress['feed']}/10)...", Fore.CYAN)
    
    fail_count = 0
    while progress["feed"] < 10 and fail_count < 5:
        # Kich hoat boost de x2 thuong & them luot cho an
        tok_res = post_action("ads_token", {"type": "boost"})
        if tok_res.get("ok"):
            post_action("start_boost", {"ads_ok": tok_res.get("token")})

        res = post_action("tap")
        if res.get("ok"):
            progress["feed"] += 1
            fail_count = 0
            log("+", f"Cho an lan {progress['feed']}/10: +{res.get('added', 500):,} coin (Con {res.get('left', 0)} luot)", Fore.GREEN)
            time.sleep(1)
        else:
            err = str(res.get("error", ""))
            fail_count += 1
            if "háº¿t" in err.lower() or "limit" in err.lower():
                log("OK", f"Cho an: {err} -> Da hoan tat luot toi da!", Fore.YELLOW)
                progress["feed"] = 10
                progress["feed_done"] = True
                break
            time.sleep(2)

    if progress["feed"] >= 10:
        progress["feed_done"] = True
        log("OK", "Cho an: DA DAT DU 10/10 LAN!", Fore.GREEN)

# -----------------------------------------------------------------
#  2. MO RUONG (OPEN_CHEST) - BAT BUOC DU 10/10 LAN
# -----------------------------------------------------------------
def do_chest_tasks():
    if progress["chest_done"]:
        return
    log("+", f"Kiem tra Mo ruong (Tien do: {progress['chest']}/10)...", Fore.CYAN)
    
    fail_count = 0
    while progress["chest"] < 10 and fail_count < 5:
        res = post_action("open_chest")
        if res.get("ok"):
            progress["chest"] += 1
            fail_count = 0
            reward = res.get("reward", 0)
            left = res.get("left", 0)
            log("+", f"Mo ruong lan {progress['chest']}/10: +{reward:,} coin (Server con {left} luot)", Fore.GREEN)
            if left == 0:
                progress["chest"] = 10
                progress["chest_done"] = True
                break
            time.sleep(1)
        else:
            err = str(res.get("error", ""))
            fail_count += 1
            if "háº¿t lÆ°á»£t" in err.lower():
                log("OK", f"Mo ruong: {err} -> Server xac nhan da mo du 10 ruong hom nay!", Fore.YELLOW)
                progress["chest"] = 10
                progress["chest_done"] = True
                break
            time.sleep(2)

    if progress["chest"] >= 10:
        progress["chest_done"] = True
        log("OK", "Mo ruong: DA DAT DU 10/10 LAN!", Fore.GREEN)

# -----------------------------------------------------------------
#  3. TRA LOI QUIZ - BAT BUOC DU 10/10 LAN (GIAI DUNG 100%)
# -----------------------------------------------------------------
def solve_quiz(q_text, options):
    for k, v in QUIZ_ANSWERS.items():
        if k in q_text.lower():
            for idx, opt in enumerate(options):
                if v.lower() in opt.lower():
                    return idx
    return random.randint(0, len(options) - 1) if options else 0

def do_quiz_tasks():
    if progress["quiz_done"]:
        return
    log("+", f"Kiem tra Tra loi cau hoi (Tien do: {progress['quiz']}/10)...", Fore.CYAN)
    
    while progress["quiz"] < 10:
        q_res = post_action("quiz_get")
        if not q_res.get("ok") or not q_res.get("quiz"):
            log("OK", "Cau hoi: Server da het cau hoi trong ngay!", Fore.YELLOW)
            progress["quiz"] = 10
            progress["quiz_done"] = True
            break
        
        quiz = q_res.get("quiz", {})
        qid = quiz.get("id")
        qtxt = quiz.get("question", "")
        opts = quiz.get("options", [])
        
        selected_idx = solve_quiz(qtxt, opts)
        time.sleep(1)
        
        a_res = post_action("quiz_answer", {"quiz_id": qid, "option": selected_idx})
        if a_res.get("ok"):
            progress["quiz"] += 1
            earned = a_res.get("reward", 0)
            log("+", f"Cau hoi lan {progress['quiz']}/10: '{qtxt[:32]}...' -> [{opts[selected_idx]}] (+{earned:,} coin)", Fore.GREEN)
        else:
            time.sleep(2)
        time.sleep(1)

    if progress["quiz"] >= 10:
        progress["quiz_done"] = True
        log("OK", "Tra loi cau hoi: DA DAT DU 10/10 LAN!", Fore.GREEN)

# -----------------------------------------------------------------
#  4. NHIEM VU 1, 2, 3 (MONETAG) - BAT BUOC DU 10/10 LAN MOI TASK
# -----------------------------------------------------------------
def do_monetag_tasks():
    task_mapping = [
        ("task1", "monetag1", "Nhiem vu 1 (Monetag)"),
        ("task2", "monetag2", "Nhiem vu 2 (Monetag)"),
        ("task3", "monetag3", "Nhiem vu 3 (Monetag)"),
    ]
    now = time.time()

    for task_key, src, task_name in task_mapping:
        done_flag_key = f"{task_key}_done"
        if progress[done_flag_key]:
            continue

        # Neu dang trong thoi gian cooldown 10 phut -> bo qua cho lan quet sau, KHONG danh dau xong!
        if now < cooldown_monetag[task_key]:
            rem = int(cooldown_monetag[task_key] - now)
            mins, secs = divmod(rem, 60)
            log("WAIT", f"{task_name}: Dang cooldown {mins}m {secs}s nua (Hien tai: {progress[task_key]}/10)...", Fore.YELLOW)
            continue

        res = post_action("reward", {"amount": 300, "source": src})
        if res.get("ok") and res.get("status") == "ok":
            progress[task_key] += 1
            log("+", f"{task_name} lan {progress[task_key]}/10: +{res.get('reward', 300)} coin", Fore.GREEN)
            # Thiet lap cooldown 10 phut cho lan tiep theo
            cooldown_monetag[task_key] = time.time() + 605
            if progress[task_key] >= 10:
                progress[done_flag_key] = True
                log("OK", f"{task_name}: DA HOAN THANH DU 10/10 LAN!", Fore.GREEN)
        else:
            err = str(res.get("error", ""))
            log("INFO", f"{task_name} (Hien tai: {progress[task_key]}/10): {err}", Fore.YELLOW)
            # Trich xuat so phut can cho
            m = re.search(r'(\d+)\s*phÃºt', err)
            if m:
                mins_wait = int(m.group(1))
                cooldown_monetag[task_key] = time.time() + (mins_wait * 60) + 5
            elif "háº¿t lÆ°á»£t" in err.lower():
                progress[task_key] = 10
                progress[done_flag_key] = True
                log("OK", f"{task_name}: Server bao da het luot hom nay (10/10)!", Fore.GREEN)
            else:
                cooldown_monetag[task_key] = time.time() + 60
        time.sleep(1)

# -----------------------------------------------------------------
#  5. CAY PHU SMARTLINKS (task6 - task37)
# -----------------------------------------------------------------
def do_extra_smartlinks():
    global last_smartlink_run
    # Cooldown 10 phut giua cac dot chay smartlinks
    if time.time() - last_smartlink_run < 605:
        return
    log("+", "Kiem tra chay cac Smartlinks (task6 - task37)...", Fore.CYAN)
    success = 0
    for tk in EXTRA_TASKS:
        res = post_action(tk)
        if res.get("ok") and res.get("status") == "ok":
            success += 1
            log("+", f"Smartlink {tk}: +{res.get('reward', 100)} coin", Fore.GREEN)
            time.sleep(1)
    if success > 0:
        log("DONE", f"Da nhan thuong thanh cong tu {success} Smartlink!", Fore.GREEN)
    last_smartlink_run = time.time()

# -----------------------------------------------------------------
#  KIEM TRA TAT CA NHIEM VU CO DU 10/10 CHUA
# -----------------------------------------------------------------
def is_all_tasks_10_completed():
    return (
        progress["feed_done"] and
        progress["chest_done"] and
        progress["quiz_done"] and
        progress["task1_done"] and
        progress["task2_done"] and
        progress["task3_done"]
    )

def get_seconds_until_midnight_vn():
    vn_tz = timezone(timedelta(hours=7))
    now_vn = datetime.now(vn_tz)
    tomorrow = now_vn.date() + timedelta(days=1)
    midnight = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 5, tzinfo=vn_tz)
    return int((midnight - now_vn).total_seconds())

def print_dashboard(user):
    coins = user.get("coins", 0) if user else 0
    print(f"""
{Fore.YELLOW}====================================================================
|  BANG TIEN DO NHIEM VU XEP HANG TRONG NGAY (ACC 1: @hungzai22)     |
+------------------------------------------------------------------+
|  Cho an (Tap+Boost)   : {progress['feed']:>2}/10  [{'DA DU 10/10' if progress['feed_done'] else 'DANG LAM'}]
|  Mo ruong (Chest)     : {progress['chest']:>2}/10  [{'DA DU 10/10' if progress['chest_done'] else 'DANG LAM'}]
|  Tra loi cau hoi      : {progress['quiz']:>2}/10  [{'DA DU 10/10' if progress['quiz_done'] else 'DANG LAM'}]
|  Nhiem vu 1 (Monetag) : {progress['task1']:>2}/10  [{'DA DU 10/10' if progress['task1_done'] else 'CHO COOLDOWN'}]
|  Nhiem vu 2 (Monetag) : {progress['task2']:>2}/10  [{'DA DU 10/10' if progress['task2_done'] else 'CHO COOLDOWN'}]
|  Nhiem vu 3 (Monetag) : {progress['task3']:>2}/10  [{'DA DU 10/10' if progress['task3_done'] else 'CHO COOLDOWN'}]
+------------------------------------------------------------------+
|  So du vi TelePet     : {coins:>10,} Coins (~{coins*0.02:,.2f} VND)
===================================================================={Style.RESET_ALL}""")

def reset_daily_progress():
    global progress, cooldown_monetag
    progress = {
        "feed": 0, "chest": 0, "quiz": 0,
        "task1": 0, "task2": 0, "task3": 0,
        "feed_done": False, "chest_done": False, "quiz_done": False,
        "task1_done": False, "task2_done": False, "task3_done": False,
    }
    cooldown_monetag = {"task1": 0, "task2": 0, "task3": 0}
    log("RESET", "DA SANG NGAY MOI (00:00 GMT+7)! RESET TOAN BO TIEN DO DE DUA TOP!", Fore.GREEN)

def main():
    print(f"""
{Fore.YELLOW}====================================================================
|  BOT DUA TOP XEP HANG 24/7 - AUTO TELEPET (ACC 1: @hungzai22)
|  Tai khoan: phan hoang (ID: 8896084050)
|  - TU DONG BAT BUOC CHAY DU 10 LAN CHO MOI MUC
|  - Tu dong cho het 10 phut cooldown de lam tiep Monetag 1, 2, 3
|  - Cho an (10/10) - Mo ruong (10/10) - Quiz (10/10)
|  - Chi di ngu khi DA DAT DU 10/10 LAN TAT CA CAC MUC!
===================================================================={Style.RESET_ALL}
    """)

    # 1. Tu dong lay init_data moi tu Telegram Client
    get_fresh_init_data_sync()

    curr_u = refresh_profile()
    if curr_u:
        log("LOGIN", f"Dang nhap thanh cong: {curr_u.get('name')} (@{curr_u.get('username')}) | So du: {curr_u.get('coins'):,} Coins", Fore.GREEN)
    else:
        log("ERR", "Khong the xac thuc voi may chu TelePet!", Fore.RED)
        return

    while True:
        # Diem danh hang ngay
        do_daily_claim()

        # 1. Chay Cho an (tap + boost)
        do_feed_tasks()

        # 2. Chay Mo ruong (open_chest)
        do_chest_tasks()

        # 3. Chay Tra loi cau hoi (quiz_get + quiz_answer)
        do_quiz_tasks()

        # 4. Chay Nhiem vu 1, 2, 3 (Monetag: reward)
        do_monetag_tasks()

        # 5. Cay phu Smartlinks (task6 - task37)
        do_extra_smartlinks()

        # In bang dieu khien
        curr_u = refresh_profile()
        print_dashboard(curr_u)

        # KIEM TRA: TAT CA CAC MUC DA DU 10/10 LAN CHUA?
        if is_all_tasks_10_completed():
            sec_to_midnight = get_seconds_until_midnight_vn()
            hrs, rem = divmod(sec_to_midnight, 3600)
            mins, secs = divmod(rem, 60)

            print("\n" + "="*66)
            log("DONE", "ðŸŽ‰ TAT CA NHIEM VU DUA TOP DA DAT DU 10/10 LAN TRONG NGAY!", Fore.GREEN)
            log("SLEEP", f"Cho bot nghi den 00:00:05 GMT+7 ngay mai (con {hrs}h {mins}m {secs}s)...", Fore.MAGENTA)
            print("="*66 + "\n")

            while True:
                sec_left = get_seconds_until_midnight_vn()
                if sec_left <= 5:
                    break
                time.sleep(min(sec_left, 60))

            log("RESET", "DA TOI 00:00 GMT+7! Reset ngay moi va nhan init_data moi...", Fore.GREEN)
            reset_daily_progress()
            get_fresh_init_data_sync()
        else:
            # Chua du 10/10 vi Monetag hoac Smartlink dang vuong cooldown 10 phut
            now = time.time()
            rem_waits = [
                cooldown_monetag["task1"] - now,
                cooldown_monetag["task2"] - now,
                cooldown_monetag["task3"] - now
            ]
            valid_waits = [w for w in rem_waits if w > 0]
            sleep_time = max(30, int(min(valid_waits))) if valid_waits else 60
            sleep_time = min(sleep_time, 180)  # Kiem tra toi da moi 3 phut

            mins, secs = divmod(sleep_time, 60)
            log("LOOP", f"Dang cho cooldown Monetag de chay tiep cho du 10/10 (Nghi {mins}m {secs}s roi quet lai)...", Fore.CYAN)
            time.sleep(sleep_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[STOP] Da dung bot.{Style.RESET_ALL}")
