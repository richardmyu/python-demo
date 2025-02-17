# 导入pdfplumber
import pdfplumber

# 读取pdf文件，保存为pdf实例
pdf =  pdfplumber.open("./waichaung.pdf")

# 访问第二页
print('--',pdf)
first_page = pdf.pages[0]

# 自动读取表格信息，返回列表
table = first_page.extract_table()

print(table)