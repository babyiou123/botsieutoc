import streamlit as st

# Cấu hình trang web dạng mobile-friendly
st.set_page_config(
    page_title="Bot Tín Hiệu Siêu Tốc",
    page_icon="🤖",
    layout="centered"
)

# Khởi tạo trạng thái phiên làm việc (Session State) để lưu dữ liệu khi chuyển trang/tương tác
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
        return f"🔥 VÀO LỆNH: Canh bẻ cầu (Gãy {gay} tay, gấp thếp!)", "red"
    elif an >= 2:
        return f"🚀 BÁM CẦU: Đu theo trend (Ăn thông {an} tay!)", "green"
    else:
        return "⏳ NGỒI NGOÀI: Cầu đang nhiễu, chờ nhịp rõ.", "gray"

# ================= GIAO DIỆN WEB =================
st.markdown("<h2 style='text-align: center; color: #4da6ff;'>🤖 Bot Tín Hiệu Siêu Tốc</h2>", unsafe_allow_html=True)

# Phần nhập liệu
so_de = st.text_input("Nhập 2 số giải đặc biệt kỳ trước:", max_chars=2, placeholder="VD: 88")

col1, col2 = st.columns(2)
win_duong = col1.checkbox("Húp Bóng Dương 💰")
win_am = col2.checkbox("Húp Bóng Âm 💰")

if st.button("⚡ CHỐT SỐ & CẬP NHẬT KỲ MỚI", use_container_width=True):
    if len(so_de) != 2 or not so_de.isdigit():
        st.warning("Vui lòng nhập đúng 2 chữ số!")
    else:
        st.session_state.last_so = so_de
        
        # Cập nhật lịch sử nhịp
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
            
        # Ghi log
        status_d = "WIN" if win_duong else "LOSE"
        status_a = "WIN" if win_am else "LOSE"
        st.session_state.logs.insert(0, f"Kỳ {so_de} ➔ B.Dương: {status_d} | B.Âm: {status_a}")

# Hiển thị kết quả tính toán hiện tại
if len(so_de) == 2 and so_de.isdigit():
    d1, d2 = tinh_bong_duong(so_de)
    a1, a2 = tinh_bong_am(so_de)
    
    st.markdown("---")
    st.markdown(f"### 🔵 Bóng Dương: `{d1}`, `{d2}`")
    th_d, color_d = phan_tich_chien_thuat(st.session_state.nhip_duong['an'], st.session_state.nhip_duong['gay'])
    st.markdown(f":{color_d}[{th_d}] (Ăn: {st.session_state.nhip_duong['an']} | Gãy: {st.session_state.nhip_duong['gay']})")
    st.code(f"{d1},{d2}")

    st.markdown(f"### 🟠 Bóng Âm: `{a1}`, `{a2}`")
    th_a, color_a = phan_tich_chien_thuat(st.session_state.nhip_am['an'], st.session_state.nhip_am['gay'])
    st.markdown(f":{color_a}[{th_a}] (Ăn: {st.session_state.nhip_am['an']} | Gãy: {st.session_state.nhip_am['gay']})")
    st.code(f"{a1},{a2}")

# Gợi ý gấp thếp
st.markdown("---")
st.info("💡 **Lộ trình gấp thếp gợi ý:** 1k - 3k - 7k - 16k - 35k - 70k - 150k")

# Hiển thị Nhật ký
st.markdown("### 📝 Nhật Ký Hoạt Động")
if st.session_state.logs:
    for log in st.session_state.logs[:10]: # Hiển thị 10 log gần nhất
        st.text(log)
else:
    st.text("Chưa có lịch sử hoạt động.")
