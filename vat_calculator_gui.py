import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to the resource, used for accessing files when packaged by PyInstaller. """
    if hasattr(sys, '_MEIPASS'):
        # If the program is being run in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def judge_isnum(input_str):
    if input_str[0] == '-':
        input_str = input_str[1:]
    input_str = re.sub(r'\.', '', input_str)
    return input_str.isdigit()

def get_c(c):
    return "零壹贰叁肆伍陆柒捌玖"[c]

def judge_zero(num):
    return all(n == '0' for n in num)

def get_pre(input_str):
    return input_str.split('.')[0]

def get_post(input_str):
    parts = input_str.split('.')
    return parts[1] if len(parts) > 1 else ''

def get_four(num):
    num = int(num)
    if num == 0:
        return ""
    elif num < 10:
        return get_c(num)
    elif num < 100:
        if num % 10 == 0:
            return get_four(num // 10) + "拾"
        else:
            return get_four(num // 10) + "拾" + get_four(num % 10)
    elif num < 1000:
        if num % 100 == 0:
            return get_four(num // 100) + "佰"
        elif num % 100 < 10:
            return get_four(num // 100) + "佰零" + get_four(num % 100)
        else:
            return get_four(num // 100) + "佰" + get_four(num % 100)
    elif num < 10000:
        if num % 1000 == 0:
            return get_four(num // 1000) + "仟"
        elif num % 1000 < 100:
            return get_four(num // 1000) + "仟零" + get_four(num % 1000)
        else:
            return get_four(num // 1000) + "仟" + get_four(num % 1000)

def get_eight(num):
    num = num.lstrip('0')
    if len(num) <= 4:
        return get_four(int(num))
    str1 = num[:-4]
    str2 = num[-4:]
    if str2[0] == '0' and not judge_zero(str2):
        return get_four(int(str1)) + "万零" + get_four(int(str2))
    elif judge_zero(str2):
        return get_four(int(str1)) + "万"
    else:
        return get_four(int(str1)) + "万" + get_four(int(str2))

def get_16(num):
    num = num.lstrip('0')
    if len(num) <= 8:
        return get_eight(num)
    str1 = num[:-8]
    str2 = num[-8:]
    if str2[0] == '0' and not judge_zero(str2):
        return get_eight(str1) + "亿零" + get_eight(str2)
    elif judge_zero(str2):
        return get_eight(str1) + "亿"
    else:
        return get_eight(str1) + "亿" + get_eight(str2)

def get_out_16(num):
    num = num.lstrip('0')
    if len(num) <= 16:
        return get_16(num)
    while len(num) > 16:
        str1 = num[:-8]
        str2 = num[-8:]
        if str2[0] == '0' and not judge_zero(str2):
            return get_out_16(str1) + "亿零" + get_eight(str2)
        elif judge_zero(str2):
            return get_out_16(str1) + "亿"
        else:
            return get_out_16(str1) + "亿" + get_eight(str2)

def get_pre_c(pre):
    if len(pre) <= 4:
        return get_four(int(pre))
    elif len(pre) <= 8:
        return get_eight(pre)
    elif len(pre) <= 16:
        return get_16(pre)
    else:
        return get_out_16(pre)

def get_post_c(post, pre_len):
    if not post:
        return ""
    elif len(post) == 1:
        num = int(post)
        return "" if num == 0 else get_c(num) + "角"
    else:
        two = post[:2]
        num = int(two)
        if num == 0:
            return ""
        elif num < 10 and pre_len != 0:
            return "零" + get_c(num) + "分"
        elif num < 10 and pre_len == 0:
            return get_c(num) + "分"
        else:
            jiao = num // 10
            fen = num % 10
            return get_c(jiao) + "角" + (get_c(fen) + "分" if fen else "")

def number2word(input_str):
    if not judge_isnum(input_str):
        raise ValueError("输入不合法")
    input_str = input_str.lstrip('0')
    pre = get_pre(input_str)
    post = get_post(input_str)
    out1 = get_pre_c(pre)
    out2 = get_post_c(post, len(pre))
    if not out1 and not out2:
        return "人民币零元整"
    elif not out1:
        return "人民币" + out2
    elif not out2:
        return "人民币" + out1 + "元整"
    else:
        return "人民币" + out1 + "元" + out2

def calculate_vat(amount, include_vat, vat_rate):
    amount = round(amount, 2)
    if include_vat.lower() == '是':
        net_amount = round(amount / (1 + vat_rate), 2)
        vat_amount = round(amount - net_amount, 2)
    else:
        net_amount = amount
        vat_amount = round(amount * vat_rate, 2)
    total_amount = round(net_amount + vat_amount, 2)
    
    return {
        "增值税额": vat_amount,
        "净额（不含增值税）": net_amount,
        "总金额（含增值税）": total_amount,
        "增值税额（大写）": number2word(f"{vat_amount:.2f}"),
        "净额（大写）": number2word(f"{net_amount:.2f}"),
        "总金额（大写）": number2word(f"{total_amount:.2f}")
    }

def calculate_and_show():
    try:
        amount_str = amount_entry.get()
        vat_rate_str = vat_rate_entry.get()
        
        amount = float(amount_str)
        vat_rate = float(vat_rate_str)
        
        include_vat = include_vat_var.get()
        result = calculate_vat(amount, include_vat, vat_rate)
        result_text = (
            f"增值税额：{result['增值税额']:.2f}\n"
            f"净额（不含增值税）：{result['净额（不含增值税）']:.2f}\n"
            f"总金额（含增值税）：{result['总金额（含增值税）']:.2f}\n"
            f"增值税额（大写）：{result['增值税额（大写）']}\n"
            f"净额（大写）：{result['净额（大写）']}\n"
            f"总金额（大写）：{result['总金额（大写）']}"
        )
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.INSERT, result_text)
        results_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

# Setup GUI
root = tk.Tk()
root.title("增值税计算器")

# 加载图标，使用 resource_path 确保路径正确
icon_path = resource_path('calculate.ico')
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Error loading icon: {e}")

tk.Label(root, text="请输入金额：").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()
amount_entry.insert(0, "20240628")  # 设置默认值为20240628

tk.Label(root, text="金额中包含增值税（是/否）：").pack()
include_vat_var = tk.StringVar(value="是")
tk.Radiobutton(root, text="是", variable=include_vat_var, value="是").pack()
tk.Radiobutton(root, text="否", variable=include_vat_var, value="否").pack()

tk.Label(root, text="请输入税率（如0.06表示6%）：").pack()
vat_rate_entry = tk.Entry(root)
vat_rate_entry.pack()
vat_rate_entry.insert(0, "0.06")  # 设置默认值为0.06

calculate_button = tk.Button(root, text="计算", command=calculate_and_show)
calculate_button.pack()

results_text = scrolledtext.ScrolledText(root, state='disabled', height=10)
results_text.pack()

root.mainloop()
