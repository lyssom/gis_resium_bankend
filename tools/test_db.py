import sqlite3


def get_data(z, x, y):
    conn = sqlite3.connect('./datas/-04-02-All.db')
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