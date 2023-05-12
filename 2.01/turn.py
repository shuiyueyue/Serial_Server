import cv2
import os

# 读取视频文件
cap = cv2.VideoCapture("images/car_1.mp4")

# 设置每次读取的帧数
batch_size = 100

# 创建文件夹用于保存图片
if not os.path.exists("images1"):
    os.makedirs("images1")

# 循环读取视频帧并保存为图片
idx = 0
while True:
    # 读取一批视频帧
    frames = []
    for i in range(batch_size):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    # 处理视频帧
    for frame in frames:
        # 对视频帧进行处理
        # ...

        # 保存为图片
        cv2.imwrite(f"images1/{idx}.jpg", frame)
        idx += 1

    if not ret:
        break

# 释放视频文件
cap.release()
