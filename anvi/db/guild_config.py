from anvi.db.client import get_db

TABLE = "guild_config"

def get_guild_config(guild_id: int):
    db = get_db()
    res = (
        db.table(TABLE)
        .select("*")
        .eq("guild_id", guild_id)
        .single()
        .execute()
    )
    return res.data

def set_modlog_channel(guild_id: int, channel_id: int):
    db = get_db()
    return (
        db.table(TABLE)
        .upsert({
            "guild_id": guild_id,
            "modlog_channel_id": channel_id,
        })
        .execute()
    )
