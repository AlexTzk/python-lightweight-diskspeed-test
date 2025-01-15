import os
import time
from flask import Flask, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

test_results = []

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
        test_path = request.form.get("testpath") or "/app"

        os.makedirs(test_path, exist_ok=True)

        test_file = os.path.join(test_path, "disk_speed_test.tmp")

        try:
            write_speed = test_write_speed(test_file, file_size_mb)
            read_speed = test_read_speed(test_file)

            test_results.append({
                "file_size_mb": file_size_mb,
                "write_speed": write_speed,
                "read_speed": read_speed,
                "path": test_path
            })

            return f"""
            <h2>Disk Speed Test Results</h2>
            <p><strong>File Size:</strong> {file_size_mb} MB</p>
            <p><strong>Path:</strong> {test_path}</p>
            <p><strong>Write Speed:</strong> {write_speed:.2f} MB/s</p>
            <p><strong>Read Speed:</strong> {read_speed:.2f} MB/s</p>
            <a href="/">Run Another Test</a> | <a href="/graph">View Graph</a>
            """
        finally:
            # Clean up the temporary file
            if os.path.exists(test_file):
                os.remove(test_file)

    return """
    <h2>Disk Speed Test</h2>
    <form method="POST">
      <label for="filesize">File Size (MB):</label>
      <input type="text" name="filesize" value="100"><br><br>

      <label for="testpath">Optional Path in Container:</label>
      <input type="text" name="testpath" placeholder="/app"><br><br>

      <input type="submit" value="Test Speed">
    </form>
    <hr>
    <a href="/graph">View Graph of Previous Tests</a>
    """

@app.route("/graph")
def graph():
    if not test_results:
        return "<p>No tests have been run yet. <a href='/'>Go run a test</a>!</p>"

    x_vals = range(len(test_results))
    write_speeds = [r["write_speed"] for r in test_results]
    read_speeds  = [r["read_speed"] for r in test_results]
    labels       = [f'Size:{r["file_size_mb"]}MB\nPath:{r["path"]}' for r in test_results]

    plt.figure(figsize=(10, 6))
    bar_width = 0.4

    plt.bar([x - bar_width/2 for x in x_vals], write_speeds, width=bar_width, color='blue', label='Write MB/s')
    plt.bar([x + bar_width/2 for x in x_vals], read_speeds, width=bar_width, color='orange', label='Read MB/s')

    plt.xticks(ticks=x_vals, labels=labels, rotation=45, ha='right')
    plt.ylabel("Speed (MB/s)")
    plt.title("Disk Speed Tests")
    plt.legend()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    html = f"""
    <h2>Disk Speed Test Results Chart</h2>
    <img src="data:image/png;base64,{img_base64}" />
    <br><br>
    <a href="/">Back to Test</a>
    """
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
