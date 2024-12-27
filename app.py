from flask import Flask, send_from_directory, jsonify, render_template, request
from flask_cors import CORS
from gis_operator.space_distance import get_space_distance
import os

app = Flask(__name__)
CORS(app)  # 允许跨域

# 瓦片文件夹路径
TILES_DIR = os.path.abspath("D:/新建文件夹/terrain")  # 替换为你的瓦片文件夹路径

@app.route('/')
def serve_index():
    return render_template('index.html')


@app.route('/cesium/<path:filename>')
def serve_cesium(filename):
    static_folder='./static/cesium'
    return send_from_directory(static_folder, filename)

# 提供瓦片文件
@app.route('/tiles/<int:z>/<int:x>/<int:y>.terrain')
def get_tile(z, x, y):
    # 构建瓦片路径
    tile_path = os.path.join(TILES_DIR, str(z), str(x), f"{y}.terrain")
    print(tile_path)
    print(666)
    if not os.path.exists(tile_path):
        print(6667)
        return jsonify({"error": "Tile not found"}), 404
    dtile = os.path.join(TILES_DIR, str(z), str(x))
    return send_from_directory(dtile, f"{y}.terrain")

# 提供瓦片文件
@app.route('/tiles/layer.json')
def get_layer():
    print(1111122)
    # 构建瓦片路径
    dtile = os.path.join(TILES_DIR)
    print("vvvv")
    print(send_from_directory(dtile, "layer.json"))

    print(2222)

    return send_from_directory(dtile, "layer.json")

@app.route('/tileset.json')
def get_tileset():
    tileset_path = "./tileset.json"
    return send_from_directory('./datas', './tileset.json')

@app.route('/NoLod_0.b3dm')
def get_NoLod():
    tileset_path = "./tileset.json"
    return send_from_directory('./datas', './NoLod_0.b3dm')

@app.route('/getSpaceDistance', methods=['POST'])
def getSpaceDistance():
    data = request.get_json()
    positions = data.get('positions')
    print(positions)
    return str(get_space_distance(positions))


@app.route('/pm25/<int:z>/<int:x>/<int:y>.png')
def serve_tile(z, x, y):
    """服务瓦片数据"""
    return send_from_directory(f'./datas/pm25/{z}/{x}', f"{y}.png")


# 启动服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

