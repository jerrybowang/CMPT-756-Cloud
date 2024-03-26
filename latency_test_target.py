import requests
import threading
import time

# 定义请求URL
base_url = "<url>" # 你的URL
# base_url = "http://localhost:8080" # 你的URL
translate_url = f"{base_url}/translate"



# 翻译文本并计算延迟 - sequential
def simulate_translation(latencies, text, num_runs):
    latencies["translate"] = []
    # 创建线程列表
    threads = []
    for _ in range(num_runs):
        thread = threading.Thread(target=translate_text_and_measure_latency, args=(latencies, text))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()
    print("Translation simulation completed.")



# 翻译文本并测量延迟
def translate_text_and_measure_latency(latencies, text):
    start_time = time.time()
    data = {'text': text}
    response = requests.post(translate_url, data=data)
    latency = time.time() - start_time
    latencies["translate"].append(latency)






# 模拟用户行为
def simulate_user(num_runs):
    file_path = "image.png"  # 你的图像文件路径
    text = "This is a sample text for sentiment analysis and translation."  # 你的文本
    ZN_text = "这是一个用于情感分析和翻译的示例文本。"  # 你的文本

    # 创建一个空字典用于存储延迟结果
    latencies = {
        "translate": []
    }

    # 创建线程列表
    threads = []

    # 创建并启动线程

    translate_thread = threading.Thread(target=simulate_translation, args=(latencies, ZN_text, num_runs))

    threads.append(translate_thread)


    for thread in threads:
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("All threads completed.")

    return latencies

# 运行模拟
num_runs = 20  # 每个请求运行的次数
latencies = simulate_user(num_runs)

# calculate average latency for each endpoint
average_latencies = {}
for key, value in latencies.items():
    try:
        average_latency = sum(value) / len(value)
    except ZeroDivisionError:
        average_latency = -1
    average_latencies[key] = average_latency

# save latencies to a file
with open("latencies-target.txt", "w") as f:
        f.write("Latencies:\n")
        for key, values in latencies.items():
            f.write(f"{key}:\n")
            for i, value in enumerate(values):
                f.write(f"Run {i+1}: {value} seconds\n")
        f.write("\nAverage Latencies:\n")
        for key, value in average_latencies.items():
            f.write(f"{key}: {value} seconds\n")

