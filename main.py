import os
import re
import pandas as pd
from agents import create_llm2sql_team
from typing import Optional, Union, Tuple, List
import sqlite3
from datetime import datetime

class LLM2SQLConverter:
    """LLM到SQL转换器"""
    
    def __init__(self, csv_file: str, db_file: str = "data.db"):
        """
        初始化转换器
        :param csv_file: CSV数据文件路径
        :param db_file: SQLite数据库文件路径
        """
        self.df = pd.read_csv(csv_file)
        self.table_info = self._get_table_info()
        self.db_file = db_file
        self.backup_dir = "db_backups"
        
        # 创建备份目录
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 创建智能体团队
        self.manager = create_llm2sql_team()
        
    def _init_database(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect(self.db_file)
        # 将DataFrame写入数据库
        self.df.to_sql('data_table', conn, if_exists='replace', index=False)
        conn.close()
        
    def _backup_database(self) -> str:
        """
        备份数据库
        :return: 备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
        conn = sqlite3.connect(self.db_file)
        backup_conn = sqlite3.connect(backup_file)
        conn.backup(backup_conn)
        conn.close()
        backup_conn.close()
        return backup_file
        
    def _restore_database(self, backup_file: str):
        """
        从备份恢复数据库
        :param backup_file: 备份文件路径
        """
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"备份文件不存在: {backup_file}")
            
        backup_conn = sqlite3.connect(backup_file)
        conn = sqlite3.connect(self.db_file)
        backup_conn.backup(conn)
        backup_conn.close()
        conn.close()
        
    def _get_table_info(self) -> str:
        """获取数据表信息"""
        columns = self.df.columns.tolist()
        dtypes = self.df.dtypes.to_dict()
        
        table_info = "数据表结构如下：\n"
        table_info += "表名: data_table\n"
        table_info += "列信息:\n"
        
        for col in columns:
            table_info += f"- {col}: {dtypes[col]}\n"
            
        # 添加示例数据
        table_info += "\n前3行数据示例:\n"
        table_info += str(self.df.head(3))
        
        return table_info
        
    def convert_to_sql(self, query: str, operation_type: str = "查询", return_messages: bool = False) -> Union[str, Tuple[str, List[dict]]]:
        """
        将自然语言转换为SQL查询
        :param query: 自然语言查询
        :param operation_type: 操作类型（查询/更新/删除）
        :param return_messages: 是否返回对话消息
        :return: SQL查询语句，如果return_messages为True，则同时返回对话消息
        """
        # 构建完整的查询上下文
        full_query = f"""
        {self.table_info}
        
        操作类型: {operation_type}
        用户需求: {query}
        
        请根据上述表结构和数据示例，生成对应的SQL语句。
        如果是更新或删除操作，请特别注意数据安全，添加适当的WHERE条件。
        SQL语句必须使用```sql 和 ``` 标记包裹。
        """
        
        # 启动团队对话
        chat_history = self.manager.groupchat.agents[0].initiate_chat(
            recipient=self.manager,
            clear_history=True,
            message=full_query
        )
        
        # 从对话历史中提取SQL语句
        sql_query = self._extract_sql_from_chat(chat_history)
        
        if return_messages:
            # 提取对话消息
            messages = []
            if hasattr(chat_history, 'messages'):
                messages = chat_history.messages
            elif hasattr(chat_history, 'chat_history'):
                messages = chat_history.chat_history
                
            # 格式化消息
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, dict):
                    formatted_messages.append({
                        'role': msg.get('role', 'unknown'),
                        'content': msg.get('content', ''),
                        'to': msg.get('to', None)
                    })
                else:
                    # 处理其他可能的消息格式
                    formatted_messages.append({
                        'role': getattr(msg, 'role', 'unknown'),
                        'content': str(msg),
                        'to': getattr(msg, 'to', None)
                    })
            
            return sql_query, formatted_messages
            
        return sql_query
        
    def execute_sql(self, sql: str, is_query: bool = True) -> Optional[pd.DataFrame]:
        """
        执行SQL语句
        :param sql: SQL语句
        :param is_query: 是否是查询操作
        :return: 如果是查询操作，返回结果DataFrame；否则返回None
        """
        conn = sqlite3.connect(self.db_file)
        try:
            if is_query:
                result = pd.read_sql_query(sql, conn)
                return result
            else:
                # 非查询操作先备份
                self._backup_database()
                conn.execute(sql)
                conn.commit()
                return None
        finally:
            conn.close()
            
    def list_backups(self) -> list:
        """列出所有可用的备份"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                backups.append(file)
        return sorted(backups, reverse=True)
        
    def _extract_sql_from_chat(self, chat_result) -> str:
        """从对话历史中提取SQL语句"""
        # 使用正则表达式提取 SQL 代码块
        sql_pattern = r"```sql\s*(.*?)\s*```"
        
        # 获取消息内容
        if hasattr(chat_result, 'messages'):
            # 如果有messages属性，获取最后一条消息
            messages = chat_result.messages
            if messages:
                last_message = messages[-1]
                content = last_message.get('content', '') if isinstance(last_message, dict) else str(last_message)
                sql_matches = re.findall(sql_pattern, content, re.DOTALL)
                if sql_matches:
                    sql = sql_matches[0].strip()
                    # 转换SQL语句以适应SQLite
                    sql = self._convert_sql_to_sqlite(sql)
                    return sql
        elif hasattr(chat_result, 'summary'):
            # 如果有summary属性，直接使用summary
            content = chat_result.summary
            sql_matches = re.findall(sql_pattern, content, re.DOTALL)
            if sql_matches:
                sql = sql_matches[0].strip()
                # 转换SQL语句以适应SQLite
                sql = self._convert_sql_to_sqlite(sql)
                return sql
        
        return "-- 未找到有效的SQL语句"

    def _convert_sql_to_sqlite(self, sql: str) -> str:
        """将SQL语句转换为SQLite兼容的格式"""
        # 替换RAND()函数为RANDOM()
        sql = re.sub(r'RAND\(\)', 'RANDOM()', sql, flags=re.IGNORECASE)
        
        # 替换FLOOR()函数为CAST()
        sql = re.sub(
            r'FLOOR\((.*?)\)',
            r'CAST(\1 AS INTEGER)',
            sql,
            flags=re.IGNORECASE
        )
        
        # 替换复杂的随机数生成表达式
        sql = re.sub(
            r'FLOOR\(RANDOM\(\)\s*\*\s*\((\d+)\s*-\s*(\d+)\s*\+\s*1\)\)\s*\+\s*(\d+)',
            r'ABS(RANDOM() % (\1 - \2 + 1)) + \3',
            sql,
            flags=re.IGNORECASE
        )
        
        return sql

def print_menu():
    """打印主菜单"""
    print("\n=== 数据库操作系统 ===")
    print("1. 查询数据")
    print("2. 更新数据")
    print("3. 删除数据")
    print("4. 查看备份列表")
    print("5. 恢复数据库")
    print("6. 退出")
    print("==================")
    
def handle_query(converter: LLM2SQLConverter):
    """处理查询操作"""
    query = input("\n请输入您的查询需求（例如：查找年龄大于25岁的用户）：\n")
    sql, messages = converter.convert_to_sql(query, "查询", True)
    print(f"\n生成的SQL:\n{sql}\n")
    
    confirm = input("是否执行该SQL语句？(y/n): ")
    if confirm.lower() == 'y':
        result = converter.execute_sql(sql, True)
        if result is not None and not result.empty:
            print("\n查询结果：")
            print(result.to_string())
        else:
            print("\n没有找到匹配的数据。")
            
    print("\n对话消息：")
    for msg in messages:
        print(f"角色: {msg['role']}")
        print(f"内容: {msg['content']}")
        print(f"目标: {msg['to']}")
        
def handle_update(converter: LLM2SQLConverter):
    """处理更新操作"""
    query = input("\n请输入您的更新需求（例如：将用户1的年龄更新为30岁）：\n")
    sql, messages = converter.convert_to_sql(query, "更新", True)
    print(f"\n生成的SQL:\n{sql}\n")
    
    confirm = input("是否执行该SQL语句？(y/n): ")
    if confirm.lower() == 'y':
        converter.execute_sql(sql, False)
        print("\n数据已更新。")
        
    print("\n对话消息：")
    for msg in messages:
        print(f"角色: {msg['role']}")
        print(f"内容: {msg['content']}")
        print(f"目标: {msg['to']}")
        
def handle_delete(converter: LLM2SQLConverter):
    """处理删除操作"""
    query = input("\n请输入您的删除需求（例如：删除年龄小于20岁的用户）：\n")
    sql, messages = converter.convert_to_sql(query, "删除", True)
    print(f"\n生成的SQL:\n{sql}\n")
    
    confirm = input("警告：删除操作不可逆！是否执行该SQL语句？(y/n): ")
    if confirm.lower() == 'y':
        converter.execute_sql(sql, False)
        print("\n数据已删除。")
        
    print("\n对话消息：")
    for msg in messages:
        print(f"角色: {msg['role']}")
        print(f"内容: {msg['content']}")
        print(f"目标: {msg['to']}")
        
def handle_restore(converter: LLM2SQLConverter):
    """处理数据库恢复"""
    backups = converter.list_backups()
    if not backups:
        print("\n没有可用的备份。")
        return
        
    print("\n可用的备份文件：")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
        
    choice = input("\n请选择要恢复的备份文件编号（输入数字）：")
    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            backup_file = os.path.join(converter.backup_dir, backups[index])
            converter._restore_database(backup_file)
            print("\n数据库已恢复。")
        else:
            print("\n无效的选择。")
    except ValueError:
        print("\n请输入有效的数字。")
        
def main():
    # 创建测试数据
    test_data = pd.DataFrame({
        'id': range(1, 101),
        'name': [f'用户{i}' for i in range(1, 101)],
        'age': [20 + i % 30 for i in range(1, 101)],
        'score': [80 + i % 20 for i in range(1, 101)]
    })
    
    # 保存测试数据
    test_data.to_csv('test_data.csv', index=False)
    
    # 创建转换器
    converter = LLM2SQLConverter('test_data.csv')
    
    while True:
        print_menu()
        choice = input("请选择操作（输入数字）：")
        
        if choice == '1':
            handle_query(converter)
        elif choice == '2':
            handle_update(converter)
        elif choice == '3':
            handle_delete(converter)
        elif choice == '4':
            backups = converter.list_backups()
            if backups:
                print("\n可用的备份文件：")
                for backup in backups:
                    print(backup)
            else:
                print("\n没有可用的备份。")
        elif choice == '5':
            handle_restore(converter)
        elif choice == '6':
            print("\n感谢使用，再见！")
            break
        else:
            print("\n无效的选择，请重试。")
        
if __name__ == "__main__":
    main() 