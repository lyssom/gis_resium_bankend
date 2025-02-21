import geojson
import xarray as xr
import numpy as np
import os

# from netCDF4 import Dataset
import netCDF4 as nc4

def netcdf_to_geojson(nc_file, lon_variable, lat_variable, data_variable, geojson_name):
    file_path = nc_file
    if os.path.exists(file_path):
        print("文件存在")
    else:
        print("文件不存在")
    # nc = nc4.Dataset(nc_file)
    
    # print(nc)
    ds = xr.open_dataset(nc_file)
    print(ds)
    
    # "reprojecting" by making new coordinate arrays following the equidistant cylindrical projection
    step_lon = 360 / ds[lon_variable].size
    step_lat = 180 / ds[lat_variable].size

    reproject_lon = np.arange(-180, 180, step_lon)
    reproject_lat = np.arange(-90, 90, step_lat)

    new_latitude_var = xr.DataArray(reproject_lat, dims="latitude")
    new_longitude_var = xr.DataArray(reproject_lon, dims="longitude")
    
    # update the dataset with new coordinate variables
    ds["latitude"] = new_latitude_var
    ds["longitude"] = new_longitude_var

    # identify key variables
    latitude = ds["latitude"]
    latitude_range = len(latitude)
    longitude = ds["longitude"]
    longitude_range = len(longitude)
    data_var = ds[data_variable].values

    
    print(data_var.shape)
    
    print(latitude)
    print(longitude)
    print(latitude_range)
    print(longitude_range)
    # loop over all coordinate pairs

    data = []
    for i in range(latitude_range):
        for j in range(longitude_range):
            lat = float(latitude[i])
            lon = float(longitude[j])
            # print (i,j)
            # print(data_var[:, :, i, j])
            # print(data_var.shape)
            # print(data_var[0, :, j, i])
            data_value = float(data_var[0, 0, i, j])
            print(data_value)

            data.append(data_value)

    #         # # Create a GeoJSON feature for each point
    #         point = geojson.Point((lon, lat))
    #         properties = {data_variable: data_value}
    #         feature = geojson.Feature(geometry=point, properties=properties)
    #         geojson_features.append(feature)
            if j > 100:
                break
        if i > 10:
            break
    
    # with open(geojson_name, "w") as f:
    #     geojson.dump(geojson.FeatureCollection(geojson_features), f)

    import json

    # with open('../2024122600.json', 'r') as f:
    #     data = json.load(f)
    #     print(len(data[0]['data']))

    # h1 = {
    #     "parameterCategory": 2,
    #     "parameterCategoryName": "Momentum",
    #     "parameterNumber": 2,
    #     "parameterNumberName": "U-component_of_wind",
    #     "nx": 360,
    #     "ny": 181,
    #     "lo1":0.0,"la1":90.0,"lo2":359.0,"la2":-90.0,
    #     "dx": 1.0,
    #     "dy": 1.0
    # }

    h2 = {
        "parameterCategory": 2,
        "parameterCategoryName": "Momentum",
        "parameterNumber": 3,
        "parameterNumberName": "U-component_of_wind"
        }

    h = {
        "parameterCategory": 2,
        "parameterCategoryName": "Momentum",
        "parameterNumber": 2,
        "parameterNumberName": "U-component_of_wind",
        "nx": 36,
        "ny": 18,
        "lo1": 0.0,
        "la1": 90.0,
        "lo2": 36,
        "la2": 18,
        "dx": 1.0,
        "dy": 1.0
        }

    with open('output.json', 'w') as out_file:

        # data = data[1]['data'][:int(len(data[1]['data'])/100)]
        print(len(data))
        print(min(data))
        print(max(data))
        # d = [{'header': h1, 'data': data}]  + [{'header': h2, 'data':data}] 
        # d = [{'header': h, 'data': data[1]['data']}]  + [{'header': h2, 'data': data[1]['data']}] 
        d = [{'header': h, 'data': data}]  + [{'header': h2, 'data': data}] 
        # d = {'header': data[1]['header'], 'data': data[1]['data']}
        json.dump(d, out_file, indent=4)




netcdf_to_geojson("./all_hisv2c_z_2120_20241020.nc", "lon", "lat", "temp", "./test112.geojson")

    