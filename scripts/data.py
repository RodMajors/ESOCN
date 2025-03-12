import pandas as pd
from sqlalchemy import create_engine
import time
from urllib.parse import quote_plus
import re  # 导入正则表达式模块

# 记录开始时间
start_time = time.time()

en_file_path = 'E:/projects/ESOCN/public/en.lang.csv'
zh_file_path = 'E:/projects/ESOCN/public/zh.lang.csv'

# 读取 CSV 文件
df_en = pd.read_csv(en_file_path, usecols=['ID', 'Index', 'Text'])
df_zh = pd.read_csv(zh_file_path, usecols=['ID', 'Index', 'Text'])

# 重命名 Text 列
df_en = df_en.rename(columns={'Text': 'enText'})
df_zh = df_zh.rename(columns={'Text': 'zhText'})

# 定义清理函数，移除 ^ 及其后面的部分
def clean_text(text):
    if pd.isna(text):  # 检查是否为 NaN
        return text
    return re.sub(r'\^.*$', '', str(text))  # 移除 ^ 及其后面的所有字符

# 清理 enText 和 zhText 列
df_en['enText'] = df_en['enText'].apply(clean_text)
df_zh['zhText'] = df_zh['zhText'].apply(clean_text)

# 合并两个 DataFrame
df_merged = pd.concat([df_en[['ID', 'Index', 'enText']], df_zh['zhText']], axis=1)

# MySQL 连接参数
mysql_user = 'root'
mysql_password = 'Lzr@136595755'  # 密码中包含 @，需要编码
mysql_host = 'localhost'
mysql_database = 'esodata'
table_name = 'esotext'

# 对密码进行 URL 编码
encoded_password = quote_plus(mysql_password)

# 创建数据库引擎，使用编码后的密码
engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_database}')

# 将数据写入 MySQL
df_merged.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=10000, method='multi')

# 记录结束时间
end_time = time.time()
print(f"处理完成，总耗时: {end_time - start_time:.2f} 秒")