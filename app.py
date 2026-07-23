import streamlit as st

st.set_page_config(
    page_title="Bot Tín Hiệu Siêu Tốc",
    page_icon="🤖",
    layout="centered"
)

# CSS tùy chỉnh lại toàn bộ giao diện gọn gàng, tinh tế, loại bỏ khung thừa
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.6rem;
            padding-bottom: 0.6rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
        }
        h2 { font-size: 1.15rem !important; margin-bottom: -5px !important; text-align: center; color: #4da6ff; }
        p, label, span { font-size: 0.78rem !important; }
        .stTextInput input { font-size: 1rem !important; padding: 2px !important; text-align: center; }
        div.stButton > button { padding: 4px 8px !important; font-size: 0.82rem !important; font-weight: bold; width: 100%; }
        hr { margin: 6px 0px !important; }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo Session State
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
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

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
        return f"🔥 Bẻ cầu (Gãy {gay})", "red"
    elif an >= 2:
        return f"🚀 Bám cầu (Ăn {an})", "green"
    else:
        return "⏳ Chờ nhịp...", "gray"

def hien_thi_roadmap_html(history, title):
    st.markdown(f"<span style='font-size: 0.7rem; font-weight: bold;'>📊 {title}</span>", unsafe_allow_html=True)
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

    max_col = max([col for col, row in grid.keys()]) if grid else 0
    max_cols_display = max(10, max_col + 1)
    
    html_content = "<div style='overflow-x: auto; background-color: #262626; padding: 2px; border-radius: 4px;'><table style='border-collapse: collapse; margin: auto;'>"
    for r in range(6):
        html_content += "<tr>"
        for c in range(max_cols_display):
            val = grid.get((c, r), None)
            if val is True:
                dot = "<div style='width: 5px; height: 5px; background-color: #00ff00; border-radius: 50%; margin: 1px;'></div>"
            elif val is False:
                dot = "<div style='width: 5px; height: 5px; background-color: #ff4d4d; border-radius: 50%; margin: 1px;'></div>"
            else:
                dot = "<div style='width: 5px; height: 5px; background-color: #333333; border-radius: 50%; margin: 1px;'></div>"
            html_content += f"<td style='border: 1px solid #2a2a2a; width: 9px; height: 9px; text-align: center;'>{dot}</td>"
        html_content += "</tr>"
    html_content += "</table></div>"
    st.markdown(html_content, unsafe_allow_html=True)

# ================= GIAO DIỆN CHÍNH =================
st.markdown("<h2>🤖 Bot Tín Hiệu Siêu Tốc</h2>", unsafe_allow_html=True)

# ----------------- KHU VỰC 1: NHẬP SỐ & XEM KẾT QUẢ -----------------
so_de = st.text_input("Nhập 2 số ĐB Kỳ trước:", max_chars=2, placeholder="VD: 25")

if len(so_de) == 2 and so_de.isdigit():
    d1_pre, d2_pre = tinh_bong_duong(so_de)
    a1_pre, a2_pre = tinh_bong_am(so_de)
    preview_active = True
else:
    d1_pre, d2_pre, a1_pre, a2_pre = "--", "--", "--", "--"
    preview_active = False

col_d, col_a = st.columns(2)
with col_d:
    st.markdown(f"🔵 **B.Dương: {d1_pre}, {d2_pre}**")
    th_d, color_d = phan_tich_chien_thuat(st.session_state.nhip_duong['an'], st.session_state.nhip_duong['gay'])
    st.markdown(f":{color_d}[{th_d}] (Ăn:{st.session_state.nhip_duong['an']}|Gãy:{st.session_state.nhip_duong['gay']})")

with col_a:
    st.markdown(f"🟠 **B.Âm: {a1_pre}, {a2_pre}**")
    th_a, color_a = phan_tich_chien_thuat(st.session_state.nhip_am['an'], st.session_state.nhip_am['gay'])
    st.markdown(f":{color_a}[{th_a}] (Ăn:{st.session_state.nhip_am['an']}|Gãy:{st.session_state.nhip_am['gay']})")

if preview_active:
    st.markdown(f"<div style='font-size: 0.73rem; color: #00ffcc; text-align: center; margin-top: -2px;'>👉 Đã nhận số {so_de}. Tích chọn 'Húp' bên dưới rồi bấm Chốt số!</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------- KHU VỰC 2: CHECKBOX & NÚT CHỐT (DÙNG FORM ĐỂ TỰ RESET) -----------------
with st.form(key=f"chot_form_{st.session_state.form_key}"):
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        win_duong = st.checkbox("Húp Dương 💰")
    with f_col2:
        win_am = st.checkbox("Húp Âm 💰")
        
    submit_btn = st.form_submit_button(label="⚡ CHỐT SỐ & CẬP NHẬT KỲ MỚI", use_container_width=True)

# Xử lý khi bấm nút Chốt
if submit_btn:
    if len(so_de) != 2 or not so_de.isdigit():
        st.warning("Vui lòng nhập đủ 2 chữ số ĐB Kỳ trước ở trên!")
    else:
        d1_pre, d2_pre = tinh_bong_duong(so_de)
        a1_pre, a2_pre = tinh_bong_am(so_de)

        # Cập nhật nhịp bóng dương
        if win_duong:
            st.session_state.nhip_duong['an'] += 1
            st.session_state.nhip_duong['gay'] = 0
            st.session_state.history_duong.append(True)
            status_d_str = "win"
        else:
            st.session_state.nhip_duong['an'] = 0
            st.session_state.nhip_duong['gay'] += 1
            st.session_state.history_duong.append(False)
            status_d_str = "lose"
            
        # Cập nhật nhịp bóng âm
        if win_am:
            st.session_state.nhip_am['an'] += 1
            st.session_state.nhip_am['gay'] = 0
            st.session_state.history_am.append(True)
            status_a_str = "win"
        else:
            st.session_state.nhip_am['an'] = 0
            st.session_state.nhip_am['gay'] += 1
            st.session_state.history_am.append(False)
            status_a_str = "lose"
            
        # Ghi log chuẩn định dạng yêu cầu
        log_entry = f"số {so_de} - b.am:{a1_pre}-{a2_pre} - {status_a_str} - b.duong:{d1_pre}-{d2_pre} - {status_d_str}"
        st.session_state.logs.insert(0, log_entry)
        
        # Đổi key form để reset sạch form (bỏ stick 100%) và rerun lại trang
        st.session_state.form_key += 1
        st.rerun()

# Roadmap thu nhỏ tinh gọn
st.markdown("<hr>", unsafe_allow_html=True)
r_col1, r_col2 = st.columns(2)
with r_col1:
    hien_thi_roadmap_html(st.session_state.history_duong, "ROADMAP BÓNG DƯƠNG")
with r_col2:
    hien_thi_roadmap_html(st.session_state.history_am, "ROADMAP BÓNG ÂM")

# Gấp thếp & Nhật ký hoạt động
st.markdown("<div style='font-size: 0.68rem; color: #ffcc00; text-align: center; margin-top: 2px;'>💡 Gấp thếp: 1k-3k-7k-16k-35k-70k-150k</div>", unsafe_allow_html=True)

st.markdown("<span style='font-size: 0.72rem; font-weight: bold;'>📝 Nhật Ký Hoạt Động</span>", unsafe_allow_html=True)
if st.session_state.logs:
    logs_html = "<br>".join([f"• {log}" for log in st.session_state.logs[:4]])
    st.markdown(f"<div style='font-size: 0.68rem; color: #cccccc; background-color: #1e1e1e; padding: 4px; border-radius: 4px;'>{logs_html}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='font-size: 0.68rem; color: #888888;'>Chưa có lịch sử chốt số.</div>", unsafe_allow_html=True)
