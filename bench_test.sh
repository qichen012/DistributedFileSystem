#!/bin/bash
# ============================
# Distributed File System 压力测试脚本 (含元数据接口自动检测)
# ============================

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/bench_$(date +%Y%m%d_%H%M%S).txt"

echo "🚀 压力测试开始，日志保存到: $LOG_FILE"
echo "================= 压力测试报告 =================" | tee -a "$LOG_FILE"
echo "时间: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# helper: 检查 URL 是否可用 (HTTP 200)
check_url_ok() {
  url="$1"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  if [ "$code" = "200" ]; then
    return 0
  else
    return 1
  fi
}

# ---------- 测试 1: 单节点下载能力 ----------
echo ">>> 测试 1: 单节点下载 (Node 9001)" | tee -a "$LOG_FILE"
wrk -t2 -c50 -d15s "http://localhost:9001/get_chunk?file_id=1509&chunk_index=0" 2>&1 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ---------- 测试 2: 多节点下载能力 ----------
echo ">>> 测试 2: 单节点下载 (Node 9002)" | tee -a "$LOG_FILE"
wrk -t4 -c100 -d30s "http://localhost:9002/get_chunk?file_id=1509&chunk_index=0" 2>&1 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ---------- 测试 3: 节点监控接口 ----------
echo ">>> 测试 3: 节点监控接口 (Node 9001)" | tee -a "$LOG_FILE"
ab -n 1000 -c 100 "http://127.0.0.1:9001/metries" 2>&1 | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ---------- 测试 4: 上传接口 ----------
echo ">>> 测试 4: 上传接口 (Node 9001)" | tee -a "$LOG_FILE"
echo "testdata" > post.txt
ab -n 500 -c 20 -p post.txt -T "application/x-www-form-urlencoded" "http://127.0.0.1:9001/store_chunk" 2>&1 | tee -a "$LOG_FILE"
rm -f post.txt
echo "" | tee -a "$LOG_FILE"

# ---------- 测试 5: 元数据服务查询（优先 file/list_file） ----------
echo ">>> 测试 5: 元数据服务查询 (尝试 file/list_file 到 node/list_nodes)" | tee -a "$LOG_FILE"

PRIMARY_URL="http://127.0.0.1:8000/file/list_files"
FALLBACK_URL="http://127.0.0.1:8000/node/list_nodes"

if check_url_ok "$PRIMARY_URL"; then
  echo "[INFO] 使用 $PRIMARY_URL 进行压测" | tee -a "$LOG_FILE"
  ab -n 1000 -c 50 "$PRIMARY_URL" 2>&1 | tee -a "$LOG_FILE"
elif check_url_ok "$FALLBACK_URL"; then
  echo "[INFO] $PRIMARY_URL 不可用，使用备选 $FALLBACK_URL 进行压测" | tee -a "$LOG_FILE"
  ab -n 1000 -c 50 "$FALLBACK_URL" 2>&1 | tee -a "$LOG_FILE"
else
  echo "[WARN] 两个元数据查询接口均不可用：$PRIMARY_URL, $FALLBACK_URL" | tee -a "$LOG_FILE"
  echo "[WARN] 跳过元数据服务压测" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"

echo "✅ 压力测试完成，结果保存在: $LOG_FILE"
