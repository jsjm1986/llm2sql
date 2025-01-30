# LLM2SQL - Intelligent Database Assistant

English | [简体中文](README.md)

A natural language to SQL conversion system based on large language models, providing an intuitive database operation interface. Complete complex database operations through natural language descriptions without writing SQL code.

## 🌟 Features

### 1. Natural Language Interaction
- Support natural language descriptions for database operations
- Intelligent understanding of user intent and conversion to accurate SQL statements
- Multi-round dialogue support with real-time AI analysis display
- Support for complex query conditions and business logic

### 2. Database Operations
- Query Data: Support complex query conditions and data filtering
- Update Data: Generate secure update statements intelligently
- Delete Data: Include safety confirmation mechanism
- Automatic Backup: Create database backups before important operations
- Data Recovery: Support rollback to previous backup points

### 3. Intelligent Agent System
- Multi-agent Collaboration:
  - SQL Expert: Responsible for generating and optimizing SQL statements
  - Data Analyst: Assist in understanding data structure and business logic
  - User Agent: Handle user input and result display
- Real-time Dialogue Display: Visualize interactions between agents

### 4. User Interface
- Modern Web Interface: Based on Vue 3 and Element Plus
- Responsive Design: Adapt to various screen sizes
- Real-time Feedback:
  - Execution progress display
  - SQL preview with syntax highlighting
  - Instant result display
  - Error handling and notifications
- Operation Logs: Detailed recording of all operation steps

## 🛠️ Technology Stack

### Backend
- Python 3.8+
- Flask: Web framework
- SQLite: Database
- Pandas: Data processing
- AutoGen: Multi-agent system
- Deepseek: Large language model support

### Frontend
- Vue 3: Frontend framework
- Element Plus: UI component library
- Axios: HTTP client
- CSS3: Custom styles and animations

## 📦 Installation

### Requirements
- Python 3.8 or higher
- pip package manager
- Node.js 14+ (optional, for frontend development)
- Modern browsers (Chrome, Firefox, Safari, etc.)

### Setup Steps

1. Clone the project:
```bash
git clone https://github.com/jsjm1986/llm2sql.git
cd llm2sql
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Windows
set DEEPSEEK_API_KEY=your_api_key

# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key
```

5. Run the application:
```bash
python app.py
```

6. Access the application:
Open your browser and visit `http://localhost:5000`

## 📝 Usage Examples

### 1. Data Queries
```plaintext
Example 1: Find users over 25 years old
Generated SQL: SELECT * FROM data_table WHERE age > 25

Example 2: Find top 10 users with highest scores
Generated SQL: SELECT * FROM data_table ORDER BY score DESC LIMIT 10
```

### 2. Data Updates
```plaintext
Example 1: Update user 1's age to 30
Generated SQL: UPDATE data_table SET age = 30 WHERE id = 1

Example 2: Add 5 points to all users with scores above 90
Generated SQL: UPDATE data_table SET score = score + 5 WHERE score > 90
```

### 3. Data Deletion
```plaintext
Example 1: Delete users under 18 years old
Generated SQL: DELETE FROM data_table WHERE age < 18

Example 2: Delete user records with zero score
Generated SQL: DELETE FROM data_table WHERE score = 0
```

## 🔒 Security Features

1. Automatic Backup:
   - Create backups before update/delete operations
   - Backup files include timestamps
   - Support rollback anytime

2. Operation Confirmation:
   - Secondary confirmation for important operations
   - Clear warning messages
   - Operation log recording

3. Data Validation:
   - SQL injection protection
   - Input data validation
   - Error handling mechanism

## 📁 Project Structure

```
llm2sql/
├── app.py              # Flask application main file
├── main.py             # Core logic implementation
├── agents.py           # Intelligent agent definitions
├── requirements.txt    # Project dependencies
├── static/            # Static resources
│   ├── css/          # Style files
│   └── js/           # JavaScript files
├── templates/         # HTML templates
├── db_backups/       # Database backups
└── README.md         # Project documentation
```

## ❓ FAQ

1. Q: How to handle API key expiration?
   A: Update the DEEPSEEK_API_KEY value in environment variables.

2. Q: What to do when database backups take up too much space?
   A: Regularly clean up old backup files, keeping only the most recent ones.

3. Q: How to customize the data table structure?
   A: Modify the test data generation part in main.py or directly import your own CSV file.

4. Q: Why can't some complex queries be converted correctly?
   A: Current version may have limited support for specific complex queries. Consider breaking them down into simpler queries.

## 🚀 Development Plans

- [ ] Support more database types (MySQL, PostgreSQL, etc.)
- [ ] Add user authentication system
- [ ] Support data visualization
- [ ] Add batch operation functionality
- [ ] Optimize SQL generation performance
- [ ] Support more natural language models
- [ ] Add API documentation
- [ ] Support data import/export

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 👥 Contact

- Project Maintainer: jsjm1986
- GitHub: [https://github.com/jsjm1986](https://github.com/jsjm1986)
- Project Repository: [https://github.com/jsjm1986/llm2sql](https://github.com/jsjm1986/llm2sql)

## 🙏 Acknowledgments

- Deepseek - Providing powerful language model support
- AutoGen - Providing excellent multi-agent framework
- Vue.js Team - Providing outstanding frontend framework
- Element Plus Team - Providing beautiful UI components 