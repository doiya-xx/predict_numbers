# 爬取"http://www.zcwnet.com/zcw/dpc/fcssq"网站的数据
# 获取页面中"2000期"的点击事件，
# 获取事件返回的表格信息
# 保存到".\spiders\numbers.csv"文件中

import json
import os
import csv
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 当前所在的目录
current_path = os.path.dirname(__file__)
# 如果".\spiders"目录不存在所在目录
if not os.path.exists(os.path.join(current_path, "spiders")):
    # 创建".\spiders"目录
    os.mkdir(os.path.join(current_path, "spiders"))

# 爬取"http://www.zcwnet.com/zcw/dpc/fcssq"网站的数据
def get_numbers():
    # POST "http://www.zcwnet.com/zcw/hisfc/fcssq"
    # 请求头
    # Accept: application/json, text/javascript, */*; q=0.01
    # Accept-Encoding: gzip, deflate
    # Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
    # Content-Length: 54
    # Content-Type: application/x-www-form-urlencoded
    # Cookie: JSESSIONID=ac60e645-e672-4f6c-8a81-fb275252f8eb; Hm_lvt_929da96c01241989409d8e51d2ac56b1=1681979836,1682061095,1682172876; Hm_lpvt_929da96c01241989409d8e51d2ac56b1=1682172876
    # Host: www.zcwnet.com
    # Origin: http://www.zcwnet.com
    # Proxy-Connection: keep-alive
    # Referer: http://www.zcwnet.com/zcw/dpc/fcssq
    # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
    # X-Requested-With: XMLHttpRequest
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        "Content-Length": "54",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.zcwnet.com",
        "Origin": "http://www.zcwnet.com"
    }
    # 请求参数
    # pageSize: 2000
    # pageNum: 1
    # orderByColumn: ctime
    # isAsc: desc
    data = {
        "pageSize": "2000",
        "pageNum": "1",
        "orderByColumn": "ctime",
        "isAsc": "desc",
    }
    # 发送请求
    response = requests.post("http://www.zcwnet.com/zcw/hisfc/fcssq", headers=headers, data=data)
    # 响应标头
    # Connection: keep-alive
    # Content-Type: application/json;charset=UTF-8
    # Date: Sat, 22 Apr 2023 14:38:08 GMT
    # Keep-Alive: timeout=4
    # Proxy-Connection: keep-alive
    # Server: nginx/1.18.0
    # Transfer-Encoding: chunked
    # 解析响应数据
    # 将json字符串转换为python对象
    json_data = response.json()
    # 把json_data转换为字符串，然后保存到"./spiders/resonse.json"文件中，需要美化json字符串
    # with open(os.path.join(current_path, "spiders", "resonse.json"), "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, indent=4 ,ensure_ascii=False)
    
    # 获取数据
    # json_data["rows"]是一个[[], [], ..., []]列表
    # []列表中的每个元素是一个字典{}
    # 字典中的key是'ctime', 'id', 'num', 'val', 'week'
    # 字典中的value是对应的值
    # 例如：json_data["rows"][0]["ctime"]是"2023-04-20 21:30:00"
    # 例如：json_data["rows"][0]["week"]是"周四"
    # 例如：json_data["rows"][0]["id"]是"2239"
    # 例如：json_data["rows"][0]["num"]是"2023044"
    # 例如：json_data["rows"][0]["val"]是"01,02,03,04,05,06,07"，其中前六个是红球，最后一个是蓝球，期望存到csv中红球和篮球分开
    # 期望的数据格式是一个一维列表，将json_data["rows"]转换为一维列表
    # 例如：["2023-04-20", "周四", "2239", "2023044", "01,02,03,04,05,06", "07"]

    numbers = []
    # 遍历json_data["rows"]列表
    for row in json_data["rows"]:
        # 创建一个列表
        number = []
        # 添加"2023-04-20"数据
        number.append(row["ctime"].split(" ")[0])
        # 添加"周四"数据
        number.append(row["week"])
        # 添加"2239"数据
        number.append(row["id"])
        # 添加"2023044"数据
        number.append(row["num"])
        # 添加"01,02,03,04,05,06"数据，并且转为String类型
        number.append(",".join(row["val"].split(",")[:-1]))
        # 添加"07"数据
        number.append(row["val"].split(",")[-1])
        # 添加到列表中
        numbers.append(number)
    # 返回数据
    return numbers



# 保存数据到".\spiders\numbers.csv"文件中
def save_numbers(numbers):
    # 打开文件
    with open(os.path.join(current_path, "spiders", "numbers.csv"), "w", encoding="utf-8-sig", newline="") as f:
        # 创建csv写入器
        writer = csv.writer(f)
        # 写入数据
        writer.writerows(numbers)


# 主函数
def main():
    # 爬取数据
    numbers = get_numbers()
    # 保存数据
    save_numbers(numbers)

# 判断是否是主函数
if __name__ == "__main__":
    # 执行主函数
    main()