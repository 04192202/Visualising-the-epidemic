import time
import pymysql


# 获取系统时间
def get_sys_time():
    # 当前时间
    dt = time.strftime("%Y-%m-%d %X")
    return dt


# 获取数据库连接
def get_conn():
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', password='',
        database='cov', charset='utf8'
    )
    cursor = conn.cursor()
    return conn, cursor


# 释放资源
def close(conn, cursor):
    cursor.close()
    conn.close()


# 查询数据库数据
def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    return res


# 获取center1
def get_center1():
    # 查询详情表
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    # print(res)
    return res[0]


# 获取center2
def get_center2():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    print(res)
    return res


# 获取left1
def get_left1():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    print(res)
    return res


def get_left2():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    print(res)
    return res


# 获取right1
def get_right1():
    sql = 'SELECT city,confirm FROM ' \
          '(select city,confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    print(res)
    return res


def get_right2():
    sql = "select content from hotsearch order by id desc"
    res = query(sql)
    print(res)
    return res


def get_history_data(date=None):
    if not date:
        sql = "select * from history order by ds desc"
    else:
        sql = "select * from history where ds='{}'".format(date)
    res = query(sql)
    print(res)
    return res


def update_history_data(date, confirm, confirm_add, suspect, suspect_add, heal, heal_add, dead, dead_add):
    # 获取数据库连接
    conn, cursor = get_conn()
    sql = f"update history set confirm={confirm} ,confirm_add={confirm_add}, suspect={suspect}, " \
          f"suspect_add={suspect_add}, heal={heal}, heal_add={heal_add}, dead={dead}, dead_add={dead_add} where ds='{date}'"
    res = cursor.execute(sql)
    conn.commit()
    print(res)
    return res


def add_history_data(date, confirm, confirm_add, suspect, suspect_add, heal, heal_add, dead, dead_add):
    # 获取数据库连接
    sql = f"select * from history where ds='{date}'"
    res = query(sql)
    if res:
        update_history_data(date, confirm, confirm_add, suspect, suspect_add, heal, heal_add, dead, dead_add)
    else:
        conn, cursor = get_conn()
        sql = f"insert into history values('{date}', {confirm}, {confirm_add}, {suspect}, " \
              f"{suspect_add}, {heal}, {heal_add}, {dead}, {dead_add})"
        print(sql)
        res = cursor.execute(sql)
        conn.commit()
        print(res)
    return res


def delete_history_data(date):
    sql = f'delete from history where ds="{date}"'
    conn, cursor = get_conn()
    res = cursor.execute(sql)
    conn.commit()
    print(res)
    return res


if __name__ == '__main__':
    # get_center1()
    # get_center2()
    # get_left1()
    # get_left2()
    # get_right1()
    # get_right1()
    # delete_history_data()
    add_history_data('2020-09-21', '1', '1', '1', '1', '1', '1', '1', '1')
