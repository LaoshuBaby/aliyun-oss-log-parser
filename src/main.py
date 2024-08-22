import os
import time

WORK_DIR = "."
output_file = "data.log"


def get_working_dir():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            WORK_DIR = f.read()
    return WORK_DIR

def get_file_list(dir):
    f_list_raw=os.listdir(dir)
    f_list=[]
    for i in f_list_raw:

        if os.path.isdir(os.path.join(WORK_DIR,i)):
            pass
        else:
            f_list.append(i)
    print(f_list[0])
    print(len(f_list))
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
def main():
    WORK_DIR = get_working_dir()
    file_list = get_file_list(WORK_DIR)
    file_total = len(file_list)
    print(f"[INFO] Total files: {file_total}")

    file_thershold = 20
    log_data = []
    for count, file_name in enumerate(file_list[:file_thershold], start=1):
        with open(
            os.path.join(WORK_DIR, file_name), "r", encoding="UTF-8"
        ) as file:
            raw_data = file.read().split("\n")
            # raw_data=list(filter(bool,raw_data))
            log_data.extend(raw_data)
            print(f"[READ]: ({count}/{file_total}) = {file_name}")

    print(f"[INFO]: Total log lines = {len(log_data)}")

    if os.path.exists(os.path.join(WORK_DIR, "data"))==False:
        os.mkdir(os.path.join(WORK_DIR, "data"))
    with open(
        os.path.join(WORK_DIR, "data", output_file), "w", encoding="utf-8"
    ) as file:
        file.write("\n".join(log_data))


if __name__ == "__main__":
    main()
