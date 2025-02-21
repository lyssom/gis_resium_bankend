import os
from osgeo import ogr
import sys

from osgeo import gdal


def list_all_drivers():
    # 获取驱动程序的数量
    driver_count = ogr.GetDriverCount()

    print(f"Total drivers: {driver_count}")
    
    # 遍历所有驱动并打印名称
    for i in range(driver_count):
        driver = ogr.GetDriver(i)
        print(f"{i + 1}: {driver.GetName()}")

def convert_dgn_to_geojson():
    # 注册GDAL的驱动
    print("GDAL Version:", gdal.VersionInfo())
    ogr.RegisterAll()

    # 打开DGN文件
    list_all_drivers()
    driver = ogr.GetDriverByName('CAD')
    if driver is None:
        print("DGN driver not available.")
        return
    
    # # 打开DGN文件
    input_dgn = './static/b.dwg'
    print(os.path.abspath(input_dgn))
    if not os.path.exists(input_dgn):
        print(f"Error: The file {input_dgn} does not exist.")
    dataset = driver.Open(input_dgn, 0)  # 0 means read-only mode
    if dataset is None:
        print(f"Failed to open file {input_dgn}")
        return
    
    # 获取图层
    layer = dataset.GetLayer()
    
    # 创建GeoJSON驱动
    geojson_driver = ogr.GetDriverByName('GeoJSON')
    if geojson_driver is None:
        print("GeoJSON driver not available.")
        return
    
    # 创建输出的GeoJSON文件
    output_geojson = './static/obbb.geojson'
    geojson_dataset = geojson_driver.CreateDataSource(output_geojson)
    if geojson_dataset is None:
        print(f"Failed to create file {output_geojson}")
        return

    # 创建图层
    geojson_layer = geojson_dataset.CreateLayer(
        layer.GetName(),
        geom_type=layer.GetGeomType()  # 保持相同的几何类型
    )

    # 复制字段
    layer_defn = layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        geojson_layer.CreateField(field_defn)

    # 复制要素
    for feature in layer:
        geojson_layer.CreateFeature(feature)

    # 清理
    dataset = None
    geojson_dataset = None

    # print(f"Conversion successful: {output_geojson}")

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("Usage: python dgn2geojson.py <input.dgn> <output.geojson>")
    #     sys.exit(1)
    
    # input_dgn = sys.argv[1]
    # output_geojson = sys.argv[2]
    
    # # 确保输入文件存在
    # if not os.path.exists(input_dgn):
    #     print(f"Input file {input_dgn} does not exist.")
    #     sys.exit(1)

    # # 执行转换
    convert_dgn_to_geojson()
