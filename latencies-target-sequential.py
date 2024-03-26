import requests
import threading
import time

# 定义请求URL
base_url = "https://cmpt756-yildpitzqa-uw.a.run.app" # 你的URL
image_to_text_url = f"{base_url}/image_to_text"
sentiment_analysis_url = f"{base_url}/sentiment_analysis"
translate_url = f"{base_url}/translate"
text_to_speech_url = f"{base_url}/text_to_speech"

# 上传图像文件并计算延迟 - sequential
def simulate_image_to_text(latencies, file_path, num_runs):
    latencies["image_to_text"] = []
    for _ in range(num_runs):
        thread = threading.Thread(target=upload_image_and_measure_latency, args=(latencies, file_path))
        thread.start()
        thread.join()
    print("Image to text simulation completed.")

# 分析情感并计算延迟 - sequential
def simulate_sentiment_analysis(latencies, text, num_runs):
    latencies["sentiment_analysis"] = []
    for _ in range(num_runs):
        thread = threading.Thread(target=analyze_sentiment_and_measure_latency, args=(latencies, text))
        thread.start()
        thread.join()
    print("Sentiment analysis simulation completed.")

# 翻译文本并计算延迟 - sequential
def simulate_translation(latencies, text, num_runs):
    latencies["translate"] = []
    for _ in range(num_runs):
        thread = threading.Thread(target=translate_text_and_measure_latency, args=(latencies, text))
        thread.start()
        thread.join()
    print("Translation simulation completed.")

# 文本转语音并计算延迟 - sequential
def simulate_text_to_speech(latencies, text, num_runs):
    latencies["text_to_speech"] = []
    for _ in range(num_runs):
        thread = threading.Thread(target=text_to_speech_and_measure_latency, args=(latencies, text))
        thread.start()
        thread.join()
    print("Text to speech simulation completed.")

# 上传图像文件并测量延迟
def upload_image_and_measure_latency(latencies, file_path):
    start_time = time.time()
    files = {'file': open(file_path, 'rb')}
    response = requests.post(image_to_text_url, files=files)
    latency = time.time() - start_time
    latencies["image_to_text"].append(latency)

# 分析情感并测量延迟
def analyze_sentiment_and_measure_latency(latencies, text):
    start_time = time.time()
    data = {'text': text}
    response = requests.post(sentiment_analysis_url, data=data)
    latency = time.time() - start_time
    latencies["sentiment_analysis"].append(latency)

# 翻译文本并测量延迟
def translate_text_and_measure_latency(latencies, text):
    start_time = time.time()
    data = {'text': text}
    response = requests.post(translate_url, data=data)
    latency = time.time() - start_time
    latencies["translate"].append(latency)

# 文本转语音并测量延迟
def text_to_speech_and_measure_latency(latencies, text):
    start_time = time.time()
    data = {'text': text}
    response = requests.post(text_to_speech_url, data=data)
    latency = time.time() - start_time
    latencies["text_to_speech"].append(latency)





# 模拟用户行为
def simulate_user(num_runs):
    file_path = "image.png"  # 你的图像文件路径
    text = "This is a sample text for sentiment analysis and translation."  # 你的文本
    ZN_text = "这是一个用于情感分析和翻译的示例文本。"  # 你的文本

    # 创建一个空字典用于存储延迟结果
    latencies = {
        "image_to_text": [],
        "sentiment_analysis": [],
        "translate": [],
        "text_to_speech": []
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
with open("latencies-target-sequential.txt", "w") as f:
        f.write("Latencies:\n")
        for key, values in latencies.items():
            f.write(f"{key}:\n")
            for i, value in enumerate(values):
                f.write(f"Run {i+1}: {value} seconds\n")
        f.write("\nAverage Latencies:\n")
        for key, value in average_latencies.items():
            f.write(f"{key}: {value} seconds\n")

