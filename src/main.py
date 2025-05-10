import json
import os
import re
import time
from typing import Optional, Union

import pandas as pd

WORK_DIR = os.path.join(
    os.environ.get("USERPROFILE"), ".aliyun-oss-log-parser"
)
DATA_FILE = "data.log"


def get_config():
    default_config = {
        "data_dir": "/root",
        "file_threshold": 0,
        "mode_output": ".log",
        "flag_rapid": False,
    }
    config_path = os.path.join(WORK_DIR, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.loads(f.read())
        return config
    else:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    default_config,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
            )
        return default_config


def get_working_dir():
    env_path = os.path.join(WORK_DIR, ".env")
    print(env_path)
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            DATA_DIR = f.read()
    return DATA_DIR


def get_file_list(dir):
    f_list_raw = os.listdir(dir)
    f_list = []
    for i in f_list_raw:
        if os.path.isdir(os.path.join(WORK_DIR, i)):
            pass
        else:
            f_list.append(i)
    return f_list


def timing_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        use_time = end_time - start_time
        print(f"[TIME] {func.__name__} took {use_time:.2f}s")
        return result

    return wrapper


@timing_wrapper
def main() -> Optional[Union[dict, str]]:
    DATA_DIR = get_config()["data_dir"]
    file_list = get_file_list(DATA_DIR)
    file_total = len(file_list)
    print(f"[INFO] Total files: {file_total}")

    mode_output = (
        get_config().get("mode_output", None)
        if get_config().get("mode_output", None)
        else ".log"
    )
    flag_rapid = (
        get_config().get("flag_rapid", None)
        if get_config().get("flag_rapid", None)
        else False
    )

    # mode_output: .log/.csv/.json

    log_data = []
    file_threshold = get_config()["file_threshold"]
    for count_file, file_name in enumerate(
        file_list[
            : (file_threshold if file_threshold != 0 else len(file_list))
        ],
        start=1,
    ):
        with open(
            os.path.join(DATA_DIR, file_name), "r", encoding="UTF-8"
        ) as file:
            raw_data = file.read().split("\n")
            # raw_data=list(filter(bool,raw_data))
            log_data.extend(raw_data[:-1])
            if flag_rapid is not True:
                print(f"[READ]: ({count_file}/{file_total}) = {file_name}")

    print(f"[INFO]: Total log lines = {len(log_data)}")

    if mode_output == ".log":
        output_data = "\n".join(log_data)
    elif mode_output == ".csv":
        # import pandas
        columns = ['ip', 'datetime', 'method', 'url', 'protocol', 'status', 'size', 'time', 'referer', 'user_agent', 'bucket', 'request_id', 'is_authenticated', 'operation', 'resource', 'object_key', 'backend_time', 'error_code', 'total_time', 'request_time', 'storage_class']
        data = []
        pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<url>[^ ]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\d+) (?P<time>\d+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)" "(?P<bucket>[^"]+)" "(?P<request_id>[^"]+)" "(?P<is_authenticated>[^"]+)" "-" "(?P<operation>[^"]+)" "(?P<resource>[^"]+)" "(?P<object_key>[^"]+)" - (?P<backend_time>\d+) "(?P<error_code>[^"]*)" (?P<total_time>\d+) "(?P<request_time>\d+)" - "-" "(?P<storage_class>[^"]+)" "-" "-" "-"'


        for line in log_data:
            match = re.match(pattern, line)
            if match:
                data.append(match.groups())

        df = pd.DataFrame(data, columns=columns)
        print(df)
        output_data=str(df)
    elif mode_output == ".json":
        import pandas

    if os.path.exists(WORK_DIR) == False:
        os.mkdir(WORK_DIR)
    with open(
        os.path.join(WORK_DIR, DATA_FILE), "w", encoding="utf-8"
    ) as file:
        file.write(output_data)


if __name__ == "__main__":
    main()
