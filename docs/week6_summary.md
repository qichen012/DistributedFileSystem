# 第六周项目总结

## 一、本周目标
1. 支持客户端并行上传与下载，提高大文件传输效率；  
2. 对大文件进行上传/下载测试，并记录耗时；  
3. 使用压力测试工具 wrk/ab 模拟高并发请求，验证节点性能；  
4. 为后续性能优化和异步改造提供数据参考。

---

## 二、完成情况

### 1. 并行上传
- 新增 `upload_file_parallel()`，支持多线程上传 chunk。  
- CLI 新增参数 `--workers`，可配置并行线程数。  

### 2. 并行下载
- 新增 `download_file_parallel()`，支持多线程下载。  
- 避免副本冗余下载：只下载一份成功副本。  

### 3. 大文件测试
- 在 `tests/large_file_test.py` 中自动生成大文件并进行测试；  
- 使用 `time.time()` 记录上传/下载耗时。  

### 4. 压力测试
- 使用 wrk 模拟并发请求，测试存储节点接口：  
  ```bash
  wrk -t4 -c100 -d30s "http://localhost:9001/get_chunk?file_id=1&chunk_index=0"


所得到的数据和表格均在项目根目录中   logs/bench......  为压力测试结果
/command_times.csv 为真实大文件测试结果表