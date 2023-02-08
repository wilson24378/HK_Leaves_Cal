# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 09:44:25 2022

@author: wilso
"""

import streamlit as st

###### for calculation of annual leave #####
import datetime
from datetime import date, timedelta
import pytz


##### Define special dates #####
holiday = [
            date(2023,1,2), #一月一日翌日
            date(2023,1,23), #農曆年初二
            date(2023,1,24), #農曆年初三
            date(2023,1,25), #農曆年初四
            date(2023,4,5), #清明節
            date(2023,4,7), #耶穌受難節
            date(2023,4,8), #耶穌受難節翌日
            date(2023,4,10), #復活節星期一
            date(2023,5,1), #勞動節
            date(2023,5,26), #佛誕
            date(2023,6,22), #端午節
            date(2023,7,1), #香港特別行政區成立紀念日
            date(2023,9,30), #中秋節翌日
            date(2023,10,2), #國慶日翌日
            date(2023,10,23), #重陽節
            date(2023,12,25), #聖誕節
            date(2023,12,26), #聖誕節後第一個周日

                ]


##### Config Streamlit #####
st.set_page_config(page_title='Annual Leave Calculation',
                   layout="wide",
                    initial_sidebar_state="expanded",
                     )

hide_menu_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_menu_style, unsafe_allow_html=True)


##### Make back green white font heading #####
bgcolor = 'green'
fontcolor = 'white'
html_temp = f"""
		<div style="background-color:{bgcolor};padding:10px">
		<h1 style="color:{fontcolor};text-align:center;"> 2023 香 港 請 假 計 算 器 </h1>
		</div>
		"""
st.markdown(html_temp,unsafe_allow_html=True)
st.markdown("")
st.markdown("")
st.markdown("")

##### 內容 #####
header = f'<p style="font-family:sans-serif; color:#00FF00; font-size: 22px;">假期計算'
st.markdown(header, unsafe_allow_html=True)


column_b1, column_b2 = st.columns([1,1])

start_date = column_b1.date_input(
    "開始日",
    datetime.date(2023, 1, 1))

end_date = column_b2.date_input(
    "結束日",
    start_date)

# Calculate number of dates in period, excluding special dates
dates_in_period = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)]
holiday_dates = [d for d in holiday if d in dates_in_period]

# Exclude all Saturdays and Sundays in Hong Kong Time
hk_tz = pytz.timezone("Asia/Hong_Kong")
for d in dates_in_period:
    hk_date = hk_tz.localize(datetime.datetime.combine(d, datetime.time.min))
    if (hk_date.weekday() == 5 or hk_date.weekday() == 6):
        holiday_dates.append(hk_date)

holiday_dates = [d.strftime("%Y-%m-%d") for d in holiday_dates]
holiday_dates = list(dict.fromkeys(holiday_dates)) # drop duplicate in 
holiday_dates.sort()

actual_dates_take_leave = len(dates_in_period) - len(holiday_dates)


st.subheader(f'假期由 {start_date} 至 {end_date} ------ 總日數: {len(dates_in_period)}日')
if holiday_dates:
    st.subheader(f'包括{len(holiday_dates)}日公眾假期 / 星期六或日: \n{holiday_dates}')
st.subheader(f'實際需請假日期為: {actual_dates_take_leave}日')

