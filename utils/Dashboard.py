import streamlit as st
from modules import *
from modules import *
from pathlib import Path
import requests
from streamlit.components.v1 import html

# my_js = """
#     let intervalId;
    
#     function hideElements() {
#         const elements = document.querySelectorAll('[data-testid="stAppViewBlockContainer"] .e1f1d6gn1 > .e1f1d6gn2 [data-testid="stAlert"]');
#         console.log(document.querySelectorAll('[data-testid="stAppViewBlockContainer"] .e1f1d6gn1 > .e1f1d6gn2 [data-testid="stAlert"]'))
#         elements.forEach(element => {
#             element.style.display = 'none';
#         });
#     }

#     intervalId = setInterval(hideElements, 1000);
#     setTimeout(() => {
#         clearInterval(intervalId);
#         console.log("Interval stopped");
#     }, 5000);
# """
# my_html = f"<script>{my_js}</script>"

API_URL = "https://apiquanlydaotao.ptit.edu.vn/api/truong-thpt/"
TINH_TP_URL = API_URL + "tinh-tp"
QUAN_HUYEN_URL = API_URL + "quan-huyen/tinh-tp/"
key_mapping = {
    "diaChiTruong": "Địa chỉ trường",
    "khuVuc": "Khu vực",
    "maQH": "Mã Quận Huyện",
    "maTinhTP": "Mã Tỉnh Thành Phố",
    "maTruong": "Mã Trường",
    "tenQH": "Tên Quận",
    "tenTinhTP": "Tên Tỉnh Thành Phố",
    "tenTruong": "Tên Trường",
    "truongChuyen": "Trường Chuyên"
}
def get_data_from_api(url):
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcklkIjoiNjYzMjI5ZjBmYmI5OWEwNDdlZjVhMmIyIiwiYXV0aG9yaXphdGlvblZlcnNpb24iOjEsInBsYXRmb3JtIjoiV2ViIn0sImp0aSI6Ijc3MGU5ZDE3LWZmMjYtNDhlOC04OTFkLWM1ODBkODY4NmJkYSIsImlhdCI6MTcxNDY2ODYwOSwiZXhwIjoxNzE0NzU1MDA5fQ.kdH2UeqOtIocY66By7uSoXnHI3BePawK_DpGpFkqX7c'}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def selectbox_with_data(label, data_dict):
    selected_item = st.selectbox(label, index=None, options=list(data_dict.keys()))
    st.write('Mã:', data_dict.get(selected_item))
    return selected_item

def get_truong_info(truong_dict, search_key, search_values):
    matching_truongs = []
    for truong_info in truong_dict.get('data', []):
        if truong_info.get(search_key) in search_values:
            matching_truongs.append(truong_info)
    return matching_truongs

def sidebarConfig(sidebar):
    with sidebar:
        pass

def customsGroup(current_dir):
    css__custom = f'{current_dir}/assets/styles/custom.css'
    Custom_CSS(st, css__custom)
    Custom_Code(st, """
            <div class="main__title"> 
                <h3> Dashboard <h3>
            <div/>        
        """)
    Custom_JS(st, f'{current_dir}/assets/js/remove.js')
    col1, col2, col3 = st.columns(3)
    
    tinh_tp_data = get_data_from_api(TINH_TP_URL)
    tinh_tp_dict = {item['tenTinhTP']: item['maTinh'] for item in tinh_tp_data.get('data', [])}
    with col1:
        selected_tinh_tp = selectbox_with_data("Chọn tỉnh/TP", tinh_tp_dict)
    if (selected_tinh_tp is not None):
        quan_huyen_data = get_data_from_api(QUAN_HUYEN_URL + tinh_tp_dict.get(selected_tinh_tp, ""))
        quan_huyen_dict = {item['tenQH']: item['maQH'] for item in quan_huyen_data.get('data', [])}
        with col2:
            selected_quan_huyen = selectbox_with_data("Chọn quận/huyện", quan_huyen_dict)
        if (selected_quan_huyen is not None):
            truong_thpt_data = get_data_from_api(f"{API_URL}maTinhTP/{tinh_tp_dict.get(selected_tinh_tp)}/maQuanHuyen/{quan_huyen_dict.get(selected_quan_huyen)}")
            truong_thpt_dict = {item['tenTruong']: item['maTruong'] for item in truong_thpt_data.get('data', [])}
            with col3:
                selected_truong_thpt = selectbox_with_data("Tên trường", truong_thpt_dict)
            if (selected_truong_thpt is not None): 
                st.subheader("Thông tin về trường THPT mà bạn theo học")
                result_by_ma_truong = get_truong_info(truong_thpt_data, 'maTruong', truong_thpt_dict.get(selected_truong_thpt))
                result_by_ma_truong = [{new_key: item.pop(old_key, None) for old_key, new_key in key_mapping.items()} for item in result_by_ma_truong]
                st.write(result_by_ma_truong[0])

    
    

def Dashboard(sidebar):
    current_dir = Path(".")
    sidebarConfig(sidebar)
    customsGroup(current_dir)