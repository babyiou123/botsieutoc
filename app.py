import streamlit as st

st.set_page_config(
    page_title="Bot Tín Hiệu Siêu Tốc",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 0.8rem;
            padding-bottom: 0.8rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
        h2 { font-size: 1.2rem !important; margin-bottom: 0px !important; text-align: center; color: #4da6ff; }
        p, label, span { font-size: 0.8rem !important; }
        .stTextInput input { font-size: 1rem !important; padding: 2px !important; text-align: center; }
        div.stButton > button { padding: 4px 8px !important; font-size: 0.85rem !important; font-weight: bold; }
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
    st.markdown(f"<span style='font-size: 0.75rem; font-weight: bold;'>📊 {title}</span>", unsafe_allow_html=True)
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
    
    html_content = "<div style='overflow-x: auto; background-color: #2d2d2d; padding: 2px; border-radius: 4px;'><table style='border-collapse: collapse; margin: auto;'>"
    for r in range(6):
        html_content += "<tr>"
        for c in range(max_cols_display):
            val = grid.get((c, r), None)
            if val is True:
                dot = "<div style='width: 6px; height: 6px; background-color: #00ff00; border-radius: 50%; margin: 1px;'></div>"
            elif val is False:
                dot = "<div style='width: 6px; height: 6px; background-color: #ff4d4d; border-radius: 50%; margin: 1px;'></div>"
            else:
                dot = "<div style='width: 6px; height: 6px; background-color: #3d3d3d; border-radius: 50%; margin: 1px;'></div>"
            html_content += f"<td style='border: 1px solid #333333; width: 10px; height: 10px; text-align: center;'>{dot}</td>"
        html_content += "</tr>"
    html_content += "</table></div>"
    st.markdown(html_content, unsafe_allow_html=True)

# ================= GIAO DIỆN CHÍNH =================
st.markdown("<h2>🤖 Bot Tín Hiệu Siêu Tốc</h2>", unsafe_allow_html=True)

# Ô nhập số ĐB Kỳ trước (không dùng key cố định để tự động xóa sạch khi reset)
so_de = st.text_input("Nhập 2 số ĐB Kỳ trước:", max_chars=2, placeholder="VD: 23")

# Tính toán giá trị dự kiến
if len(so_de) == 2 and so_de.isdigit():
    d1_pre, d2_pre = tinh_bong_duong(so_de)
    a1_pre, a2_pre = tinh_bong_am(so_de)
    preview_mode = True
else:
    d1_pre, d2_pre, a1_pre, a2_pre = "--", "--", "--", "--"
    preview_mode = False

# Hiển thị Bóng Dương, Bóng Âm và nút Húp chung 1 hàng (Không truyền value cố định, dùng key độc lập)
col_d, col_a = st.columns(2)

with col_d:
    st.markdown(f"🔵 **B.Dương: {d1_pre}, {d2_pre}**")
    th_d, color_d = phan_tich_chien_thuat(st.session_state.nhip_duong['an'], st.session_state.nhip_duong['gay'])
    st.markdown(f":{color_d}[{th_d}] (Ăn:{st.session_state.nhip_duong['an']}|Gãy:{st.session_state.nhip_duong['gay']})")
    win_duong = st.checkbox("Húp Dương 💰", key="widget_chk_duong")

with col_a:
    st.markdown(f"🟠 **B.Âm: {a1_pre}, {a2_pre}**")
    th_a, color_a = phan_tich_chien_thuat(st.session_state.nhip_am['an'], st.session_state.nhip_am['gay'])
    st.markdown(f":{color_a}[{th_a}] (Ăn:{st.session_state.nhip_am['an']}|Gãy:{st.session_state.nhip_am['gay']})")
    win_am = st.checkbox("Húp Âm 💰", key="widget_chk_am")

if preview_mode:
    st.markdown(f"<div style='font-size: 0.75rem; color: #00ffcc; text-align: center;'>👉 Đã nhận số {so_de}. Tích chọn 'Húp' rồi bấm nút Chốt số bên dưới để ghi nhận!</div>", unsafe_allow_html=True)

# Nút Chốt số chính thức
if st.button("⚡ CHỐT SỐ & CẬP NHẬT KỲ MỚI", use_container_width=True):
    if len(so_de) != 2 or not so_de.isdigit():
        st.warning("Vui lòng nhập đúng 2 chữ số!")
    else:
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
        
        # Xóa sạch trạng thái widget checkbox trong session_state để bỏ stick hoàn toàn
        for key in ['widget_chk_duong', 'widget_chk_am']:
            if key in st.session_state:
                del st.session_state[key]
                
        st.rerun()

# Roadmap thu nhỏ
st.markdown("<hr style='margin: 3px 0px;'>", unsafe_allow_html=True)
r_col1, r_col2 = st.columns(2)
with r_col1:
    hien_thi_roadmap_html(st.session_state.history_duong, "ROADMAP BÓNG DƯƠNG")
with r_col2:
    hien_thi_roadmap_html(st.session_state.history_am, "ROADMAP BÓNG ÂM")

# Gấp thếp & Nhật ký hoạt động
st.markdown("<div style='font-size: 0.7rem; color: #ffcc00; text-align: center; margin-top: 3px;'>💡 Gấp thếp: 1k-3k-7k-16k-35k-70k-150k</div>", unsafe_allow_html=True)

st.markdown("<span style='font-size: 0.75rem; font-weight: bold;'>📝 Nhật Ký Hoạt Động</span>", unsafe_allow_html=True)
if st.session_state.logs:
    logs_html = "<br>".join([f"• {log}" for log in st.session_state.logs[:4]])
    st.markdown(f"<div style='font-size: 0.7rem; color: #cccccc; background-color: #222222; padding: 5px; border-radius: 4px;'>{logs_html}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='font-size: 0.7rem; color: #888888;'>Chưa có lịch sử chốt số.</div>", unsafe_allow_html=True)
