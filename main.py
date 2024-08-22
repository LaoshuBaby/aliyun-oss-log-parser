import os
import time

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
def get_file_list(directory):
    return os.listdir(directory)

@timing_wrapper
def read_files(file_list):
    log_data = []
    for file_name in file_list:
        with open(file_name, "r", encoding="UTF-8") as file:
            log_data.extend(file.read().split("\n"))
    return log_data

@timing_wrapper
def write_log(log_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(log_data))

@timing_wrapper
def main():
    directory = "."
    file_list = get_file_list(directory)
    total_files = len(file_list)
    print(f"[INFO] Total files: {total_files}")

    files_to_process = file_list[:10]
    for count, file_name in enumerate(files_to_process, start=1):
        print(f"[READ] [{count}/{total_files}] {file_name}")

    log_data = read_files(files_to_process)
    print(f"[INFO] Total log lines: {len(log_data)}")

    output_file = "p.log"
    write_log(log_data, output_file)
    

if __name__ == "__main__":
    main()