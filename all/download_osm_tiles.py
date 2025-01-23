# import os
# import requests

# # 设置瓦片 URL 模板（天地图）
# TILE_URL = "http://t{s}.tianditu.gov.cn/vec_w/wmts?&tilematrixset=GoogleMapsCompatible&Service=WMTS&Request=GetTile&Version=1.0.0&Layer=vec&Style=default&Format=tiles&TileMatrix={z}&TileRow={y}&TileCol={x}"


# TILE_URL = "https://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=026b03720b382ed3ae221e3e96000214"
# # 设置下载目录
# OUTPUT_DIR = "tianditu_tiles"

# # 创建输出目录
# if not os.path.exists(OUTPUT_DIR):
#     os.makedirs(OUTPUT_DIR)


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Connection": "keep-alive",
#     "Cookie": "HWWAFSESID=be6ed8113ffa1ae3ee5; HWWAFSESTIME=1736903988489",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1"
# }

# # 下载瓦片的函数
# def download_tile(z, x, y):
#     # 替换 URL 模板中的变量
#     url = TILE_URL.replace("{s}", str((x + y) % 3))  # 选择服务器 t0, t1, t2（简单的负载均衡）
#     url = url.replace("{z}", str(z)).replace("{x}", str(x)).replace("{y}", str(y))
#     try:
#         # 发起请求获取瓦片
#         print(url)
#         response = requests.get(url, headers=headers)
#         print(response.status_code)
#         if response.status_code == 200:
#             # 保存瓦片到本地文件
#             zoom_dir = os.path.join(OUTPUT_DIR, str(z))
#             if not os.path.exists(zoom_dir):
#                 os.makedirs(zoom_dir)
#             level_dir = os.path.join(zoom_dir, str(x))
#             if not os.path.exists(level_dir):
#                 os.makedirs(level_dir)
#             tile_file = os.path.join(level_dir, f"{y}.png")
#             with open(tile_file, 'wb') as f:
#                 f.write(response.content)
#             print(f"Downloaded {tile_file}")
#         else:
#             print(f"Failed to download tile {z}-{x}-{y}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading tile {z}-{x}-{y}: {e}")

# # 设置要下载的区域，zoom level: 0-5，x 和 y 坐标
# for z in range(6, 10):  # Zoom level
#     for x in range(0, 2 ** z):  # X 坐标（取决于缩放级别）
#         for y in range(0, 2 ** z):  # Y 坐标（取决于缩放级别）
#             download_tile(z, x, y)


import os
import requests

# 设置瓦片 URL 模板
TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

# 设置下载目录
OUTPUT_DIR = "osm_tiles"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": "HWWAFSESID=be6ed8113ffa1ae3ee5; HWWAFSESTIME=1736903988489",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

# 创建输出目录
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 下载瓦片的函数
def download_tile(z, x, y):
    # 替换 URL 模板中的变量
    url = TILE_URL.replace("{s}", "a").replace("{z}", str(z)).replace("{x}", str(x)).replace("{y}", str(y))
    print(url)
    try:
        # 发起请求获取瓦片
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            zoom_dir = os.path.join(OUTPUT_DIR, str(z))
            if not os.path.exists(zoom_dir):
                os.makedirs(zoom_dir)
            level_dir = os.path.join(zoom_dir, str(x))
            if not os.path.exists(level_dir):
                os.makedirs(level_dir)
            tile_file = os.path.join(level_dir, f"{y}.png")
            with open(tile_file, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {tile_file}")
            # tile_file = os.path.join(OUTPUT_DIR, f"{z}-{x}-{y}.png")
            # with open(tile_file, 'wb') as f:
            #     f.write(response.content)
            print(f"Downloaded {tile_file}")
        else:
            print(f"Failed to download tile {z}-{x}-{y}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading tile {z}-{x}-{y}: {e}")

# 设置要下载的区域，zoom level: 0-5，x和y坐标
for z in range(0, 10):  # Zoom level
    for x in range(0, 2 ** z):  # X coordinates (depends on zoom level)
        for y in range(0, 2 ** z):  # Y coordinates (depends on zoom level)
            download_tile(z, x, y)
