import os
from typing import List, Dict, Any
import autogen

class ModelConfig:
    """模型配置"""
    API_KEY = "sk-921cd3ca27944d239b701b93554d6433"
    BASE_URL = "https://api.deepseek.com/v1"
    
    # 配置模型参数
    CONFIG_LIST = [{
        "model": "deepseek-chat",
        "api_key": API_KEY,
        "base_url": BASE_URL,
        "api_type": "openai"
    }]

    # 模型配置
    LLM_CONFIG = {
        "timeout": 300,
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "config_list": CONFIG_LIST
    }

def create_llm2sql_team():
    """创建LLM2SQL转换团队"""
    
    # 创建SQL专家智能体
    sql_expert = autogen.AssistantAgent(
        name="sql_expert",
        system_message="""你是一位资深的SQL专家，主要职责是：
        1. 根据自然语言描述生成准确的SQL查询
        2. 确保SQL语法正确性和最佳实践
        3. 优化查询性能
        4. 处理各种数据类型和复杂查询场景
        请用中文交流，并在生成SQL时注意以下几点：
        - 使用清晰的SQL语法和适当的缩进
        - 添加必要的注释说明
        - 考虑查询性能和索引使用
        - 处理可能的边界情况和错误
        - 生成的SQL语句请使用```sql 和 ``` 包裹
        """,
        llm_config=ModelConfig.LLM_CONFIG
    )
    
    # 创建数据分析师智能体
    data_analyst = autogen.AssistantAgent(
        name="data_analyst",
        system_message="""你是一位专业的数据分析师，主要职责是：
        1. 分析数据需求和上下文
        2. 验证SQL查询结果的正确性
        3. 提供数据洞察和建议
        4. 确保数据质量和一致性
        请用中文交流，并在分析时注意：
        - 理解业务需求和数据上下文
        - 验证数据的完整性和准确性
        - 提供清晰的分析结论和建议
        - 考虑数据安全和隐私问题
        - 如果发现SQL语句有问题，请明确指出并建议修改
        """,
        llm_config=ModelConfig.LLM_CONFIG
    )
    
    # 创建用户代理
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False
    )
    
    # 创建群聊
    groupchat = autogen.GroupChat(
        agents=[user_proxy, data_analyst, sql_expert],
        messages=[],
        max_round=10
    )
    
    # 创建群聊管理器
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=ModelConfig.LLM_CONFIG
    )
    
    return manager 