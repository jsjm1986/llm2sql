# LLM2SQL - 智能数据库助手

简体中文 | [English](README_EN.md)

基于大语言模型的自然语言到SQL转换系统，支持直观的数据库操作界面。通过自然语言描述即可完成复杂的数据库操作，无需编写SQL代码。

## 🌟 功能特点

### 1. 自然语言交互
- 支持使用自然语言描述数据库操作需求
- 智能理解用户意图并转换为准确的SQL语句
- 多轮对话支持，实时展示AI分析过程
- 支持复杂的查询条件和业务逻辑

### 2. 数据库操作
- 查询数据：支持复杂的查询条件和数据筛选
- 更新数据：智能生成安全的更新语句
- 删除数据：包含安全确认机制
- 自动备份：重要操作前自动创建数据库备份
- 数据恢复：支持随时回滚到之前的备份点

### 3. 智能代理系统
- 多智能体协作：
  - SQL专家：负责生成和优化SQL语句
  - 数据分析师：协助理解数据结构和业务逻辑
  - 用户代理：处理用户输入和结果展示
- 实时对话展示：可视化展示代理之间的交互过程

### 4. 用户界面
- 现代化Web界面：基于Vue 3和Element Plus
- 响应式设计：适配各种屏幕尺寸
- 实时反馈：
  - 执行进度展示
  - SQL预览和语法高亮
  - 结果即时显示
  - 错误提示和处理
- 操作日志：详细记录所有操作步骤

## 🛠️ 技术栈

### 后端
- Python 3.8+
- Flask：Web框架
- SQLite：数据库
- Pandas：数据处理
- AutoGen：多智能体系统
- Deepseek：大语言模型支持

### 前端
- Vue 3：前端框架
- Element Plus：UI组件库
- Axios：HTTP客户端
- CSS3：自定义样式和动画

## 📦 安装说明

### 环境要求
- Python 3.8或更高版本
- pip包管理器
- Node.js 14+（可选，用于前端开发）
- 现代浏览器（Chrome, Firefox, Safari等）

### 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/jsjm1986/llm2sql.git
cd llm2sql
```

2. 创建并激活虚拟环境：
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
# Windows
set DEEPSEEK_API_KEY=your_api_key

# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key
```

5. 运行应用：
```bash
python app.py
```

6. 访问应用：
打开浏览器访问 `http://localhost:5000`

## 📝 使用示例

### 1. 数据查询
```plaintext
示例1：查找年龄大于25岁的用户
生成SQL：SELECT * FROM data_table WHERE age > 25

示例2：查找分数最高的前10名用户
生成SQL：SELECT * FROM data_table ORDER BY score DESC LIMIT 10
```

### 2. 数据更新
```plaintext
示例1：将用户1的年龄更新为30岁
生成SQL：UPDATE data_table SET age = 30 WHERE id = 1

示例2：给所有分数大于90的用户加5分
生成SQL：UPDATE data_table SET score = score + 5 WHERE score > 90
```

### 3. 数据删除
```plaintext
示例1：删除年龄小于18岁的用户
生成SQL：DELETE FROM data_table WHERE age < 18

示例2：删除分数为0的用户记录
生成SQL：DELETE FROM data_table WHERE score = 0
```

## 🔒 安全特性

1. 自动备份：
   - 更新/删除操作前自动创建备份
   - 备份文件包含时间戳
   - 支持随时回滚

2. 操作确认：
   - 重要操作需二次确认
   - 清晰的警告信息
   - 操作日志记录

3. 数据验证：
   - SQL注入防护
   - 输入数据验证
   - 错误处理机制

## 📁 项目结构

```
llm2sql/
├── app.py              # Flask应用主文件
├── main.py             # 核心逻辑实现
├── agents.py           # 智能代理定义
├── requirements.txt    # 项目依赖
├── static/            # 静态资源
│   ├── css/          # 样式文件
│   └── js/           # JavaScript文件
├── templates/         # HTML模板
├── db_backups/       # 数据库备份
└── README.md         # 项目文档
```

## ❓ 常见问题

1. Q: 如何处理API密钥过期？
   A: 更新环境变量中的DEEPSEEK_API_KEY值。

2. Q: 数据库备份占用空间过大怎么办？
   A: 定期清理旧的备份文件，保留最近的几个备份点。

3. Q: 如何自定义数据表结构？
   A: 修改main.py中的测试数据生成部分，或直接导入自己的CSV文件。

4. Q: 为什么某些复杂查询无法正确转换？
   A: 当前版本可能对特定复杂查询支持有限，建议将复杂查询拆分为多个简单查询。

## 🚀 开发计划

- [ ] 支持更多数据库类型（MySQL, PostgreSQL等）
- [ ] 添加用户认证系统
- [ ] 支持数据可视化
- [ ] 添加批量操作功能
- [ ] 优化SQL生成性能
- [ ] 支持更多自然语言模型
- [ ] 添加API文档
- [ ] 支持数据导入/导出

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👥 联系方式

- 项目维护者：蒋世杰
- GitHub：[https://github.com/jsjm1986](https://github.com/jsjm1986)
- 项目地址：[https://github.com/jsjm1986/llm2sql](https://github.com/jsjm1986/llm2sql)

## 🙏 致谢

- Deepseek - 提供强大的语言模型支持
- AutoGen - 提供优秀的多智能体框架
- Vue.js团队 - 提供出色的前端框架
- Element Plus团队 - 提供美观的UI组件库 
