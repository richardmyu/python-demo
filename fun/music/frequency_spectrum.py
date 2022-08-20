#!/usr/bin/env python3

import matplotlib.pyplot as plt
import librosa.display

# 音乐文件载入
audio_pth = 'haikuotiankong.mp3'
music, sr = librosa.load(audio_pth)

# 宽高比为 14:5 的图
plt.figure(figsize=(14, 5))
librosa.display.waveplot(music, sr=sr)

# 显示
plt.show()
