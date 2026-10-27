"""
====================================================================
  🚀 AUTO BOT SIÊU CÀY TELEGRAM: @kiemtien6789_bot (TÀI KHOẢN 2)
  ⚡ Chế độ: SMART LINK & NHIỆM VỤ QUẢNG CÁO (CHẠY VĨNH VIỄN 24/7)
====================================================================
"""

import time
import random
import requests
from datetime import datetime
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
    "referer": "https://kien.kiemtienngay.us/public/nhiemvu.php",
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "accept": "*/*",
}

# Danh sách toàn bộ nhiệm vụ Smart Link có thể cày vĩnh viễn (cooldown 10 phút)
SMART_TASKS = [
    "task6", "task9", "task10", "task11", "task12", "task13", "task14",
    "task15", "task16", "task17", "task18", "task19", "task20", "task21",
    "task22", "task23", "task24", "task25", "task26", "task27", "task28",
    "task29", "task30", "task31", "task32", "task33", "task34", "task35",
    "task36", "task37"
]

# Nhiệm vụ quảng cáo Monetag (300 coin/lần)
MONETAG_TASKS = [
    {"name": "Nhiệm vụ 1 (Monetag)", "amount": 300, "source": "monetag1"},
    {"name": "Nhiệm vụ 2 (Monetag)", "amount": 300, "source": "monetag2"},
    {"name": "Nhiệm vụ 3 (Monetag)", "amount": 300, "source": "monetag3"}
]

# Thống kê toàn phiên
stats = {
    "total_earned": 0,
    "start_coins": 0,
    "current_coins": 0,
    "rounds": 0,
    "smart_success": 0,
    "monetag_success": 0,
    "chest_success": 0,
    "tap_success": 0,
    "chest_exhausted": False,
    "boost_exhausted": False,
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
        u = r["user"]
        stats["current_coins"] = u.get("coins", 0)
        if stats["start_coins"] == 0:
            stats["start_coins"] = stats["current_coins"]
        return u
    return None

# ─────────────────────────────────────────────────────────────────
#  1. AUTO SMART LINK (VĨNH VIỄN)
# ─────────────────────────────────────────────────────────────────
def run_smartlink_tasks():
    log("🔗", "=== BẮT ĐẦU CÀY SMART LINK TASKS ===", Fore.YELLOW)
    round_coins = 0
    success_count = 0

    for task_id in SMART_TASKS:
        res = api(task_id)
        status = res.get("status", "")
        reward = res.get("reward", 0)
        error = res.get("error", "")

        if status == "ok" or res.get("ok") is True:
            round_coins += reward
            success_count += 1
            stats["smart_success"] += 1
            log("  ✅", f"{task_id.upper()}: +{reward:,} coin", Fore.GREEN)
        elif "đợi" in error or "phút" in error:
            log("  ⏳", f"{task_id.upper()}: {error}", Fore.LIGHTBLACK_EX)
        else:
            log("  ℹ️", f"{task_id.upper()}: {error if error else res}", Fore.LIGHTYELLOW_EX)

        time.sleep(random.uniform(0.4, 0.9))

    log("💎", f"Tổng coin từ Smart Link vòng này: +{round_coins:,} coin ({success_count}/{len(SMART_TASKS)} task)", Fore.CYAN)
    return round_coins

# ─────────────────────────────────────────────────────────────────
#  2. AUTO MONETAG ADS (VĨNH VIỄN)
# ─────────────────────────────────────────────────────────────────
def run_monetag_ads():
    log("📺", "=== BẮT ĐẦU NHẬN COIN QUẢNG CÁO MONETAG ===", Fore.YELLOW)
    round_coins = 0

    for m in MONETAG_TASKS:
        res = api("reward", amount=m["amount"], source=m["source"])
        if res.get("status") == "ok":
            round_coins += m["amount"]
            stats["monetag_success"] += 1
            log("  ✅", f"{m['name']}: +{m['amount']} coin", Fore.GREEN)
        else:
            err = res.get("error", "Chưa sẵn sàng")
            log("  ⏳", f"{m['name']}: {err}", Fore.LIGHTBLACK_EX)
        time.sleep(random.uniform(0.5, 1.0))

    return round_coins

# ─────────────────────────────────────────────────────────────────
#  3. SPECIAL TASKS (Task 7, 8 & Daily)
# ─────────────────────────────────────────────────────────────────
def run_special_tasks():
    # Điểm danh
    d = api("daily_claim")
    if d.get("ok") and d.get("claimed"):
        log("🎁", f"Điểm danh ngày: +{d.get('amount', 0)} coin", Fore.GREEN)

    # Task 7 & Task 8 (nếu chưa nhận)
    for tid, name in [("task7", "Nhiệm vụ 7"), ("task8", "Nhiệm vụ 8")]:
        r = api(tid)
        if r.get("status") == "ok":
            log("🎉", f"{name}: +{r.get('reward', 0):,} coin", Fore.GREEN)
        time.sleep(0.5)

# ─────────────────────────────────────────────────────────────────
#  4. CHEST & BOOST (Bypass theo giới hạn ngày của server)
# ─────────────────────────────────────────────────────────────────
def run_daily_chest_and_tap():
    # Rương (nếu server còn lượt ngày)
    if not stats["chest_exhausted"]:
        for _ in range(6):
            r = api("open_chest")
            if r.get("ok"):
                stats["chest_success"] += 1
                log("📦", f"Rương: +{r.get('reward', 0):,} coin (còn {r.get('left', 0)} lượt)", Fore.GREEN)
                time.sleep(1)
            else:
                err = r.get("error", "")
                if "hết lượt" in err:
                    stats["chest_exhausted"] = True
                break

    # Boost + Đào
    if not stats["boost_exhausted"]:
        for _ in range(5):
            tok = api("ads_token", type="boost").get("token")
            if tok:
                b = api("start_boost", ads_ok=tok)
                if b.get("ok"):
                    tap = api("tap")
                    if tap.get("ok"):
                        stats["tap_success"] += 1
                        log("🍖", f"Đào sau Boost: +{tap.get('added', 0):,} coin", Fore.GREEN)
                    time.sleep(1)
                else:
                    if "đủ 10" in b.get("error", ""):
                        stats["boost_exhausted"] = True
                    break

# ─────────────────────────────────────────────────────────────────
#  CHƯƠNG TRÌNH CHÍNH (VÒNG LẶP VĨNH VIỄN 24/7)
# ─────────────────────────────────────────────────────────────────
def main():
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║  🔥 AUTO SMART LINK & MONETAG 24/7 - FILE 1 (@gaylobucu)        ║
║  ⭐ Tự cày 30+ Smart Links không giới hạn ngày                   ║
║  ⭐ Tự claim Monetag Ads mỗi 10 phút                            ║
║  ⭐ Tự mở rương & boost đào tối đa ngày                          ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

    u = refresh_profile()
    if not u:
        log("❌", "Không thể xác thực init_data! Vui lòng cập nhật chuỗi token.", Fore.RED)
        return

    log("👤", f"Tài khoản: {u.get('name')} (@{u.get('username')})", Fore.GREEN)
    log("💰", f"Số dư khởi điểm: {stats['current_coins']:,} Coins (~{stats['current_coins']*0.02:,.2f} VNĐ)", Fore.CYAN)

    COOLDOWN_LOOP = 600  # 10 phút chuẩn theo cooldown hệ thống

    while True:
        stats["rounds"] += 1
        print("\n" + "="*60)
        log("🔄", f"BẮT ĐẦU VÒNG CÀY #{stats['rounds']} ({datetime.now().strftime('%H:%M:%S')})", Fore.MAGENTA)
        print("="*60)

        # 1. Các nhiệm vụ thưởng đặc biệt / điểm danh
        run_special_tasks()

        # 2. Rương & Boost
        run_daily_chest_and_tap()

        # 3. Nhiệm vụ Monetag Ads
        run_monetag_ads()

        # 4. Toàn bộ 30+ Nhiệm vụ Smart Link
        run_smartlink_tasks()

        # 5. Cập nhật lại số dư
        curr_u = refresh_profile()
        coins_now = stats["current_coins"]
        profit = coins_now - stats["start_coins"]

        print("\n" + "-"*60)
        log("📊", f"KẾT QUẢ VÒNG #{stats['rounds']}:", Fore.CYAN)
        log("💰", f"Số dư hiện tại : {coins_now:,} Coins (~{coins_now*0.02:,.2f} VNĐ)", Fore.YELLOW)
        log("📈", f"Tổng lãi phiên : +{profit:,} Coins (~{profit*0.02:,.2f} VNĐ)", Fore.GREEN)
        print("-" * 60)

        # Đếm ngược 10 phút đến vòng kế tiếp
        log("⏳", f"Đang chờ hồi cooldown 10 phút ({COOLDOWN_LOOP}s) để cày tiếp vĩnh viễn...", Fore.LIGHTBLACK_EX)
        for remaining in range(COOLDOWN_LOOP, 0, -10):
            mins, secs = divmod(remaining, 60)
            print(f"\r{Fore.CYAN}⏰ Vòng #{stats['rounds'] + 1} sẽ bắt đầu sau: {mins:02d}:{secs:02d}... {Style.RESET_ALL}", end="", flush=True)
            time.sleep(10)
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⛔ Đã dừng tool cày tự động.{Style.RESET_ALL}")
