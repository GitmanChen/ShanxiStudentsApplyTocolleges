import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import mysql.connector

def get_conn(db_name):
    conn = mysql.connector.connect(user='root', password='123065', host='localhost', database=db_name)
    return conn
conn1 = get_conn('2022scorerank')
cursor1 = conn1.cursor()
conn2 = get_conn('2022scoreline')
cursor2 = conn2.cursor()
# 定义窗口的函数
def create_window():
    win = tk.Tk()
    win.title("报名系统")
    win.configure(bg="white")
    win.geometry('920x760')
    
    # 定义输入栏和选择框
    input_label = tk.Label(win, text="请输入你的省排名", font=("Arial", 18))
    input_label.pack(pady=10)
    input_text = tk.Entry(win, width=30, font=("Arial", 18))
    input_text.pack(pady=10)
    select_label = tk.Label(win, text="请选择文理科", font=("Arial", 18))
    select_label.pack(pady=10)
    select_box = tk.Listbox(win, font=("Arial", 18), height=2)
    select_box.insert(0, "文科")
    select_box.insert(1, "理科")
    select_box.pack(pady=10)
    choose_label = tk.Label(win, text="你可以选择的学校有", font=("Arial", 18))
    choose_label.pack(pady=10)

    # 定义输出文本框函数
    scr = scrolledtext.ScrolledText(win,width=50,height=10,font=("宋体", 15))
    scr.pack(pady=10)

    # 定义重置按钮事件和添加重置按钮
    def reset():
        input_text.delete(0,tk.END)
        select_box.selection_clear(0,END)
        scr.delete(1.0,'end')
    reset_btn = tk.Button(win, text="重置",font=("Arial", 18),command=reset)
    reset_btn.pack()
    # 定义输入栏和选择框的事件
    def on_click():
        global rank
        rank= float(input_text.get())

    def on_select(event):
        global rank
        rank= float(input_text.get())
        subject = select_box.get(select_box.curselection())
        
    # 从scorerank数据库arts/sciences表查询  
        def get_rank_score(subject, rank):
            if subject == '文科':
                db_name = 'arts'
            elif subject=='理科':
                db_name = 'sciences'
            print('22222')
            rank_equal="SELECT 分数 AS num2 FROM 2022scorerank.%s WHERE 累计人数 = CAST(%s AS SIGNED) ORDER BY 累计人数 ASC   LIMIT 1"
            rank_exceeds="SELECT 分数 AS num2 FROM 2022scorerank.%s WHERE 累计人数 > CAST(%s AS SIGNED) "
            miniscore = "SELECT 院校名称 FROM 2022scoreline.%s WHERE 最低分 BETWEEN %s - 10 AND %s + 3"
            cursor1.execute(rank_equal % (db_name, rank,))
            result=cursor1.fetchone()

            if result:
                print(result)
            else:
                print(111)
                cursor1.execute(rank_exceeds %(db_name, rank,))
                results=cursor1.fetchall()
                result=list(results)[0]
                print(result)
            #tuple类型
            result=float(result[0])
            print(type(result))

            cursor2.execute(miniscore %(db_name, result, result))
            results = cursor2.fetchall()
            for row in results:
                scr.insert(END, ' '.join(row) + ' ')
        get_rank_score(subject, rank)
        # 绑定按钮点击事件和选择框选项事件
    input_text.bind("<Return>", lambda event: on_click())
    select_box.bind("<<ListboxSelect>>", on_select)

    notice_label = tk.Label(win, text="1.数据库容量有限，仅支持本科以上检索；  2.结果仅供参考", font=("Arial", 9))
    notice_label.pack(side=RIGHT,padx=80)
   # 运行窗口
    win.mainloop()

# 运行窗口的函数
create_window()
#关闭数据库连接
cursor1.close()
cursor2.close()
conn1.close()
conn2.close()