#用来合并两份lang.csv文件，输出到/public/data/data.csv并且存入数据库
import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
import time

def clean_text(text):
    # 如果是字符串，移除以 ^ 开头的子字符串和控制字符（如 ^Z 或 \x1A）
    if isinstance(text, str):
        text = re.sub(r'\^[A-Za-z]+', '', text)  # 移除以 ^ 开头的子字符串
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)  # 移除控制字符
        return text.strip()
    return text

def merge_csv_files(en_file, zh_file, output_file, chunk_size=10000):
    # 初始化输出 CSV 文件
    first_chunk = True
    merged_chunks = []
    
    # 分块读取 CSV 文件
    en_reader = pd.read_csv(en_file, chunksize=chunk_size)
    zh_reader = pd.read_csv(zh_file, chunksize=chunk_size)
    
    for en_chunk, zh_chunk in zip(en_reader, zh_reader):
        # 确保两块行数一致
        if len(en_chunk) != len(zh_chunk):
            raise ValueError(f"块行数不匹配：en_chunk 有 {len(en_chunk)} 行，zh_chunk 有 {len(zh_chunk)} 行")
        
        # 选择需要的列
        en_chunk = en_chunk[['ID', 'Index', 'Text']].rename(columns={'Text': 'enText'})
        zh_chunk = zh_chunk[['ID', 'Index', 'Text']].rename(columns={'Text': 'zhText'})
        
        # 清理 enText 和 zhText 中的 ^ 字符和控制字符
        en_chunk['enText'] = en_chunk['enText'].apply(clean_text)
        zh_chunk['zhText'] = zh_chunk['zhText'].apply(clean_text)
        
        # 重置索引以确保按行对齐
        en_chunk = en_chunk.reset_index(drop=True)
        zh_chunk = zh_chunk.reset_index(drop=True)
        
        # 按列拼接（逐行对应）
        merged_chunk = pd.concat([en_chunk[['ID', 'Index', 'enText']], zh_chunk[['zhText']]], axis=1)
        
        # 保存到 CSV（追加模式）
        merged_chunk.to_csv(output_file, mode='a', index=False, encoding='utf-8-sig', header=first_chunk)
        first_chunk = False
        
        # 存储合并后的分块用于数据库插入
        merged_chunks.append(merged_chunk)
    
    # 合并所有分块为完整数据框
    merged_df = pd.concat(merged_chunks, ignore_index=True)
    
    # 验证合并后的行数
    if len(merged_df) != 1094981:
        print(f"警告：合并后的数据有 {len(merged_df)} 行，预期 1094981 行，请检查输入文件")
    
    return merged_df

def connect_to_mysql(mysql_user, mysql_password, mysql_host, mysql_database, max_retries=3):
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                user=mysql_user,
                password=mysql_password,
                host=mysql_host,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            cursor = connection.cursor()
            
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database}")
            cursor.execute(f"USE {mysql_database}")
            return connection, cursor
        except Error as e:
            print(f"连接尝试 {attempt + 1} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待 2 秒后重试
            else:
                raise e
    return None, None

def write_to_mysql(df, mysql_user, mysql_password, mysql_host, mysql_database, table_name, chunk_size=10000):
    connection = None
    cursor = None
    try:
        # 连接到 MySQL
        connection, cursor = connect_to_mysql(mysql_user, mysql_password, mysql_host, mysql_database)
        
        # 创建表（如果不存在）
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ID BIGINT PRIMARY KEY,
            `Index` INT,
            enText TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            zhText TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        )
        """
        cursor.execute(create_table_query)
        
        # 插入数据的 SQL 语句
        insert_query = f"""
        INSERT INTO {table_name} (ID, `Index`, enText, zhText)
        VALUES (%s, %s, %s, %s)
        """
        
        # 分块插入数据
        total_rows = 0
        for start in range(0, len(df), chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            data = [tuple(row) for row in chunk.values]
            cursor.executemany(insert_query, data)
            total_rows += cursor.rowcount
            connection.commit()  # 每块提交一次
            print(f"已插入 {total_rows} 行数据到 {table_name} 表")
        
        print(f"总计成功插入 {total_rows} 行数据到 {table_name} 表")
        
    except Error as e:
        print(f"错误: {e}")
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL 连接已关闭")

def main():
    # 文件路径
    en_file = 'C:/projects/ESOCN/public/data/en.lang.csv'
    zh_file = 'C:/projects/ESOCN/public/data/zh.lang.csv'
    output_file = 'C:/projects/ESOCN/public/data/data.csv'
    
    # 数据库连接信息
    mysql_user = 'root'
    mysql_password = 'Lzr@136595755'
    mysql_host = 'localhost'
    mysql_database = 'esodata'
    table_name = 'esotext'
    
    # 合并 CSV 文件
    merged_df = merge_csv_files(en_file, zh_file, output_file)
    
    # 写入 MySQL 数据库
    write_to_mysql(merged_df, mysql_user, mysql_password, mysql_host, mysql_database, table_name)

if __name__ == "__main__":
    main()