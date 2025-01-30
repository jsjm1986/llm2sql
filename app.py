from flask import Flask, render_template, jsonify, request
from main import LLM2SQLConverter
import pandas as pd
import os

app = Flask(__name__)

# 创建转换器实例
converter = LLM2SQLConverter('test_data.csv')

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """处理查询请求"""
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'success': False, 'message': '查询内容不能为空'})
            
        # 生成并执行SQL
        sql, chat_messages = converter.convert_to_sql(query, "查询", return_messages=True)
        result = converter.execute_sql(sql, True)
        
        if result is not None:
            # 将DataFrame转换为字典列表
            result_list = result.to_dict('records')
            return jsonify({
                'success': True, 
                'result': result_list,
                'sql': sql,
                'chat_messages': chat_messages
            })
        else:
            return jsonify({'success': False, 'message': '未找到匹配的数据'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/update', methods=['POST'])
def handle_update():
    """处理更新请求"""
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'success': False, 'message': '更新内容不能为空'})
            
        # 生成并执行SQL
        sql, chat_messages = converter.convert_to_sql(query, "更新", return_messages=True)
        converter.execute_sql(sql, False)
        return jsonify({
            'success': True,
            'sql': sql,
            'chat_messages': chat_messages
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/delete', methods=['POST'])
def handle_delete():
    """处理删除请求"""
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'success': False, 'message': '删除条件不能为空'})
            
        # 生成并执行SQL
        sql, chat_messages = converter.convert_to_sql(query, "删除", return_messages=True)
        converter.execute_sql(sql, False)
        return jsonify({
            'success': True,
            'sql': sql,
            'chat_messages': chat_messages
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/backups', methods=['GET'])
def get_backups():
    """获取备份列表"""
    try:
        backups = converter.list_backups()
        return jsonify({'success': True, 'backups': backups})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/restore', methods=['POST'])
def handle_restore():
    """处理恢复请求"""
    try:
        filename = request.json.get('filename')
        if not filename:
            return jsonify({'success': False, 'message': '未指定备份文件'})
            
        backup_path = os.path.join(converter.backup_dir, filename)
        converter._restore_database(backup_path)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    # 确保数据和备份目录存在
    os.makedirs('db_backups', exist_ok=True)
    
    # 如果测试数据不存在，创建测试数据
    if not os.path.exists('test_data.csv'):
        test_data = pd.DataFrame({
            'id': range(1, 101),
            'name': [f'用户{i}' for i in range(1, 101)],
            'age': [20 + i % 30 for i in range(1, 101)],
            'score': [80 + i % 20 for i in range(1, 101)]
        })
        test_data.to_csv('test_data.csv', index=False)
    
    app.run(debug=True) 