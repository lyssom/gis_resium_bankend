from osgeo_utils import gdal2tiles

gdal2tiles.main(["--xyz", "-z", "0-1", "all.tif", "base_map9"])