import pytest
import pandas as pd
import asyncio
from main import LLM2SQLConverter

@pytest.fixture
def test_data():
    """创建测试数据"""
    data = pd.DataFrame({
        'id': range(1, 11),
        'name': [f'测试用户{i}' for i in range(1, 11)],
        'age': [20 + i for i in range(1, 11)],
        'score': [85 + i % 10 for i in range(1, 11)]
    })
    data.to_csv('test_data.csv', index=False)
    return 'test_data.csv'

@pytest.mark.asyncio
async def test_basic_queries(test_data):
    """测试基本查询转换"""
    converter = LLM2SQLConverter(test_data)
    
    test_cases = [
        {
            'query': '查找年龄大于25岁的用户名单',
            'expected_keywords': ['SELECT', 'FROM', 'WHERE', 'age', '>', '25']
        },
        {
            'query': '计算所有用户的平均分数',
            'expected_keywords': ['SELECT', 'AVG', 'score', 'FROM']
        },
        {
            'query': '按年龄排序显示用户信息',
            'expected_keywords': ['SELECT', 'FROM', 'ORDER BY', 'age']
        }
    ]
    
    for case in test_cases:
        sql = await converter.convert_to_sql(case['query'])
        # 验证生成的SQL包含预期关键字
        for keyword in case['expected_keywords']:
            assert keyword.lower() in sql.lower(), f"SQL应包含关键字: {keyword}"
            
@pytest.mark.asyncio
async def test_complex_queries(test_data):
    """测试复杂查询转换"""
    converter = LLM2SQLConverter(test_data)
    
    test_cases = [
        {
            'query': '找出分数最高的前3名用户的姓名和年龄',
            'expected_keywords': ['SELECT', 'name', 'age', 'ORDER BY', 'score', 'DESC', 'LIMIT', '3']
        },
        {
            'query': '计算每个年龄段的平均分数，并按平均分降序排列',
            'expected_keywords': ['SELECT', 'age', 'AVG', 'score', 'GROUP BY', 'ORDER BY', 'DESC']
        }
    ]
    
    for case in test_cases:
        sql = await converter.convert_to_sql(case['query'])
        # 验证生成的SQL包含预期关键字
        for keyword in case['expected_keywords']:
            assert keyword.lower() in sql.lower(), f"SQL应包含关键字: {keyword}" 