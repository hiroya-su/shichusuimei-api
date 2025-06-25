from flask import Flask, request, jsonify
from flask_cors import CORS
from sxtwl import fromSolar
from datetime import datetime

app = Flask(__name__)
CORS(app)

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

@app.route("/bazi")
def bazi():
    y = int(request.args.get("year"))
    m = int(request.args.get("month"))
    d = int(request.args.get("day"))
    h = int(request.args.get("hour"))

    # sxtwl で節入り補正つきの干支を取得
    lunar = fromSolar(y, m, d)

    year_gz = GAN[lunar.getYearGZ().tg] + ZHI[lunar.getYearGZ().dz]
    month_gz = GAN[lunar.getMonthGZ().tg] + ZHI[lunar.getMonthGZ().dz]
    day_gz = GAN[lunar.getDayGZ().tg] + ZHI[lunar.getDayGZ().dz]

    # 時柱（正確な節入り補正つき）
    hour_gz_raw = lunar.getHourGZ(h)
    hour_gz = GAN[hour_gz_raw.tg] + ZHI[hour_gz_raw.dz]

    return jsonify({
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "hour": hour_gz
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
