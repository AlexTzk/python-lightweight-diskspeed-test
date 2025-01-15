import os
import time

def test_write_speed(file_path, file_size_mb=100):
    data_size_bytes = file_size_mb * 1024 * 1024
    data = os.urandom(data_size_bytes)

    start_time = time.time()
    with open(file_path, 'wb') as f:
        f.write(data)
    end_time = time.time()

    elapsed = end_time - start_time
    mb_per_second = file_size_mb / elapsed
    return mb_per_second

def test_read_speed(file_path):
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    start_time = time.time()
    with open(file_path, 'rb') as f:
        _ = f.read()
    end_time = time.time()

    elapsed = end_time - start_time
    mb_per_second = file_size_mb / elapsed
    return mb_per_second

def main():
    test_file = "disk_speed_test.tmp"
    file_size_mb = 1000  # Adjust this value if you want a larger or smaller test file
    
    try:
        print(f"Creating and writing a {file_size_mb} MB file to measure write speed...")
        write_speed = test_write_speed(test_file, file_size_mb)
        print(f"Write Speed: {write_speed:.2f} MB/s\n")

        print("Reading the file to measure read speed...")
        read_speed = test_read_speed(test_file)
        print(f"Read Speed: {read_speed:.2f} MB/s\n")

    finally:
        # Clean up the temporary file
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    main()
