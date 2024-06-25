# -*- coding: utf-8 -*-
"""teaching_data_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p71n3uN_C6DCd_8Q2sKgFlq_RdxMvjeT
"""

#Level1生成用のコード

from PIL import Image
import random
import os
import numpy as np
import math

# 1種類の画像のパスを設定
image_path = 'new_items/beaker.png'

# 画像を読み込む
image = Image.open(image_path).convert("RGBA")

# 背景画像のサイズを設定（例として画像のサイズを使用）
background_image_size = (1360, 1020)

label = []

# ランダムに拡大縮小し、回転させる関数
def overlay_single_image_randomly(image, background_image_size, num_overlays):
    base_image = Image.new('L', background_image_size, (255))
    placed_positions = []

    for _ in range(num_overlays):
        # ランダムに拡大縮小 (0.5と1はハイパーパラメータ)
        scale_factor = random.uniform(0.5, 1)
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        resized_image = image.resize(new_size, Image.LANCZOS)

        # ランダムに回転
        rotation_angle = random.randint(0, 360)
        rotated_image = resized_image.rotate(rotation_angle, expand=True)

        #ランダムに配置
        x_offset = random.randint(0, background_image_size[0] - rotated_image.width)
        y_offset = random.randint(0, background_image_size[1] - rotated_image.height)
        x_center = x_offset + rotated_image.width // 2
        y_center = y_offset + rotated_image.height // 2

        norm = np.linalg.norm(new_size)
        label.append((x_center/background_image_size[0], y_center/background_image_size[1], rotated_image.width/background_image_size[0], rotated_image.height/background_image_size[1]))
        # 台紙に重ね合わせ
        base_image.paste(rotated_image, (x_offset, y_offset), rotated_image)

    return base_image

# 生成する画像の枚数
num_generated_images = 10

# 出力ディレクトリを設定　→　generated_images1
output_directory = 'image_detection/generated_images1'
os.makedirs(output_directory, exist_ok=True)

# 複数枚のランダムに重ね合わせた画像を生成
for i in range(num_generated_images):
    # 1枚の画像に重ね合わせる数
    num_overlays_per_image = 1
    combined_image = overlay_single_image_randomly(image, background_image_size, num_overlays_per_image)
    output_image_path = os.path.join(output_directory, f'beaker_{i+1}.png')
    combined_image.save(output_image_path, quality=95)
    print(f"Combined image saved to: {output_image_path}")

    params_file_path = os.path.join(output_directory, f'beaker_{i+1}.txt')
    with open(params_file_path, 'w') as f:
      for i in range(num_overlays_per_image):
         f.write(f"{0} {label[i][0]} {label[i][1]} {label[i][2]} {label[i][3]}\n")
    print(f"Overlay parameters saved to: {params_file_path}")
    label = []