from datetime import datetime, timezone, timedelta
from anvi.db.client import get_db

db = get_db()

# =======================
# WALLET HELPERS
# =======================


def get_wallet_balance(user_id: int) -> int:
    res = (
        db.table("user_wallet")
        .select("balance")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not res or not res.data:
        return 0

    return res.data["balance"]


def add_wallet_balance(user_id: int, amount: int):
    current = get_wallet_balance(user_id)
    new_balance = current + amount

    db.table("user_wallet").upsert(
        {
            "user_id": user_id,
            "balance": new_balance,
        }
    ).execute()


def set_wallet_balance(user_id: int, amount: int):
    db.table("user_wallet").upsert(
        {
            "user_id": user_id,
            "balance": amount,
        }
    ).execute()


# =======================
# DAILY HELPERS
# =======================


def get_last_daily(user_id: int):
    res = (
        db.table("user_daily")
        .select("last_daily")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not res or not res.data or res.data["last_daily"] is None:
        return None

    return datetime.fromisoformat(res.data["last_daily"])


def set_last_daily(user_id: int):
    db.table("user_daily").upsert(
        {
            "user_id": user_id,
            "last_daily": datetime.now(timezone.utc).isoformat(),
        }
    ).execute()


# =======================
# BANK HELPERS
# =======================


def get_bank_balance(user_id: int) -> int:
    res = (
        db.table("user_bank")
        .select("balance")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not res or not res.data:
        return 0

    return res.data["balance"]


def add_bank_balance(user_id: int, amount: int):
    current = get_bank_balance(user_id)
    new_balance = current + amount

    db.table("user_bank").upsert(
        {
            "user_id": user_id,
            "balance": new_balance,
        }
    ).execute()


def get_last_interest(user_id: int):
    res = (
        db.table("user_bank")
        .select("last_interest")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not res or not res.data or res.data["last_interest"] is None:
        return None

    return datetime.fromisoformat(res.data["last_interest"])


def set_last_interest(user_id: int):
    db.table("user_bank").upsert(
        {
            "user_id": user_id,
            "last_interest": datetime.now(timezone.utc).isoformat(),
        }
    ).execute()


def apply_bank_interest(user_id: int, rate: float = 0.02) -> int:
    """
    Applies bank interest once every 24 hours.
    Returns the interest gained (0 if none).
    """
    now = datetime.now(timezone.utc)

    res = (
        db.table("user_bank")
        .select("balance, last_interest")
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not res or not res.data:
        return 0

    balance = res.data.get("balance", 0)
    last_interest = res.data.get("last_interest")

    if balance <= 0:
        return 0

    if last_interest:
        last_time = datetime.fromisoformat(last_interest)
        if now - last_time < timedelta(hours=24):
            return 0

    interest = int(balance * rate)

    db.table("user_bank").upsert(
        {
            "user_id": user_id,
            "balance": balance + interest,
            "last_interest": now.isoformat(),
        }
    ).execute()

    return interest
