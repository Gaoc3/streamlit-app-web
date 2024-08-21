 
# # Define the decorator
# import asyncio
# from functools import wraps
# import posixpath
# import requests
# #_________________________________________________________________________________________________
# def auto_async_run(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if asyncio.iscoroutinefunction(func):
#             return asyncio.run(func(*args, **kwargs))
#         else:
#             return func(*args, **kwargs)
#     return wrapper

# # Example of an async function
# @auto_async_run
# async def async_function():
#     await asyncio.sleep(1)
#     print("Async function executed")

# # Example of a normal function
# @auto_async_run
# def normal_function():
#     print("Normal function executed")

# # Test the functions
# async_function()
# normal_function()



# Initialize theme button state
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.mention import mention
import json
# دالة لتحميل الثيم الأخير المخزن
THEME_FILE = "theme.json"

# دالة لحفظ الثيم في ملف JSON
def save_theme(theme_name):
    with open(THEME_FILE, "w") as file:
        json.dump({"theme": theme_name}, file,indent=4)
        

def load_theme():
    try:
        with open(THEME_FILE, "r") as file:
            data = json.load(file)
            return data['theme']  
    except FileNotFoundError:
        return None
# دالة لتحميل CSS
@st.cache_data
def load_css(file_name="style.css"):
    with open(file_name) as f:
        css = f.read()
    return css

css = load_css()
ms = st.session_state

# التحقق من وجود "themes" في session state
if "themes" not in ms:

    last_theme = load_theme() if load_theme is not None else 'light'
    ms.themes = {
        "current_theme": last_theme,
        "refreshed": True,
        "light": {
                "theme.base": "light",
                "theme.backgroundColor": "#E0E0E0",
                "theme.primaryColor": "#ec1919",
                "theme.secondaryBackgroundColor": "#1637f1",
                "theme.textColor": "#0a1464",
                  
                 },
        "dark":  {
                "theme.base": "dark",
                "theme.backgroundColor": "#141444",
                "theme.primaryColor": "#000065",
                "theme.secondaryBackgroundColor": "#82E1D7",
                "theme.textColor": "#f2f2f2",
                  
                 },
    }

# تطبيق الثيم المخزن عند بدء التطبيق
def apply_theme():
    current_theme_dict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in current_theme_dict.items():
        st._config.set_option(vkey, vval)

apply_theme()  # تطبيق الثيم عند بدء التطبيق



def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
    else:
        ms.themes["current_theme"] = "dark"
        
    apply_theme()
    
    save_theme(ms.themes["current_theme"])
    
    ms.themes["refreshed"] = False
with stylable_container(
        key="button",
        css_styles=load_css(),
    ):
    st.button(label='', on_click=ChangeTheme, type="primary")
st.json(ms.themes)
if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()


with open('element.html','r')as ht:
    components.html(ht.read())
