# import trimesh
# import json
# from shapely.geometry import Polygon, mapping

# def obj_to_geojson(obj_file, output_geojson):
#     # 读取 OBJ 文件
#     scene = trimesh.load(obj_file)
#     print(scene.get('material', {}))


#     # 检查是否是 Scene 对象
#     # if isinstance(scene, trimesh.Scene):
#     #     # 合并所有网格，或者选择第一个网格
#     #     if scene.geometry:
#     #         mesh = list(scene.geometry.values())[0]  # 取第一个网格
#     #     else:
#     #         print("Error: No mesh found in OBJ file.")
#     #         return
#     # else:
#     #     mesh = scene  # 直接是 Trimesh 对象

#     # # 获取顶点数据
#     # vertices = mesh.vertices
#     # faces = mesh.faces
    
#     # features = []

#     # # 遍历每个面，并转换为 GeoJSON 格式
#     # print(111)
#     # for face in faces:
#     #     # print(2222)
#     #     polygon = Polygon([vertices[i][:2] for i in face])  # 只取 x, y 坐标
#     #     feature = {
#     #         "type": "Feature",
#     #         "geometry": mapping(polygon),
#     #         "properties": {}
#     #     }
#     #     features.append(feature)

#     # # 构造 GeoJSON
#     # print()
#     # geojson = {
#     #     "type": "FeatureCollection",
#     #     "features": features
#     # }

#     # # 保存为 GeoJSON 文件
#     # with open(output_geojson, "w") as f:
#     #     json.dump(geojson, f, indent=4)

# # 示例
# # obj_to_geojson("model.obj", "output.geojson")


# # 示例
# print(666)
# obj_to_geojson('./static/shtProduction.obj', "./static/sht.geojson")
# print(6661)


# # import fbx
# # import os

# # def extract_fbx_data(fbx_file):
# #     # 初始化FBX管理器和场景
# #     manager = fbx.FbxManager()
# #     scene = fbx.FbxScene(manager, "scene")
# #     importer = fbx.FbxImporter(manager, "")

# #     # 导入FBX文件
# #     if not importer.importer(fbx_file):
# #         print("Error importing FBX file.")
# #         return

# #     importer.import(scene)

# #     # 提取几何数据（顶点和面）
# #     geometry_data = []
# #     for i in range(scene.getChildCount()):
# #         node = scene.getChild(i)
# #         for j in range(node.getMeshCount()):
# #             mesh = node.getMesh(j)
# #             # 获取顶点坐标
# #             vertices = mesh.getControlPoints()
# #             faces = mesh.getPolygonVertices()

# #             vertex_data = []
# #             for vertex in vertices:
# #                 vertex_data.append([vertex[0], vertex[1], vertex[2]])

# #             # 获取面数据
# #             face_data = []
# #             for i in range(mesh.getPolygonCount()):
# #                 poly = []
# #                 for j in range(mesh.getPolygonSize(i)):
# #                     poly.append(faces[mesh.getPolygonVertex(i, j)])
# #                 face_data.append(poly)

# #             geometry_data.append({
# #                 "vertices": vertex_data,
# #                 "faces": face_data
# #             })

# #     # 提取材质和纹理
# #     texture_data = []
# #     for i in range(scene.getChildCount()):
# #         node = scene.getChild(i)
# #         for j in range(node.getMaterialCount()):
# #             material = node.getMaterial(j)
# #             for texture_index in range(material.getTextureCount()):
# #                 texture = material.getTexture(texture_index)
# #                 if texture:
# #                     texture_file = texture.getFileName()
# #                     texture_data.append(texture_file)

# #     return geometry_data, texture_data

# # def save_to_file(geometry_data, texture_data, output_file="output.json"):
# #     import json
# #     data = {
# #         "geometry": geometry_data,
# #         "textures": texture_data
# #     }

# #     with open(output_file, "w") as f:
# #         json.dump(data, f, indent=2)

# #     print(f"Data saved to {output_file}")

# # if __name__ == "__main__":
# #     fbx_file = "../static/shtProduction.fbx"  # 替换为你的FBX文件路径
# #     geometry_data, texture_data = extract_fbx_data(fbx_file)
# #     save_to_file(geometry_data, texture_data)


from trimesh.exchange.obj import load_obj
import trimesh

# 读取 obj 和 mtl
with open('./static/shtProduction.obj', "r") as f:
    obj_data = load_obj(f)

# 获取几何数据
mesh = trimesh.Trimesh(**obj_data["geometry"])

# 获取材质信息
mtl_info = obj_data.get("material", {})

print("材质信息:", mtl_info)
