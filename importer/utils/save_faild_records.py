import orjson


def save_failed_records(record: dict):
    with open("faild.txt", "a+") as f:
        f.write(orjson.dumps(record).decode() + "\n")
