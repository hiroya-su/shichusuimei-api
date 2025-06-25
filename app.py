from flask import Flask, request, jsonify
from sxtwl import fromSolar
from datetime import datetime

app = Flask(__name__)

GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
ZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
hour_branches = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
hour_ranges = [(23,1),(1,3),(3,5),(5,7),(7,9),(9,11),(11,13),(13,15),(15,17),(17,19),(19,21),(21,23)]
hour_gan_matrix = [
    ["甲","丙","戊","庚","壬","甲","丙","戊","庚","壬","甲","丙"],
    ["乙","丁","己","辛","癸","乙","丁","己","辛","癸","乙","丁"],
    ["丙","戊","庚","壬","甲","丙","戊","庚","壬","甲","丙","戊"],
    ["丁","己","辛","癸","乙","丁","己","辛","癸","乙","丁","己"],
    ["戊","庚","壬","甲","丙","戊","庚","壬","甲","丙","戊","庚"],
    ["己","辛","癸","乙","丁","己","辛","癸","乙","丁","己","辛"],
    ["庚","壬","甲","丙","戊","庚","壬","甲","丙","戊","庚","壬"],
    ["辛","癸","乙","丁","己","辛","癸","乙","丁","己","辛","癸"],
    ["壬","甲","丙","戊","庚","壬","甲","丙","戊","庚","壬","甲"],
    ["癸","乙","丁","己","辛","癸","乙","丁","己","辛","癸","乙"]
]

@app.route("/bazi")
def bazi():
    y = int(request.args.get("year"))
    m = int(request.args.get("month"))
    d = int(request.args.get("day"))
    h = int(request.args.get("hour"))

    dt = datetime(y, m, d, h)
    lunar = fromSolar(y, m, d)

    year_gz = GAN[lunar.getYearGZ().tg] + ZHI[lunar.getYearGZ().dz]
    month_gz = GAN[lunar.getMonthGZ().tg] + ZHI[lunar.getMonthGZ().dz]
    day_gz = GAN[lunar.getDayGZ().tg] + ZHI[lunar.getDayGZ().dz]

    for i, (start, end) in enumerate(hour_ranges):
        if (h >= start or (start > end and h < end)):
            hour_zhi = hour_branches[i]
            break
    hour_gan = hour_gan_matrix[lunar.getDayGZ().tg][hour_branches.index(hour_zhi)]
    hour_gz = hour_gan + hour_zhi

    return jsonify({
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "hour": hour_gz
    })

if __name__ == "__main__":
    app.run()
