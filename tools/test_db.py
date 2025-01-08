import sqlite3

# 连接SQLite数据库

def get_data(z, x, y):
    print (111)
    conn = sqlite3.connect('./datas/-04-02-All.db')
    cursor = conn.cursor()

    # 执行查询，获取BLOB数据
    sql = f"SELECT DataValue FROM ImgTable where TileLevel = {z-4} and TileCol = {x} and TileRow = {y}"
    print(sql)
    cursor.execute(sql)

    # cursor.execute("SELECT DataValue FROM ImgTable limit 1")
    print(1111)
    rows = cursor.fetchall()
    print(len(rows))
    # print(cursor.fetchone())
    if len(rows) == 0:
        return None
    print(222)
    # print(cursor.fetchone())
    print(2223)
    data = rows[0][0]  # 获取BLOB数据
    print(333)
    print(data[:100])
    print(data[-100:])
    print(33311)

    # 将BLOB数据写入文件
    with open(f'output_data_{z}{x}{y}.jpg', 'wb') as f:
        f.write(data)

    conn.close()
    # data = None
    

    return data