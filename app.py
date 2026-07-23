import streamlit as st

# Cấu hình giao diện mobile tối ưu thu gọn
st.set_page_config(
    page_title="Bot Tín Hiệu Siêu Tốc",
    page_icon="🤖",
    layout="centered"
)

# CSS tùy chỉnh để ép giao diện siêu gọn, không bị tràn màn hình
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        h2 { font-size: 1.3rem !important; margin-bottom: 0px !important; }
        h3 { font-size: 1rem !important; margin-top: 5px !important; margin-bottom: 2px !important; }
        p, label, span { font-size: 0.85rem !important; }
        .stTextInput input { font-size: 1.1rem !important; padding: 4px !important; text-align: center; }
        div.stButton > button { padding: 4px 10px !important; font-size: 0.9rem !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái phiên làm việc
if 'history_duong' not in st.session_state:
    st.session_state.history_duong = []
if 'history_am' not in st.session_state:
    st.session_state.history_am = []
if 'nhip_duong' not in st.session_state:
    st.session_state.nhip_duong = {'an': 0, 'gay': 0}
if 'nhip_am' not in st.session_state:
    st.session_state.nhip_am = {'an': 0, 'gay': 0}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'last_so' not in st.session_state:
    st.session_state.last_so = "--"

# ================= CÁC HÀM LOGIC =================
def tinh_bong_duong(so_de):
    kq = ""
    for chu_so in so_de:
        kq += str((int(chu_so) + 5) % 10)
    return kq, kq[::-1]

def tinh_bong_am(so_de):
    dict_bong_am = {'0':'7', '7':'0', '1':'4', '4':'1', '2':'9', '9':'2', '3':'6', '6':'3', '5':'8', '8':'5'}
    kq = ""
    for chu_so in so_de:
        kq += dict_bong_am[chu_so]
    return kq, kq[::-1]

def phan_tich_chien_thuat(an, gay):
    if gay >= 3:
        return f"🔥 Bẻ cầu (Gãy {gay}, gấp thếp!)", "red"
    elif an >= 2:
        return f"🚀 Bám cầu (Ăn {an} tay!)", "green"
    else:
        return "⏳ Chờ nhịp rõ...", "gray"

# Hàm tạo ma trận lưới cho Roadmap thu gọn
def tao_luoi_roadmap(history):
    max_rows = 6
    grid = {}
    if history:
        current_col = 0
        current_row = 0
        grid[(current_col, current_row)] = history[0]
        
        for i in range(1, len(history)):
            prev_res = history[i-1]
            curr_res = history[i]
            
            if curr_res == prev_res:
                next_row = current_row + 1
                next_col = current_col
                
                if next_row >= max_rows or (next_col, next_row) in grid:
                    next_row = current_row
                    next_col = current_col + 1
                    
                current_row = next_row
                current_col = next_col
            else:
                next_col = 0
                while (next_col, 0) in grid:
                    next_col += 1
                current_row = 0
                current_col = next_col
                
            grid[(current_col, current_row)] = curr_res
    return grid

def hien_thi_roadmap_html(history, title, color_theme):
    st.markdown(f"<span style='font-size: 0.8rem; font-weight: bold;'>📊 {title}</span>", unsafe_allow_html=True)
    grid = tao_luoi_roadmap(history)
    
    max_col = max([col for col, row in grid.keys()]) if grid else 0
    max_cols_display = max(12, max_col + 1)
    
    html_content = "<div style='overflow-x: auto; background-color: #2d2d2d; padding: 4px; border-radius: 6px;'><table style='border-collapse: collapse; margin: auto;'>"
    for r in range(6):
        html_content += "<tr>"
        for c in range(max_cols_display):
            val = grid.get((c, r), None)
            if val is True:
                dot = "<div style='width: 10px; height: 10px; background-color: #00ff00; border-radius: 50%; margin: 1px;'></div>"
            elif val is False:
                dot = "<div style='width: 10px; height: 10px; background-color: #ff4d4d; border-radius: 50%; margin: 1px;'></div>"
            else:
                dot = "<div style='width: 10px; height: 10px; background-color: #3d3d3d; border-radius: 50%; margin: 1px;'></div>"
            html_content += f"<td style='border: 1px solid #3d3d3d; width: 16px; height: 16px; text-align: center;'>{dot}</td>"
        html_content += "</tr>"
    html_content += "</table></div>"
    st.markdown(html_content, unsafe_allow_html=True)

# ================= GIAO DIỆN CHÍNH SIÊU GỌN =================
st.markdown("<h2 style='text-align: center; color: #4da6ff;'>🤖 Bot Tín Hiệu Siêu Tốc</h2>", unsafe_allow_html=True)

# Bố trí nhập liệu và nút bấm chung 1 hàng ngang siêu gọn
col_input, col_b1, col_b2, col_btn = st.columns([1.2, 1.2, 1.2, 1.5])
with col_input:
    so_de = st.text_input("ĐB Kỳ trước", max_chars=2, placeholder="VD: 14")
with col_b1:
    win_duong = st.checkbox("Húp Dương 💰")
with col_b2:
    win_am = st.checkbox("Húp Âm 💰")
with col_btn:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # Căn chỉnh lề dọc nút bấm
    submit_btn = st.button("⚡ CHỐT SỐ", use_container_width=True)

if submit_btn:
    if len(so_de) != 2 or not so_de.isdigit():
        st.warning("Nhập đúng 2 số!")
    else:
        st.session_state.last_so = so_de
        if win_duong:
            st.session_state.nhip_duong['an'] += 1
            st.session_state.nhip_duong['gay'] = 0
            st.session_state.history_duong.append(True)
        else:
            st.session_state.nhip_duong['an'] = 0
            st.session_state.nhip_duong['gay'] += 1
            st.session_state.history_duong.append(False)
            
        if win_am:
            st.session_state.nhip_am['an'] += 1
            st.session_state.nhip_am['gay'] = 0
            st.session_state.history_am.append(True)
        else:
            st.session_state.nhip_am['an'] = 0
            st.session_state.nhip_am['gay'] += 1
            st.session_state.history_am.append(False)
            
        status_d = "WIN" if win_duong else "LOSE"
        status_a = "WIN" if win_am else "LOSE"
        st.session_state.logs.insert(0, f"Kỳ {so_de} ➔ D:{status_d} | A:{status_a}")

# Hiển thị kết quả chia 2 cột trái/phải cho gọn màn hình
if len(so_de) == 2 and so_de.isdigit():
    d1, d2 = tinh_bong_duong(so_de)
    a1, a2 = tinh_bong_am(so_de)
    
    st.markdown("<hr style='margin: 5px 0px;'>", unsafe_allow_html=True)
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown(f"### 🔵 B.Dương: `{d1}`, `{d2}`")
        th_d, color_d = phan_tich_chien_thuat(st.session_state.nhip_duong['an'], st.session_state.nhip_duong['gay'])
        st.markdown(f":{color_d}[{th_d}] (Ăn:{st.session_state.nhip_duong['an']}|Gãy:{st.session_state.nhip_duong['gay']})")
        st.code(f"{d1},{d2}")

    with c_right:
        st.markdown(f"### 🟠 B.Âm: `{a1}`, `{a2}`")
        th_a, color_a = phan_tich_chien_thuat(st.session_state.nhip_am['an'], st.session_state.nhip_am['gay'])
        st.markdown(f":{color_a}[{th_a}] (Ăn:{st.session_state.nhip_am['an']}|Gãy:{st.session_state.nhip_am['gay']})")
        st.code(f"{a1},{a2}")

# Roadmap thu gọn giao diện
st.markdown("<hr style='margin: 5px 0px;'>", unsafe_allow_html=True)
r_col1, r_col2 = st.columns(2)
with r_col1:
    hien_thi_roadmap_html(st.session_state.history_duong, "ROADMAP BÓNG DƯƠNG", "#4da6ff")
with r_col2:
    hien_thi_roadmap_html(st.session_state.history_am, "ROADMAP BÓNG ÂM", "#ff9900")

# Lộ trình gấp thếp siêu ngắn gọn phía dưới chân trang
st.markdown("<div style='font-size: 0.75rem; color: #ffcc00; text-align: center; margin-top: 5px;'>💡 Gấp thếp: 1k - 3k - 7k - 16k - 35k - 70k - 150k</div>", unsafe_allow_html=True)
