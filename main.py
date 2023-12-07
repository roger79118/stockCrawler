from stockpackage import twse


if __name__ == '__main__':
    print("Update comming soon!\n")

    data = twse.Company(2330)
    # res = data.today_info()
    # print(res)
    # res = data.month_info(2022, 2)
    # print(res)
    # res = data.day_info(2023, 11, 1)
    # print(res)
    # times = data.fmtdate()
    # print(times)
    data.save()