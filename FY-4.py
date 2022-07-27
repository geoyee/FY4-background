import requests
import os
import win32api, win32con, win32gui
from PIL import Image
import numpy as np
import time

# 爬取风云四数据
def _get_fy_img():
    url = 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG'
    res = requests.get(url)
    # 保存壁纸
    with open('background.jpg', 'wb') as f:
        f.write(res.content)
    # 保存风云数据
    timer = str(time.strftime("%Y-%m-%d-%H", time.localtime()))
    with open('datas(FY-4)\\' + timer + '.jpg', 'wb') as f:
        f.write(res.content)
    return timer  # 返回时间用于处理图像

# 设置为壁纸
def set_background(imgpath):
    keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imgpath, win32con.SPIF_SENDWININICHANGE)

# 图像获取和处理
def get_and_deal_img():
    ex_bg = True
    fy_path = 'datas(FY-4)\\' + _get_fy_img() + '.jpg'
    bk_path = 'background.jpg'
    # 读图像（大小2198,2198,3）
    fy_img = np.array(Image.open(fy_path))
    bk_img = np.array(Image.open(bk_path))
    # 删除图像
    os.remove(fy_path)
    os.remove(bk_path)
    ## 处理水印
    # 左上水印
    fy_img[0:174, 0:447, :] = 0
    bk_img[0:174, 0:447, :] = 0
    # 右下水印
    fy_img[1970:2198, 1750:2198, :] = 0
    bk_img[1970:2198, 1750:2198, :] = 0
    # 扩展壁纸到电脑显示器大小
    bk_img = Image.fromarray(np.uint8(bk_img))
    bk_img = bk_img.resize((720, 720), Image.ANTIALIAS)
    bks_img = np.zeros((1080, 1920, 3))
    bks_img[180:900, 600:1320, :] = bk_img
    if np.all(bks_img == 0):
        ex_bg = False
    # 重新保存图像
    Image.fromarray(np.uint8(fy_img)).save(fy_path)
    Image.fromarray(np.uint8(bks_img)).save(bk_path)
    # 加载桌面
    path = os.getcwd()
    if ex_bg:
        set_background(os.path.join(path, bk_path))

if __name__ == '__main__':
    get_and_deal_img()
