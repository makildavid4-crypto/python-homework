import os
import pickle

#1.查看工作目录，创建文件夹
cwd = os.getcwd()
print(f"当前工作目录：{cwd}")
data_dir = os.path.join(cwd, "exp01_data")
os.makedirs(data_dir, exist_ok=True)
print(f"数据目录路径:{data_dir},目录是否存在:{os.path.exists(data_dir)}")

#2.写入students.txt，再读取
txt_path = os.path.join(data_dir,"students.txt")
content = """name,score
Alice,85
Bob,58
Carol,92
David,76
Eva,60
Frank,89
Grace,abc
Henry,105
Incomplete
"""
#写文件
with open(txt_path,mode="w",encoding="utf-8") as f:
    f.write(content)
#读文件
with open(txt_path,mode="r",encoding="utf-8") as f:
    read_text = f.read()
print("\n读取students.txt全部内容：")
print(read_text)

#3.parse_student函数
def parse_student(line):
    line = line.strip()
    if not line:
        raise ValueError("空行")
    parts = line.split(",")
    if len(parts)!=2:
        raise ValueError(f"字段数量错误，分割得到{len(parts)}个字段")
    name_str, score_str = parts
    name_str = name_str.strip()
    score_str = score_str.strip()
    if len(name_str)==0:
        raise ValueError("姓名为空")
    try:
        score_int = int(score_str)
    except ValueError:
        raise ValueError(f"成绩无法转为整数:{score_str}")
    if not (0 <= score_int <=100):
        raise ValueError(f"成绩超出0‑100范围:{score_int}")
    return {"name":name_str, "score":score_int}

#4.逐行处理，捕获异常
valid_records = []
error_log = []
with open(txt_path,"r",encoding="utf-8") as f:
    lines = f.readlines()
for line_num, one_line in enumerate(lines, start=1):
    if line_num ==1:
        continue #跳过表头
    try:
        rec = parse_student(one_line)
        valid_records.append(rec)
    except ValueError as err:
        error_log.append({"line":line_num,"err":str(err)})

print("\n---有效记录---")
print(valid_records)
print("\n---错误日志(行号+原因)---")
for e in error_log:
    print(e)

#5.统计写入report.txt w模式 和 a追加模式
valid_num = len(valid_records)
invalid_num = len(error_log)
if valid_num>0:
    avg_score = sum(r["score"] for r in valid_records)/valid_num
    pass_cnt = sum(1 for r in valid_records if r["score"]>=60)
    pass_ratio = pass_cnt / valid_num
else:
    avg_score=0
    pass_ratio=0

report_path = os.path.join(data_dir,"report.txt")
#w模式覆盖写
with open(report_path,"w",encoding="utf-8") as fw:
    fw.write(f"有效记录数:{valid_num}\n")
    fw.write(f"无效记录数:{invalid_num}\n")
    fw.write(f"平均分:{avg_score:.2f}\n")
    fw.write(f"及格率:{pass_ratio:.1%}\n")

#a模式追加
with open(report_path,"a",encoding="utf-8") as fa:
    fa.write("=====这是a模式追加新增文字=====\n")

#读取report查看结果
with open(report_path,"r",encoding="utf-8") as fr:
    report_content = fr.read()
print("\nreport.txt(w覆盖+a追加后内容):")
print(report_content)

#6.pickle保存读取
pkl_path = os.path.join(data_dir,"students.pkl")
#dump保存
with open(pkl_path,"wb") as fpw:
    pickle.dump(valid_records, fpw)
#load读取
with open(pkl_path,"rb") as fpr:
    load_data = pickle.load(fpr)

print("\npickle加载后数据与原数据是否相等：", load_data == valid_records)

#8.捕获FileNotFoundError
print("\n---捕获不存在文件异常测试---")
not_exist_file = os.path.join(data_dir,"no_file.txt")
try:
    with open(not_exist_file,"r",encoding="utf-8") as f:
        pass
except FileNotFoundError as e:
    print(f"捕获FileNotFoundError:{e}")
