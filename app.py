import os
from flask import Flask, render_template_string, request, send_file
import io
from PIL import Image

app = Flask(__name__)

BASE_DIR = os.getcwd()
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# 這裡保留你原本完整的對應表
ORACLE_FONT_MAP = {
    "新": "new.png", "年": "year.png", "快": "fast.png", "樂": "happy.png", "幸": "fortune.png","加": "add.png",
    "五": "five.png", "福": "blessing.png", "臨": "approach.png", "門": "door.png", 
    "招": "trick.png", "財": "fiscal.png", "進": "in.png", "寶": "precious.png", 
    "大": "big.png", "吉": "lucky.png", "利": "profit.png", "富": "rich.png", 
    "貴": "expensive.png", "祥": "xiang.png", "如": "if.png", "意": "meaning.png", 
    "日": "day.png", "斗": "dou.png", "金": "gold.png", "生": "born.png", 
    "興": "prosper.png", "隆": "prosperous.png", "四": "four.png", "季": "season.png", 
    "平": "flat.png", "安": "safe.png", "萬": "million.png", "象": "elephent.png", 
    "更": "even.png", "迎": "welcome.png", "春": "spring.png", "心": "heart.png", 
    "想": "think.png", "事": "thing.png", "成": "become.png", "壽": "birth.png", 
    "無": "no.png", "疆": "territory.png", "勝": "win.png", "亨": "heng.png", 
    "通": "through.png", "長": "long.png", "命": "life.png", "一": "one.png", "領": "lead.png",
    "團": "group.png", "和": "and.png", "氣": "gas.png", "有": "have.png", "謝": "thank.png",
    "餘": "remain.png", "豐": "affluent.png", "衣": "clothes.png", "足": "foot.png", 
    "食": "food.png", "源": "origin.png", "廣": "wide.png", "馬": "horse.png", "原": "origin.png", 
    "到": "arrive.png", "功": "achivement.png", "國": "country.png", "泰": "thai.png", 
    "民": "civil.png", "康": "healthy.png", "寧": "peaceful.png", "龍": "dragon.png", 
    "精": "fine.png", "神": "god.png", "恭": "gong.png", "喜": "like.png", "姚": "yao.png",
    '乾': "dry.png", "昆": "insect.png", "浩": "hao.png", "翰": "hang.png", "先": "gofirst.png",
    "發": "fa.png", "竭": "exhaust.png", "思": "consider.png", "遠": "far.png", "林": "lin.png",
    "慮": "concern.png", "妘": "yun.png", "若": "asif.png", "驚": "shock.png", "親": "kiss.png",
    "鴻": "bigbird.png","蓁": "zhen.png","身": "body.png","壯": "strong.png","力": "force.png",
    "健": "health.png","賀": "congratulations.png","禧": "Jubilee.png","立": "stand.png","元": "coin.png",
    "復": "again.png","始": "start.png","花": "flower.png","華": "flower.png","開": "open.png","榮": "glory.png",
    "滿": "full.png","出": "out.png","入": "comein.png","院": "yard.png","光": "ray.png","暉": "hui.png","輝": "hui.png",
    "展": "exhibition.png","圖": "pic.png","暖": "warm.png","本": "ori.png","貨": "product.png","輪":"wheel.png",
    "轉": "turn.png","客": "guest.png","似": "seemslike.png","雲": "cloud.png","來": "come.png","穀": "grain.png",
    "收": "receive.png","風": "wind.png","調": "adjust.png","雨": "rain.png","順": "shun.png","六": "six.png",
    "畜": "animal.png","旺": "flourish.png","步": "step.png","高": "high.png","陞": "lift.png","升": "lift.png",
    "學": "learn.png","業": "industry.png","路": "road.png","盈": "filled.png","達": "arrival.png","昌": "chang.png",
    "盛": "sheng.png","茂": "mao.png","銀": "silver.png","玉": "jade.png","堂": "hall.png","祿": "goodfortune.png",
    "瑞": "luck.png","慶": "celebrate.png","接": "catch.png","送": "deliver.png","舊": "old.png","歲": "age.png",
    "時": "time.png","節": "period.png","月": "moon.png","照": "shine.png","曜": "illuminate.png","耀": "illuminate.png",
    "登": "board.png","景": "view.png","初": "first.png","貞": "Chastity.png","天": "sky.png","地": "land.png",
    "人": "person.png","美": "beautiful.png","稱": "saythat.png","隨": "follow.png","願": "wish.png","就": "jiu.png",
    "基": "kee.png","宏": "magnificent.png","拓": "extend.png","集": "collect.png","德": "virtue.png","錦": "sew2.png",
    "仁": "Benevolence.png","里": "village.png","厚": "thick.png","道": "path.png","傳": "pass.png","家": "home.png",
    "久": "longtime.png","青": "bluegreen.png","永": "forever.png","駐": "stay.png","同": "together.png","壽": "lifetime.png",
    "宅": "home2.png","戶": "household.png","納": "accept.png","千": "thousand.png","歡": "joyous.png","笑": "laugh.png",
    "聚": "gather.png","圓": "circle.png","敦": "dun.png","睦": "Mutsumi.png","鄰": "neighbor.png","情": "affection.png",
    "深": "deep.png","似": "similar.png","海": "ocean.png","山": "mountain.png","流": "flow.png","延": "prolong.png",
    "綿": "cotton.png","葉": "leaf.png","近": "close.png","悅": "joy.png","闔": "entirefamily.png","𰻞": "1u;6.jpg",
    "三": "three.png","羊": "sheep.png","陽": "sun.png","回": "back.png","百": "hundred.png","洋": "foreign.png",
    "得": "get.png","揚": "raise.png","眉": "eyebrow.png","吐": "vomit.png","餐": "meal.png","奔": "run.png","繡": "sew.png"
    # ... 請在此處保留你原本長長的字體清單 ...
}

def remove_white_background(img, threshold=220):
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

def generate_oracle_couplet(text):
    char_count = len(text)
    if char_count == 0: return None

    if char_count == 1:
        CANVAS_W, canvas_h, CHAR_SIZE, paper_file = 400, 400, 250, "background_square2.png"
    else:
        CHAR_SIZE, CANVAS_W, SPACING, TOP_MARGIN = 175, 320, 200, 55
        canvas_h = char_count * SPACING + TOP_MARGIN
        paper_file = "background2.jpg"

    paper_path = os.path.join(BASE_DIR, paper_file)
    couplet_created = False
    
    if os.path.exists(paper_path):
        try:
            raw_paper = Image.open(paper_path).convert("RGBA")
            p_w, p_h = raw_paper.size
            if char_count == 1:
                src_ratio, dst_ratio = p_w / p_h, CANVAS_W / canvas_h
                if src_ratio > dst_ratio:
                    scale_factor = canvas_h / p_h
                    new_w = int(p_w * scale_factor)
                    resized_paper = raw_paper.resize((new_w, canvas_h), Image.Resampling.LANCZOS)
                    left = (new_w - CANVAS_W) // 2
                    couplet = resized_paper.crop((left, 0, left + CANVAS_W, canvas_h))
                else:
                    scale_factor = CANVAS_W / p_w
                    new_h = int(p_h * scale_factor)
                    resized_paper = raw_paper.resize((CANVAS_W, new_h), Image.Resampling.LANCZOS)
                    top = (new_h - canvas_h) // 2
                    couplet = resized_paper.crop((0, top, CANVAS_W, top + canvas_h))
            else:
                scale_factor = CANVAS_W / p_w
                new_paper_h = int(p_h * scale_factor)
                resized_paper = raw_paper.resize((CANVAS_W, new_paper_h), Image.Resampling.LANCZOS)
                if new_paper_h >= canvas_h:
                    top = (new_paper_h - canvas_h) // 2
                    couplet = resized_paper.crop((0, top, CANVAS_W, top + canvas_h))
                else:
                    couplet = resized_paper.resize((CANVAS_W, canvas_h), Image.Resampling.LANCZOS)
            couplet_created = True
        except Exception:
            pass
    
    if not couplet_created:
        couplet = Image.new("RGBA", (CANVAS_W, canvas_h), (180, 0, 0, 255))

    for i, char in enumerate(text):
        img_filename = ORACLE_FONT_MAP.get(char)
        if img_filename:
            img_path = os.path.join(ASSETS_DIR, img_filename)
            if os.path.exists(img_path):
                try:
                    char_img = Image.open(img_path).convert("RGBA")
                    char_img = remove_white_background(char_img, threshold=220)
                    char_img.thumbnail((CHAR_SIZE, CHAR_SIZE), Image.Resampling.LANCZOS)
                    cw, ch = char_img.size
                    x_pos = (CANVAS_W - cw) // 2
                    y_pos = (canvas_h - ch) // 2 if char_count == 1 else (i * SPACING) + TOP_MARGIN
                    couplet.paste(char_img, (x_pos, y_pos), char_img)
                except Exception:
                    pass
    return couplet

# 🌐 網頁路由設定：首頁畫面 (簡單的輸入框)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>甲骨文春聯產生器</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f7f7f7; }
        input[type="text"] { padding: 10px; font-size: 16px; width: 250px; }
        button { padding: 10px 20px; font-size: 16px; background-color: #b40000; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🏮 甲骨文春聯線上產生器 🏮</h1>
    <form action="/generate" method="get">
        <input type="text" name="text" placeholder="請輸入春聯文字 (如: 新年快樂)" required>
        <button type="submit">生成春聯</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate')
def generate():
    user_input = request.args.get('text', '').strip()
    img = generate_oracle_couplet(user_input)
    if img:
        # 將 PIL 圖片轉成記憶體中的二進位檔案，直接傳送給瀏覽器顯示
        img_io = io.BytesIO()
        img.convert("RGB").save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return "生成失敗，請檢查輸入的字是否有在字典中！"

# ⚠️ Render 部署關鍵：動態綁定 Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)