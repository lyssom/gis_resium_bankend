from flask import Flask, send_from_directory, jsonify, render_template, request, send_file, Response
from flask_cors import CORS
# from gis_operator.space_distance import get_space_distance
import os
import json
import uuid

app = Flask(__name__)
CORS(app)  # 允许跨域

# 瓦片文件夹路径
TILES_DIR = os.path.abspath("./datas/example/fy_dem/terrain")  # 替换为你的瓦片文件夹路径


@app.route('/')
def serve_index():
    return render_template('index.html')


@app.route('/cesium/<path:filename>')
def serve_cesium(filename):
    static_folder='./static/cesium'
    return send_from_directory(static_folder, filename)

@app.route('/tiles/<int:z>/<int:x>/<int:y>.terrain')
def get_tile(z, x, y):
    # 构建瓦片路径
    tile_path = os.path.join(TILES_DIR, str(z), str(x), f"{y}.terrain")
    if not os.path.exists(tile_path):
        return jsonify({"error": "Tile not found"}), 404
    dtile = os.path.join(TILES_DIR, str(z), str(x))
    response = send_from_directory(dtile, f"{y}.terrain")
    response.headers['Content-Encoding'] = 'gzip'  # 添加 gzip 编码响应头
    response.headers['Content-Type'] = 'application/octet-stream'
    return response

# 提供瓦片文件
@app.route('/tiles/layer.json')
def get_layer():
    dtile = os.path.join(TILES_DIR)
    return send_from_directory(dtile, "layer.json")

HMTILES_DIR = os.path.abspath("./datas/hm/terrain")
@app.route('/hmtiles/<int:z>/<int:x>/<int:y>.terrain')
def get_hm_tile(z, x, y):
    # 构建瓦片路径
    tile_path = os.path.join(HMTILES_DIR, str(z), str(x), f"{y}.terrain")
    if not os.path.exists(tile_path):
        return jsonify({"error": "Tile not found"}), 404
    dtile = os.path.join(HMTILES_DIR, str(z), str(x))
    response = send_from_directory(dtile, f"{y}.terrain")
    response.headers['Content-Encoding'] = 'gzip'  # 添加 gzip 编码响应头
    response.headers['Content-Type'] = 'application/octet-stream'
    return response

# 提供瓦片文件
@app.route('/hmtiles/layer.json')
def get_hm_layer():
    dtile = os.path.join(HMTILES_DIR)
    return send_from_directory(dtile, "layer.json")

CLWXTILES_DIR = os.path.abspath("./datas/clwx/terrain")
@app.route('/clwxtiles/<int:z>/<int:x>/<int:y>.terrain')
def get_clwx_tile(z, x, y):
    # 构建瓦片路径
    tile_path = os.path.join(CLWXTILES_DIR, str(z), str(x), f"{y}.terrain")
    if not os.path.exists(tile_path):
        return jsonify({"error": "Tile not found"}), 404
    dtile = os.path.join(CLWXTILES_DIR, str(z), str(x))
    response = send_from_directory(dtile, f"{y}.terrain")
    response.headers['Content-Encoding'] = 'gzip'  # 添加 gzip 编码响应头
    response.headers['Content-Type'] = 'application/octet-stream'
    return response

# 提供瓦片文件
@app.route('/clwxtiles/layer.json')
def get_clwx_layer():
    dtile = os.path.join(CLWXTILES_DIR)
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

@app.route('/tiananmen/<int:z>/<int:x>/<int:y>.png')
def serve_tiananmen_tile(z, x, y):
    """服务瓦片数据"""
    # if not os.path.exists(f'./datas/tiananmen/{z}/{x}/{y}.png'):
    #     return send_from_directory(f'./datas/tiananmen/{16}/{53956}', f"{40703}.png")
    new_y = 2**z - y - 1
    return send_from_directory(f'./datas/tiananmen/{z}/{x}', f"{new_y}.png")


from tools.test_db import get_data

@app.route('/all/<int:z>/<int:x>/<int:y>.jpg')
def serve_all_tile(z, x, y):
    """服务瓦片数据"""
    print (z, x, y)
    d = get_data(z, x, y)
    # print(d)
    # # return send_from_directory(f'./datas/pm25/{z}/{x}', f"{y}.png")
    # import sqlite3

    # # 连接SQLite数据库
    # conn = sqlite3.connect('../datas/-04-02-All.db')
    # cursor = conn.cursor()

    # # 执行查询，获取BLOB数据
    # # cursor.execute("show databases")
    # cursor.execute("SELECT DataValue FROM ImgTable LIMIT 1")
    # # data = cursor.fetchone()[0]  # 获取BLOB数据

    # # # 将BLOB数据写入文件
    # # # with open('output_data.jpg', 'wb') as f:
    # # #     f.write(data)

    # # conn.close()
    # with open('./output_data.jpg') as d:
    #     d= d
    #     print(333)
    #     print(d)
    return Response(d, mimetype='image/jpeg')
    # image_path = './output_data.jpg'
    # return send_file(image_path, mimetype='image/jpeg')

@app.route('/shtower/tileset.json')
def get_sht_tileset():
    tileset_path = "./tileset.json"
    return send_from_directory('./datas/shanghaitower/shanghaitower', './tileset.json')

@app.route('/shtower/Data/<tile>/tileset.json')
def get_sht_tileset_detail_json(tile):
    tileset_path = "./tileset.json"
    print(666)
    print(f'./datas/shanghaitower/shanghaitower/Data/{tile}', './tileset.json')
    return send_from_directory(f'./datas/shanghaitower/shanghaitower/Data/{tile}', './tileset.json')

@app.route('/shtower/Data/<tile>/<filename>.b3dm')
def get_sht_tileset_detail(tile,filename):
    tileset_path = "./tileset.json"
    print(666)
    print(f'./datas/shanghaitower/shanghaitower/Data/{tile}', './tileset.json')
    return send_from_directory(f'./datas/shanghaitower/shanghaitower/Data/{tile}', f'./{filename}.b3dm')

@app.route('/get_scene_detail')
def get_scene_detail():
    params = request.args
    id = params.get('id')

    scene_folder = 'scene'
    scene_child_folder = f'{scene_folder}/scene_{id}/scene_detail.json'
    scene_code_folder = f'{scene_folder}/scene_{id}/scene_code.js'
    
    with open(scene_child_folder, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(scene_code_folder)
    with open(scene_code_folder, 'r', encoding='utf-8') as f:
        data['code'] = f.read()
    return jsonify(data)


@app.route('/get_scene_list')
def get_scene_list():
    scene_files = []
    folder_path = 'scene'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for idx, dir_name in enumerate(os.listdir(folder_path)):
        dir_path = os.path.join(folder_path, dir_name)
        print(dir_path)

        scene_id = dir_path.split('_')[-1]
        
        if os.path.isdir(dir_path):
            json_file_path = os.path.join(dir_path, 'scene_detail.json')
            print(f"Checking file: {json_file_path}")
            
            if os.path.exists(json_file_path):
                # 读取 scene_detail.json 文件并获取 name
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        scene_name = data.get('name')
                        if not scene_name:
                            scene_name = f"scene_{idx + 1}"
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in {json_file_path}")
                        continue  # 如果有错误，跳过当前文件
                
                # 添加到 scene_files 列表
                scene_files.append({
                    "id": scene_id,
                    "name": scene_name,
                    "path": json_file_path
                })
    
    print(scene_files)
    return scene_files


@app.route('/save_scene_detail', methods=['POST'])
def save_scene_detail():
    data = request.get_json()
    print(data)
    code = data.pop('code')
    id = uuid.uuid4().hex
    # json.dump(data, open('scene_detail.json', 'w'), ensure_ascii=False)

    scene_folder = 'scene'
    scene_child_folder = f'{scene_folder}/scene_{id}'

    if not os.path.exists(scene_folder):
        os.makedirs(scene_folder)
    if not os.path.exists(scene_child_folder):
        os.makedirs(scene_child_folder)
    with open(f'{scene_child_folder}/scene_detail.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  

    with open(f'{scene_child_folder}/scene_code.js', 'w', encoding='utf-8') as f:
        f.write(code)   
    return jsonify({"code": 0, "msg": "success"})


@app.route('/get_image_datas')
def get_image_datas():
    terrain_data = []
    tiles_data = []
    wms_data = []
    if os.path.exists('terrain.json'):
        with open('terrain.json', 'r', encoding='utf-8') as f:
            terrain_data = json.load(f)
    if os.path.exists('tiles.json'):
        with open('tiles.json', 'r', encoding='utf-8') as f:
            tiles_data = json.load(f)
    if os.path.exists('wms.json'):
        with open('wms.json', 'r', encoding='utf-8') as f:
            wms_data = json.load(f)
    return jsonify({"terrain_data": terrain_data, "tiles_data": tiles_data, "wms_data": wms_data})


@app.route('/save_image_data', methods=['POST'])
def save_image_data():
    data = request.get_json()

    # 检查 data 是否为 None
    if not data:
        return jsonify({"code": 1, "msg": "No JSON data provided"})

    print(data)
    print(data.get('data'))
    
    # 获取数据细节
    data_detail = data.get('data', {})
    data_type = data_detail.pop('data_type', None)

    data_detail['id'] = uuid.uuid4().hex

    # 确定文件名
    if data_type == 'terrain':
        file_name = 'terrain.json'
    elif data_type == 'WMS':
        file_name = 'wms.json'
    elif data_type == 'tiles':
        file_name = 'tiles.json'  # 修正为赋值
    else:
        return jsonify({"code": 0, "msg": "success"})  # 如果数据类型不匹配，则返回成功

    # 如果文件不存在，创建一个空的文件并写入数据
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump([data_detail], f, ensure_ascii=False, indent=4)
        return jsonify({"code": 0, "msg": "First data written to file"})

    # 读取文件数据，如果文件为空则初始化为空列表
    with open(file_name, 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []  # 如果文件格式错误，初始化为空列表

        if len(data) == 0:  # 文件为空，写入第一行数据
            data.append(data_detail)
            f.seek(0)  # 将文件指针移回文件开头
            json.dump(data, f, ensure_ascii=False, indent=4)
            return jsonify({"code": 0, "msg": "File was empty, first data written"})

        # 如果文件不为空，追加数据
        data.append(data_detail)
        f.seek(0)  # 将文件指针移回文件开头
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({"code": 0, "msg": "Data appended to file"})

@app.route('/ter_analysis/<filename>')
def get_ter_analysis_img(filename):
    return send_from_directory('static/ter_analysis', filename)

@app.route('/get_excavate_resource')
def get_excavate_resource():
    excavate_datas = []
    # http://127.0.0.1:8000/get_excavate_resource?lon=118.1&lat=39.9&hight=363
    
    params = request.args
    lon = float(params.get('lon', 0))
    lat = float(params.get('lat', 0))
    hight = float(params.get('hight', 0))
    print(lon)
    print(lat)
    print(hight)
    if os.path.exists('excavate.json'):
        with open('excavate.json', 'r', encoding='utf-8') as f:
            excavate_datas = json.load(f)

    print(excavate_datas)
    for data in excavate_datas:
        if data.get('start_lat') <= lat and lat <= data.get('end_lat') and data.get('start_lon') <= lon and lon <= data.get('end_lon'):
            print(data)
            for res_hight, resource in data.get('depths').items():
                print(hight)
                print(res_hight)
                if hight <= float(res_hight):
                    print(resource)
                    return jsonify(resource)
            return jsonify(resource)
    return jsonify({"bottom": "bottom_default.jpg", "side": "side_default.jpg"})


# 启动服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

