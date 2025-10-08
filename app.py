import streamlit as st
from datetime import date, datetime
from PIL import Image
import json
import os
import time

# 设置页面
st.set_page_config(page_title="我的日记", page_icon="📔", layout="centered")

# 创建文件夹和路径
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
settings_file = "data/settings.json"
diary_file = os.path.join("data", "diary.json")

# 加载或创建设置
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {}

# 背景图片设置
bg_url = st.text_input(
    "背景图片 URL（留空使用默认）",
    value=settings.get("bg_url", "https://images.unsplash.com/photo-1503264116251-35a269479413")
)

# 保存设置
settings["bg_url"] = bg_url
with open(settings_file, "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)

# 设置背景 CSS
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('{bg_url}');
        background-size: cover;
        background-attachment: fixed;
    }}
    section[data-testid="stAppViewContainer"] > div {{
        background-color: rgba(255,255,255,0.85);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 页面标题和鼓励语
st.title("📔 我的日记")
st.markdown(f"📅 **{date.today()}**")
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
    <style>
    .custom-font {
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 26px;
    }
    </style>
    <div class="custom-font">
        💖 亲爱的吴思楠，今天也要快乐啊！！！
    </div>
""", unsafe_allow_html=True)

# 获取今天日期和季节
today = datetime.today()
month = today.month

if month in [3, 4, 5]:
    season = "spring"
elif month in [6, 7, 8]:
    season = "summer"
elif month in [9, 10, 11]:
    season = "autumn"
else:
    season = "winter"

# 加载日记数据
if os.path.exists(diary_file):
    with open(diary_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# 日记输入表单
entry_date = st.date_input("日期", value=date.today())
uploaded_file = st.file_uploader("上传照片（可选）", type=["jpg", "jpeg", "png"])
score = st.slider("心情评分", 0.0, 10.0, 7.0, step=0.5)
note = st.text_area("今天记录", height=200)

# 保存日记按钮逻辑
if st.button("💾 保存日记"):
    if note.strip() == "":
        st.warning("请填写日记内容再保存哦～")
    else:
        image_path = ""
        if uploaded_file is not None:
            timestamp = int(time.time())
            fname = f"{timestamp}_{uploaded_file.name}"
            save_path = os.path.join("uploads", fname)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            image_path = save_path

        entry = {
            "date": str(entry_date),
            "score": float(score),
            "note": note,
            "image": image_path,
            "saved_at": int(time.time())
        }

        data.append(entry)

        with open(diary_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        st.success("✅ 日记已保存！")
        st.balloons()

# 🎂 生日祝福
if today.month == 8 and today.day == 19:
    st.balloons()
    st.markdown("🎂 **亲爱的吴思楠，生日快乐呀！！愿你永远幸福，永远闪闪发光！** 🎉")

# 🌸🍦🍎❄️ 每写满10条日记根据季节触发庆祝
if len(data) > 0 and len(data) % 10 == 0:
    if season == "spring":
        st.markdown(f"🌸 今天是春天，落樱缤纷，庆祝你写下了第 {len(data)} 条日记！")
        st.balloons()
    elif season == "summer":
        st.markdown(f"🍦 夏天的冰淇淋为你庆祝第 {len(data)} 条日记！清凉又甜蜜～")
        st.image("https://i.imgur.com/O3ZCqQk.png", width=150)
    elif season == "autumn":
        st.markdown(f"🍎 秋天来了，果实累累！这是你第 {len(data)} 条日记，太棒啦！")
        st.image("https://i.imgur.com/Ue3mL6P.png", width=150)
    elif season == "winter":
        st.markdown(f"❄️ 冬天的雪花为你飘落，庆祝你的第 {len(data)} 条日记～")
        try:
            st.snow()
        except Exception:
            st.write("❄️（雪花动画暂不可用）")

# 显示最近的日记
st.markdown("---")
st.subheader("最近的日记")

if data:
    # 取最近10条，带原始索引
    recent_entries = list(enumerate(data))[-10:]
    for i, (idx, entry) in enumerate(reversed(recent_entries)):
        st.write(f"📅 {entry['date']}    评分：{entry['score']}")
        st.write(entry['note'])
        if entry.get("image"):
            try:
                img = Image.open(entry["image"])
                st.image(img, width=300)
            except Exception:
                st.write("（显示图片失败）")
        if st.button(f"🗑️ 删除这条日记（{entry['date']}）", key=f"delete_{i}"):
            del data[idx]
            with open(diary_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.experimental_rerun()
        st.markdown("---")
else:
    st.info("目前没有日记。")
