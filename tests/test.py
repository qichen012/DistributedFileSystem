import subprocess
import time
import csv

def run_command(cmd, label, iteration, total):
    """运行命令并返回执行时间（秒）"""
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end = time.time()
    elapsed = end - start

    # 打印执行情况 + 进度
    print(f"[{iteration}/{total}] {label} | 耗时: {elapsed:.4f} 秒")
    if result.stderr:
        print(f"错误信息: {result.stderr.strip()}")
    return elapsed

if __name__ == "__main__":
    commands = {
        "upload_parallel": [
            "python3", "-m", "client.cli", "upload",
            "tests/test.txt", "--parallel", "--workers", "10"
        ],
        "upload_replicas": [
            "python3", "-m", "client.cli", "upload",
            "tests/test.txt", "--replicas", "3", "--strategy", "round_robin"
        ],
        "download_parallel": [
            "python3", "-m", "client.cli", "download", "704",
            "tests/storage_data/download_data.txt", "--parallel", "--workers", "10"
        ],
        "download_id": [
            "python3", "-m", "client.cli", "download",
            "704", "tests/storage_data/download_data.txt"
        ]
    }

    # 打开 CSV 文件
    with open("command_times.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # 表头：command, run1, run2, ..., run100, average
        header = ["command"] + [f"run{i}" for i in range(1, 101)] + ["average"]
        writer.writerow(header)

        # 每个命令跑 100 次
        for label, cmd in commands.items():
            print(f"\n>>> 开始执行命令: {label}\n")
            times = []
            total = 100
            for i in range(1, total + 1):
                elapsed = run_command(cmd, label, i, total)
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)

            # 写一行：命令 + 每次耗时 + 平均值
            row = [label] + [f"{t:.4f}" for t in times] + [f"{avg_time:.4f}"]
            writer.writerow(row)

            print(f"\n>>> {label} 平均耗时: {avg_time:.4f} 秒\n")
