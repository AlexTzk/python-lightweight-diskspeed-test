import os
import time
from flask import Flask, request

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file_size_mb = int(request.form.get("filesize", 100))

        test_file = "disk_speed_test.tmp"
        try:
            write_speed = test_write_speed(test_file, file_size_mb)

            read_speed = test_read_speed(test_file)

            return f"""
            <h2>Disk Speed Test Results</h2>
            <p><strong>File size:</strong> {file_size_mb} MB</p>
            <p><strong>Write Speed:</strong> {write_speed:.2f} MB/s</p>
            <p><strong>Read Speed:</strong> {read_speed:.2f} MB/s</p>
            <a href="/">Back</a>
            """
        finally:
            # Clean up the temporary file
            if os.path.exists(test_file):
                os.remove(test_file)

    return """
    <h2>Disk Speed Test</h2>
    <form method="POST">
      <label for="filesize">File Size (MB):</label>
      <input type="text" name="filesize" value="100">
      <input type="submit" value="Test Speed">
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
