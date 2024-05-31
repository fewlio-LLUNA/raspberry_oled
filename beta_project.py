from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import Image, ImageOps, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time
import random
from datetime import datetime


# GPIOの警告を無効にします
GPIO.setwarnings(False)

# SPI接続の設定
serial = spi(device=0, port=0, gpio_DC=25, gpio_RST=27)
device = ssd1306(serial)

# 画像のパス
image_paths = [
    "/home/pi/beta_nomal01.png",
    "/home/pi/beta_nomal02.png",
    "/home/pi/beta_nomal03.png"
]

# フォントのパスとサイズ設定
font_path = "/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf"
font_size = 11
font = ImageFont.truetype(font_path, font_size)

# 挨拶の選択
def get_greeting():
    current_hour = datetime.now().hour
    if 6 <= current_hour <= 8:
        return "おはよう"
    elif 9 <= current_hour <= 16:
        return "こんにちは"
    else:
        return "こんばんは"

# テキスト設定
greet = get_greeting() # 表示したいテキスト
greet_x, greet_y = 67,26  # テキストの開始座標（画像の右側）

def load_and_prepare_image(image_path):
    
    image = Image.open(image_path)

    # 画像の色を反転
    image = ImageOps.invert(image.convert('RGB'))

    # OLEDディスプレイ用の背景画像を作成（ディスプレイの解像度に合わせる）
    background = Image.new('1', (device.width, device.height), "black")

    # 背景画像上の表示したい座標を設定

    x, y = 0, 0  # 画像を左上に配置

    # 背景画像に画像を貼付
    background.paste(image, (x, y))

    # テキストを描画
    draw = ImageDraw.Draw(background)
    draw.text((greet_x, greet_y), greet, font=font, fill="white")
    return background

# 初期画像をロード
background_images = [load_and_prepare_image(path) for path in image_paths]

while True:
    # 初期画像を表示
    device.display(background_images[0].convert('1'))

    # ランダムな秒数
    time_to_wait = random.randint(1, 10)
    time.sleep(time_to_wait)

    # アニメーションを表示
    for bg_image in background_images:
        device.display(bg_image.convert('1'))
        time.sleep(0.1)