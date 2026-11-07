import redis
import utils

redis_config = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "decode_responses": True,
}


def get_and_maybe_update(address):
    entity_key = get_entity_key(address)
    r = redis.Redis(**redis_config)
    content = r.get(entity_key)
    if not content:
        content = get_address_content_from_provider(address)
        r.set(entity_key, json.dumps(content))
        return {"data": content, "meta": {"cache": "MISS"}}
    return {"data": json.loads(content), "meta": {"cache": "HIT"}}