import subprocess
import time
import csv

def run_command(cmd, label, iteration, total):
    """运行命令并返回执行时间（秒）"""
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end = time.time()
    elapsed = end - start

    print(f"[{iteration}/{total}] {label} | 耗时: {elapsed:.4f} 秒")
    if result.stderr:
        print(f"错误信息: {result.stderr.strip()}")
    return elapsed

def trimmed_mean(times, trim_ratio=0.05):
    """去掉前后一定比例的数据后求均值"""
    n = len(times)
    k = int(n * trim_ratio)
    sorted_times = sorted(times)
    trimmed = sorted_times[k: n - k] if n > 2 * k else sorted_times
    return sum(trimmed) / len(trimmed)

if __name__ == "__main__":
    commands = {
        "download_parallel_5": [
            "python3", "-m", "client.cli", "download", "1404",
            "tests/storage_data/download_data.txt", "--parallel", "--workers", "5"
        ],
        "download_parallel_25": [
            "python3", "-m", "client.cli", "download", "1404",
            "tests/storage_data/download_data.txt", "--parallel", "--workers", "25"
        ],
        "download_parallel_50": [
            "python3", "-m", "client.cli", "download", "1404",
            "tests/storage_data/download_data.txt", "--parallel", "--workers", "50"
        ],
        "download_parallel_100": [
            "python3", "-m", "client.cli", "download", "1404",
            "tests/storage_data/download_data.txt", "--parallel", "--workers", "100"
        ]
    }

    with open("command_times02.csv", "w", newline="") as f:
        writer = csv.writer(f)
        header = ["command"] + [f"run{i}" for i in range(1, 101)] + ["average_raw", "average_trimmed"]
        writer.writerow(header)

        for label, cmd in commands.items():
            print(f"\n>>> 开始执行命令: {label}\n")
            times = []
            total = 100
            for i in range(1, total + 1):
                elapsed = run_command(cmd, label, i, total)
                times.append(elapsed)

            avg_raw = sum(times) / len(times)
            avg_trimmed = trimmed_mean(times, trim_ratio=0.05)

            row = [label] + [f"{t:.4f}" for t in times] + [f"{avg_raw:.4f}", f"{avg_trimmed:.4f}"]
            writer.writerow(row)

            print(f">>> {label} 原始平均耗时: {avg_raw:.4f} 秒")
            print(f">>> {label} 去掉前后 5% 极端值后的平均耗时: {avg_trimmed:.4f} 秒\n")
