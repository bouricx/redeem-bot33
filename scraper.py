import requests

API_URL = "https://www.nfkeys.store/api/keys/redeem"

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://www.nfkeys.store",
    "referer": "https://www.nfkeys.store/redeem",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
}


def redeem_key(key: str) -> dict:
    key = (key or "").strip()
    if not key:
        raise Exception("กรุณาใส่คีย์ก่อน")

    try:
        response = requests.post(
            API_URL,
            json={"code": key},
            headers=HEADERS,
            timeout=30,
        )
    except requests.Timeout:
        raise Exception("เซิร์ฟเวอร์ใช้เวลานานเกินไป ลองใหม่ภายหลัง")
    except requests.RequestException:
        raise Exception("เชื่อมต่อเซิร์ฟเวอร์ต้นทางไม่ได้")

    if response.status_code != 200:
        raise Exception(f"เว็บตอบกลับผิดพลาด (รหัส {response.status_code})")

    try:
        data = response.json()
    except ValueError:
        raise Exception("รูปแบบข้อมูลจากเซิร์ฟเวอร์ไม่ถูกต้อง")

    if data.get("result") != "ok":
        msg = data.get("message") or data.get("error") or "คีย์ไม่ถูกต้อง หรือถูกใช้ไปแล้ว"
        raise Exception(str(msg))

    profile_data = data.get("assignedProfile") or {}
    tokens = data.get("tokens") or {}

    return {
        "profile_name": profile_data.get("name", "-"),
        "avatar_url": profile_data.get("avatarUrl", ""),
        "plan_tier": data.get("planTier", "-"),
        "redeemed_ts": data.get("redeemedAt"),
        "expires_ts": data.get("expiresAt"),
        "profile_number": data.get("profileNumber", "-"),
        "slot": data.get("slot", "-"),
        "capacity": data.get("capacity", "-"),
        "links": {
            "pc": tokens.get("desktop", "") or "",
            "mobile": tokens.get("mobile", "") or "",
            "tv": tokens.get("tv", "") or "",
        },
    }
