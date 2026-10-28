"""
====================================================================
  🏆 BOT ĐUA TOP XẾP HẠNG TELEGRAM: @kiemtien6789_bot (TÀI KHOẢN 2)
  🎯 Mục tiêu: Hoàn thành sớm nhất 10/10 tất cả nhiệm vụ mỗi ngày:
      1. Cho ăn (10 lần boost + đào)
      2. Mở rương (10 lần rương)
      3. Câu hỏi (10/10 câu trắc nghiệm tự động trả lời đúng 100%)
      4. Nhiệm vụ 1, 2, 3 (Monetag Ads 10 lần/ngày)
  🌙 Khi đủ 10/10: Tự động ngủ đến 00:00 GMT+7 và thức dậy cày tiếp!
====================================================================
"""

import time
import random
import requests
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────────────────────────
#  CẤU HÌNH HỆ THỐNG - TÀI KHOẢN 2 (@gaylobucu)
# ─────────────────────────────────────────────────────────────────

API_URL = "https://kien.kiemtienngay.us/public/api.php"

INIT_DATA = (
    "query_id=AAHL3Il2AwAAAMvciXYWkX5S"
    "&user=%7B%22id%22%3A8431197387%2C%22first_name%22%3A%22fug%C3%B9%E1%BB%B5tdtcvhcytx%22%2C"
    "%22last_name%22%3A%22%40EcoForestTonBot%F0%9F%8C%BF%22%2C%22username%22%3A%22gaylobucu%22%2C"
    "%22language_code%22%3A%22vi%22%2C%22allows_write_to_pm%22%3Atrue%2C"
    "%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F"
    "yR_oYve0R8PTyYwqBzk1vokJzdmAYmXVlSyykmw-Oy_a7N5wt-aO1yxuzIlOFqGh.svg%22%7D"
    "&auth_date=1793112986"
    "&signature=y6g53vvOVhrxLVfdqotSUKt2D9mz6R9hC5pUQYB_Eipu8xyvdSK1l82KsUMAV86Pgcz7TZWYvcWGRRUDUKYcBA"
    "&hash=75030b0a7c68655091ae53479a90b2f90ae30cc23169fe2d485965a64b8f46cf"
)

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    ),
    "origin": "https://kien.kiemtienngay.us",
    "referer": "https://kien.kiemtienngay.us/public/index.php",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "accept": "*/*",
}

# Bộ đếm tiến độ nhiệm vụ xếp hạng (Tối đa 10 lần mỗi loại)
progress = {
    "feed": 0,      # Cho ăn (max 10)
    "chest": 0,     # Mở rương (max 10)
    "quiz": 0,      # Trả lời câu hỏi (max 10)
    "task1": 0,     # Nhiệm vụ 1 Monetag (max 10)
    "task2": 0,     # Nhiệm vụ 2 Monetag (max 10)
    "task3": 0,     # Nhiệm vụ 3 Monetag (max 10)
    "feed_done": False,
    "chest_done": False,
    "quiz_done": False,
    "task1_done": False,
    "task2_done": False,
    "task3_done": False,
}

def log(tag, msg, color=Fore.WHITE):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{ts}]{Style.RESET_ALL} {tag} {color}{msg}{Style.RESET_ALL}")

def api(action, **kwargs):
    payload = {"action": action, "init_data": INIT_DATA}
    payload.update(kwargs)
    try:
        r = requests.post(API_URL, headers=HEADERS, data=payload, timeout=12)
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def refresh_profile():
    r = api("me")
    if r.get("ok"):
        return r["user"]
    return None

def get_seconds_until_midnight_vn():
    """Tính số giây từ hiện tại đến 00:00:05 GMT+7 ngày hôm sau"""
    vn_tz = timezone(timedelta(hours=7))
    now_vn = datetime.now(vn_tz)
    tomorrow_midnight = (now_vn + timedelta(days=1)).replace(
        hour=0, minute=0, second=5, microsecond=0
    )
    return int((tomorrow_midnight - now_vn).total_seconds())

# ─────────────────────────────────────────────────────────────────
#  1. NHIỆM VỤ: CHO ĂN (10 LẦN BOOST + ĐÀO)
# ─────────────────────────────────────────────────────────────────
def do_feed_tasks():
    if progress["feed_done"]:
        return

    log("🍖", "=== [1/4] TIẾN HÀNH CHO ĂN (ĐÀO COIN) ===", Fore.YELLOW)
    while progress["feed"] < 10:
        tok_res = api("ads_token", type="boost")
        tok = tok_res.get("token")
        if not tok:
            break
        
        b = api("start_boost", ads_ok=tok)
        if b.get("ok"):
            progress["feed"] += 1
            log("  ⚡", f"Boost lượt #{progress['feed']}/10 thành công", Fore.CYAN)
            time.sleep(1)
            tap = api("tap")
            if tap.get("ok"):
                log("  🍖", f"Đã cho ăn: +{tap.get('added', 0):,} coin", Fore.GREEN)
            time.sleep(1)
        else:
            err = b.get("error", "")
            if "đủ 10" in err or "hết" in err:
                progress["feed"] = 10
                progress["feed_done"] = True
                log("  ✅", "Đã đạt giới hạn 10 lượt cho ăn hôm nay!", Fore.GREEN)
            break

    # Đào vét hết các lượt còn dư
    while True:
        tap = api("tap")
        if tap.get("ok"):
            log("  🍖", f"Đào vét: +{tap.get('added', 0):,} coin", Fore.GREEN)
            if tap.get("left", 0) <= 0:
                break
            time.sleep(1)
        else:
            break

    if progress["feed"] >= 10:
        progress["feed_done"] = True

# ─────────────────────────────────────────────────────────────────
#  2. NHIỆM VỤ: MỞ RƯƠNG (10 LẦN)
# ─────────────────────────────────────────────────────────────────
def do_chest_tasks():
    if progress["chest_done"]:
        return

    log("📦", "=== [2/4] TIẾN HÀNH MỞ RƯƠNG ===", Fore.YELLOW)
    while progress["chest"] < 10:
        tok_res = api("ads_token", type="chest")
        tok = tok_res.get("token")

        r = api("open_chest", ads_ok=tok if tok else "")
        if r.get("ok"):
            progress["chest"] += 1
            log("  💎", f"Mở rương #{progress['chest']}/10: +{r.get('reward', 0):,} coin", Fore.GREEN)
            if r.get("left", 0) <= 0:
                progress["chest"] = 10
                progress["chest_done"] = True
                break
            time.sleep(1.2)
        else:
            err = r.get("error", "")
            if "hết lượt" in err:
                progress["chest"] = 10
                progress["chest_done"] = True
                log("  ✅", "Đã hoàn thành mở rương tối đa hôm nay!", Fore.GREEN)
            break

# ─────────────────────────────────────────────────────────────────
#  3. NHIỆM VỤ: CÂU HỎI (TRẢ LỜI ĐỦ 10 CÂU TRẮC NGHIỆM)
# ─────────────────────────────────────────────────────────────────
def do_quiz_tasks():
    if progress["quiz_done"]:
        return

    log("❓", "=== [3/4] TIẾN HÀNH TRẢ LỜI CÂU HỎI (QUIZ) ===", Fore.YELLOW)
    while progress["quiz"] < 10:
        q_res = api("quiz_get")
        if not q_res.get("ok") or not q_res.get("quiz"):
            break

        quiz = q_res["quiz"]
        q_id = quiz["id"]
        q_text = quiz.get("question", "")
        options = quiz.get("options", [])

        # Thử từng đáp án để luôn chọn đúng 100%
        solved = False
        for opt_idx, opt_text in enumerate(options):
            time.sleep(0.8)
            ans = api("quiz_answer", quiz_id=q_id, option=opt_idx)
            if ans.get("ok") and ans.get("correct"):
                progress["quiz"] += 1
                log("  🎯", f"Câu #{progress['quiz']}/10: '{q_text}' ➔ Đúng: [{opt_text}] (+{ans.get('reward', 0):,} coin)", Fore.GREEN)
                solved = True
                break
            elif "10 câu" in ans.get("error", ""):
                progress["quiz"] = 10
                progress["quiz_done"] = True
                log("  ✅", "Đã hoàn thành đủ 10/10 câu hỏi hôm nay!", Fore.GREEN)
                return

        if not solved and not progress["quiz_done"]:
            time.sleep(1)

    if progress["quiz"] >= 10:
        progress["quiz_done"] = True

# ─────────────────────────────────────────────────────────────────
#  4. NHIỆM VỤ 1 - 2 - 3 (MONETAG ADS: MỖI NV 10 LẦN)
# ─────────────────────────────────────────────────────────────────
def do_monetag_tasks():
    all_done = progress["task1_done"] and progress["task2_done"] and progress["task3_done"]
    if all_done:
        return

    log("📺", "=== [4/4] TIẾN HÀNH NHIỆM VỤ 1 - 2 - 3 (MONETAG) ===", Fore.YELLOW)
    tasks = [
        ("task1", "Nhiệm vụ 1", "monetag1"),
        ("task2", "Nhiệm vụ 2", "monetag2"),
        ("task3", "Nhiệm vụ 3", "monetag3"),
    ]

    for key, name, src in tasks:
        if progress[f"{key}_done"]:
            continue

        res = api("reward", amount=300, source=src)
        if res.get("status") == "ok":
            progress[key] += 1
            log("  ✅", f"{name}: Hoàn thành lần #{progress[key]}/10 (+300 coin)", Fore.GREEN)
            if progress[key] >= 10:
                progress[f"{key}_done"] = True
        else:
            err = res.get("error", "")
            if "hết lượt" in err or "10" in err:
                progress[key] = 10
                progress[f"{key}_done"] = True
                log("  ✅", f"{name}: Đã làm đủ 10 lần hôm nay!", Fore.GREEN)
            else:
                log("  ⏳", f"{name} (#{progress[key]}/10): {err}", Fore.LIGHTBLACK_EX)
        time.sleep(1)

# ─────────────────────────────────────────────────────────────────
#  CÀY THÊM SMART LINK & ĐIỂM DANH TRONG LÚC CHỜ
# ─────────────────────────────────────────────────────────────────
SMART_TASKS = [
    "task6", "task9", "task10", "task11", "task12", "task13", "task14",
    "task15", "task16", "task17", "task18", "task19", "task20", "task21",
    "task22", "task23", "task24", "task25", "task26", "task27", "task28",
    "task29", "task30", "task31", "task32", "task33", "task34", "task35",
    "task36", "task37"
]

def do_extra_smartlinks():
    api("daily_claim")
    api("task7")
    api("task8")
    for tid in SMART_TASKS:
        api(tid)
        time.sleep(0.3)

# ─────────────────────────────────────────────────────────────────
#  KIỂM TRA HOÀN THÀNH VÀ ĐIỀU KHIỂN
# ─────────────────────────────────────────────────────────────────
def is_all_ranking_tasks_completed():
    return (
        progress["feed_done"] and
        progress["chest_done"] and
        progress["quiz_done"] and
        progress["task1_done"] and
        progress["task2_done"] and
        progress["task3_done"]
    )

def print_dashboard(profile):
    coins = profile.get("coins", 0) if profile else 0
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  📊 BẢNG TIẾN ĐỘ NHIỆM VỤ XẾP HẠNG TRONG NGÀY                     ║
╠══════════════════════════════════════════════════════════════════╣
║  🦴 Cho ăn (Boost+Đào)  : {progress['feed']:>2}/10  {'✅ Xong' if progress['feed_done'] else '⏳ Đang làm'}
║  📦 Mở rương            : {progress['chest']:>2}/10  {'✅ Xong' if progress['chest_done'] else '⏳ Đang làm'}
║  ❓ Trả lời câu hỏi     : {progress['quiz']:>2}/10  {'✅ Xong' if progress['quiz_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 1 (Monetag): {progress['task1']:>2}/10  {'✅ Xong' if progress['task1_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 2 (Monetag): {progress['task2']:>2}/10  {'✅ Xong' if progress['task2_done'] else '⏳ Đang làm'}
║  🎬 Nhiệm vụ 3 (Monetag): {progress['task3']:>2}/10  {'✅ Xong' if progress['task3_done'] else '⏳ Đang làm'}
╠══════════════════════════════════════════════════════════════════╣
║  💰 Số dư hiện tại      : {coins:>10,} Coins (~{coins*0.02:,.2f} VNĐ)
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}""")

def reset_daily_progress():
    global progress
    progress = {
        "feed": 0, "chest": 0, "quiz": 0,
        "task1": 0, "task2": 0, "task3": 0,
        "feed_done": False, "chest_done": False, "quiz_done": False,
        "task1_done": False, "task2_done": False, "task3_done": False,
    }
    log("🌅", "ĐÃ SANG NGÀY MỚI (00:00 GMT+7)! RESET BẢNG TIẾN ĐỘ ĐỂ ĐUA TOP!", Fore.GREEN)

# ─────────────────────────────────────────────────────────────────
#  CHƯƠNG TRÌNH CHÍNH
# ─────────────────────────────────────────────────────────────────
def main():
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  🏆 BOT ĐUA TOP XẾP HẠNG 24/7 - FILE 2 (@gaylobucu)              ║
║  📌 Mục tiêu: Hoàn tất 10 lần Cho ăn, Rương, Quiz, NV 1-2-3     ║
║  🌙 Đủ 10 lần ➔ Ngủ đến 00:00 GMT+7 thức dậy chạy tiếp            ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

    u = refresh_profile()
    if not u:
        log("❌", "Token INIT_DATA không hợp lệ hoặc đã hết hạn!", Fore.RED)
        return

    log("👤", f"Tài khoản: {u.get('name')} (@{u.get('username')})", Fore.GREEN)

    while True:
        # 1. Chạy Cho ăn
        do_feed_tasks()

        # 2. Chạy Mở rương
        do_chest_tasks()

        # 3. Chạy Trả lời câu hỏi
        do_quiz_tasks()

        # 4. Chạy Nhiệm vụ 1, 2, 3 (Monetag)
        do_monetag_tasks()

        # 5. Cày phụ Smartlinks trong lúc rảnh
        do_extra_smartlinks()

        # Cập nhật số dư & In bảng điều khiển
        curr_u = refresh_profile()
        print_dashboard(curr_u)

        # 6. KIỂM TRA ĐÃ HOÀN THÀNH 10/10 TẤT CẢ CHƯA
        if is_all_ranking_tasks_completed():
            sec_to_midnight = get_seconds_until_midnight_vn()
            hrs, rem = divmod(sec_to_midnight, 3600)
            mins, secs = divmod(rem, 60)

            print("\n" + "="*66)
            log("🎉", "CHÚC MỪNG! ĐÃ HOÀN THÀNH 10/10 TẤT CẢ NHIỆM VỤ XẾP HẠNG HÔM NAY!", Fore.GREEN)
            log("🌙", f"Cho bot ngủ đến 00:00:05 GMT+7 ngày mai (còn {hrs}h {mins}m {secs}s)...", Fore.MAGENTA)
            print("="*66 + "\n")

            time.sleep(sec_to_midnight)
            reset_daily_progress()
            continue

        # Nếu chưa xong hết (thường do NV 1-2-3 phải chờ cooldown 10 phút)
        log("⏳", "Chờ 10 phút hồi Cooldown của Nhiệm Vụ 1-2-3 để làm lượt tiếp theo...", Fore.LIGHTBLACK_EX)
        for remaining in range(600, 0, -10):
            mins, secs = divmod(remaining, 60)
            print(f"\r{Fore.CYAN}⏰ Lượt tiếp theo sẽ chạy sau: {mins:02d}:{secs:02d}... {Style.RESET_ALL}", end="", flush=True)
            time.sleep(10)
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⛔ Đã dừng bot.{Style.RESET_ALL}")
