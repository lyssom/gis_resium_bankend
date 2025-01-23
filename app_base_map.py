from flask import Flask, Response, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # 允许跨域

def get_data(z, x, y):
    conn = sqlite3.connect('./-04-02-All.db')
    cursor = conn.cursor()
    sql = f"SELECT TileLevel, TileCol, TileRow FROM ImgTable limit 10"
    cursor.execute(sql)
    rows = cursor.fetchall()

    # z-4解决场景Level对应关系问题，需要正确的关系进行调整
    sql = f"SELECT DataValue FROM ImgTable where TileLevel = {z-4} and TileCol = {x} and TileRow = {y}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None
    data = rows[0][0]  # 获取BLOB数据

    # with open(f'output_data_{z}{x}{y}.jpg', 'wb') as f:
    #     f.write(data)

    conn.close()
    return data

# @app.route('/all/<int:z>/<int:x>/<int:y>.jpg')
# def serve_all_tile(z, x, y):
#     """服务瓦片数据"""
#     d = get_data(z, x, y)
#     return Response(d, mimetype='image/jpeg')

@app.route('/all/<int:z>/<int:x>/<int:y>.png')
def serve_all_tile(z, x, y):
    """服务瓦片数据"""
    print (z, x, y)
    # return send_from_directory(f'./tianditu_tiles/{z}/{x}', f"{y}.png")
    return send_from_directory(f'./osm_tiles1/{z}/{x}', f"{y}.png")


# 启动服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

# 这个是完整的python 
# 安装好python环境后
# 在命令行输入
# pip install flask
# pip install flask-cors
# 将要加载的-04-02-All.db底图文件放在app_base_map.py同级目录下
# 执行python app_base_map.py

# 代码编辑器中，编写（注意端口号）
# //移除默认底图
# var baseLayer = viewer.imageryLayers.get(0);
# viewer.imageryLayers.remove(baseLayer);

# //加载自定义底图
# var xyz = new Cesium.UrlTemplateImageryProvider({
#   "url": 'http://127.0.0.1:8001/all/{z}/{x}/{y}.jpg'
# })
# viewer.imageryLayers.addImageryProvider(xyz)