const { createApp, ref } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

const app = createApp({
    setup() {
        const activeTab = ref('query');
        const queryInput = ref('');
        const updateInput = ref('');
        const deleteInput = ref('');
        const queryResult = ref([]);
        const tableColumns = ref([]);
        const backups = ref([]);
        const showQueryResult = ref(false);

        // 加载状态
        const loading = ref({
            query: false,
            update: false,
            delete: false,
            backup: false,
            restore: false
        });

        // 执行日志
        const logs = ref({
            query: [],
            update: [],
            delete: [],
            backup: []
        });

        // 格式化消息内容
        const formatMessage = (content) => {
            if (!content) return '';
            
            // 将换行符转换为<br>
            content = content.replace(/\n/g, '<br>');
            
            // 处理代码块
            content = content.replace(/```(.*?)\n([\s\S]*?)```/g, (match, language, code) => {
                return `<div class="sql-code"><pre><code>${code.trim()}</code></pre></div>`;
            });
            
            return content;
        };

        // 添加日志
        const addLog = (type, message, options = {}) => {
            const log = {
                time: new Date().toLocaleTimeString(),
                message,
                type: options.type || 'primary',
                color: options.color || '#409EFF',
                sql: options.sql || null,
                chat_messages: options.chat_messages || null
            };
            logs.value[type].unshift(log);
        };

        // 清除日志
        const clearLogs = (type) => {
            logs.value[type] = [];
        };

        // 处理查询
        const handleQuery = async () => {
            if (!queryInput.value.trim()) {
                ElMessage.warning('请输入查询需求');
                return;
            }

            loading.value.query = true;
            clearLogs('query');
            showQueryResult.value = false;
            addLog('query', '开始处理查询请求...', { type: 'primary' });

            try {
                addLog('query', '正在分析查询需求...', { type: 'info' });
                const response = await axios.post('/api/query', {
                    query: queryInput.value
                });
                
                if (response.data.success) {
                    queryResult.value = response.data.result;
                    showQueryResult.value = true;
                    
                    if (queryResult.value.length > 0) {
                        tableColumns.value = Object.keys(queryResult.value[0]);
                    }
                    
                    // 添加AI对话日志
                    if (response.data.chat_messages && response.data.chat_messages.length > 0) {
                        addLog('query', 'AI分析过程：', {
                            type: 'info',
                            chat_messages: response.data.chat_messages
                        });
                    }
                    
                    addLog('query', '生成SQL语句：', { 
                        type: 'success',
                        sql: response.data.sql 
                    });
                    
                    const resultCount = queryResult.value.length;
                    if (resultCount > 0) {
                        addLog('query', `查询完成，找到 ${resultCount} 条记录`, { 
                            type: 'success',
                            color: '#67C23A'
                        });
                        ElMessage.success(`查询成功，找到 ${resultCount} 条记录`);
                    } else {
                        addLog('query', '查询完成，未找到匹配的数据', { 
                            type: 'warning',
                            color: '#E6A23C'
                        });
                        ElMessage.warning('未找到匹配的数据');
                    }
                } else {
                    addLog('query', `查询失败：${response.data.message}`, { 
                        type: 'error',
                        color: '#F56C6C'
                    });
                    ElMessage.error(response.data.message || '查询失败');
                }
            } catch (error) {
                addLog('query', `发生错误：${error.message}`, { 
                    type: 'error',
                    color: '#F56C6C'
                });
                ElMessage.error('查询出错：' + error.message);
            } finally {
                loading.value.query = false;
            }
        };

        // 处理更新
        const handleUpdate = async () => {
            if (!updateInput.value.trim()) {
                ElMessage.warning('请输入更新需求');
                return;
            }

            try {
                const result = await ElMessageBox.confirm(
                    '确定要执行更新操作吗？',
                    '确认',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }
                );

                if (result) {
                    loading.value.update = true;
                    clearLogs('update');
                    addLog('update', '开始处理更新请求...', { type: 'primary' });
                    addLog('update', '正在分析更新需求...', { type: 'info' });

                    const response = await axios.post('/api/update', {
                        query: updateInput.value
                    });
                    
                    if (response.data.success) {
                        // 添加AI对话日志
                        if (response.data.chat_messages && response.data.chat_messages.length > 0) {
                            addLog('update', 'AI分析过程：', {
                                type: 'info',
                                chat_messages: response.data.chat_messages
                            });
                        }
                        
                        addLog('update', '生成SQL语句：', { 
                            type: 'success',
                            sql: response.data.sql 
                        });
                        addLog('update', '更新操作执行成功', { 
                            type: 'success',
                            color: '#67C23A'
                        });
                        ElMessage.success('更新成功');
                        updateInput.value = '';
                    } else {
                        addLog('update', `更新失败：${response.data.message}`, { 
                            type: 'error',
                            color: '#F56C6C'
                        });
                        ElMessage.error(response.data.message || '更新失败');
                    }
                }
            } catch (error) {
                if (error !== 'cancel') {
                    addLog('update', `发生错误：${error.message}`, { 
                        type: 'error',
                        color: '#F56C6C'
                    });
                    ElMessage.error('更新出错：' + error.message);
                }
            } finally {
                loading.value.update = false;
            }
        };

        // 处理删除
        const handleDelete = async () => {
            if (!deleteInput.value.trim()) {
                ElMessage.warning('请输入删除条件');
                return;
            }

            try {
                const result = await ElMessageBox.confirm(
                    '确定要执行删除操作吗？此操作不可逆！',
                    '警告',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'danger',
                    }
                );

                if (result) {
                    loading.value.delete = true;
                    clearLogs('delete');
                    addLog('delete', '开始处理删除请求...', { type: 'primary' });
                    addLog('delete', '正在分析删除条件...', { type: 'info' });

                    const response = await axios.post('/api/delete', {
                        query: deleteInput.value
                    });
                    
                    if (response.data.success) {
                        // 添加AI对话日志
                        if (response.data.chat_messages && response.data.chat_messages.length > 0) {
                            addLog('delete', 'AI分析过程：', {
                                type: 'info',
                                chat_messages: response.data.chat_messages
                            });
                        }
                        
                        addLog('delete', '生成SQL语句：', { 
                            type: 'success',
                            sql: response.data.sql 
                        });
                        addLog('delete', '删除操作执行成功', { 
                            type: 'success',
                            color: '#67C23A'
                        });
                        ElMessage.success('删除成功');
                        deleteInput.value = '';
                    } else {
                        addLog('delete', `删除失败：${response.data.message}`, { 
                            type: 'error',
                            color: '#F56C6C'
                        });
                        ElMessage.error(response.data.message || '删除失败');
                    }
                }
            } catch (error) {
                if (error !== 'cancel') {
                    addLog('delete', `发生错误：${error.message}`, { 
                        type: 'error',
                        color: '#F56C6C'
                    });
                    ElMessage.error('删除出错：' + error.message);
                }
            } finally {
                loading.value.delete = false;
            }
        };

        // 刷新备份列表
        const refreshBackups = async () => {
            loading.value.backup = true;
            clearLogs('backup');
            addLog('backup', '正在获取备份列表...', { type: 'info' });

            try {
                const response = await axios.get('/api/backups');
                if (response.data.success) {
                    backups.value = response.data.backups.map(filename => ({
                        filename
                    }));
                    addLog('backup', `成功获取 ${backups.value.length} 个备份文件`, { 
                        type: 'success',
                        color: '#67C23A'
                    });
                } else {
                    addLog('backup', '获取备份列表失败', { 
                        type: 'error',
                        color: '#F56C6C'
                    });
                    ElMessage.error('获取备份列表失败');
                }
            } catch (error) {
                addLog('backup', `发生错误：${error.message}`, { 
                    type: 'error',
                    color: '#F56C6C'
                });
                ElMessage.error('获取备份列表出错：' + error.message);
            } finally {
                loading.value.backup = false;
            }
        };

        // 处理恢复
        const handleRestore = async (filename) => {
            try {
                const result = await ElMessageBox.confirm(
                    '确定要恢复到此备份吗？当前数据将被覆盖！',
                    '警告',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }
                );

                if (result) {
                    loading.value.restore = true;
                    addLog('backup', `开始恢复备份：${filename}`, { type: 'primary' });

                    const response = await axios.post('/api/restore', {
                        filename
                    });
                    
                    if (response.data.success) {
                        addLog('backup', '数据库恢复成功', { 
                            type: 'success',
                            color: '#67C23A'
                        });
                        ElMessage.success('恢复成功');
                        refreshBackups();
                    } else {
                        addLog('backup', `恢复失败：${response.data.message}`, { 
                            type: 'error',
                            color: '#F56C6C'
                        });
                        ElMessage.error(response.data.message || '恢复失败');
                    }
                }
            } catch (error) {
                if (error !== 'cancel') {
                    addLog('backup', `发生错误：${error.message}`, { 
                        type: 'error',
                        color: '#F56C6C'
                    });
                    ElMessage.error('恢复出错：' + error.message);
                }
            } finally {
                loading.value.restore = false;
            }
        };

        // 初始化时获取备份列表
        refreshBackups();

        return {
            activeTab,
            queryInput,
            updateInput,
            deleteInput,
            queryResult,
            tableColumns,
            backups,
            loading,
            logs,
            formatMessage,
            handleQuery,
            handleUpdate,
            handleDelete,
            refreshBackups,
            handleRestore,
            showQueryResult
        };
    }
});

// 使用Element Plus
app.use(ElementPlus, {
    locale: ElementPlusLocaleZhCn, // 使用中文语言包
});

// 全局属性
app.config.globalProperties.$message = ElementPlus.ElMessage;
app.config.globalProperties.$messageBox = ElementPlus.ElMessageBox;

// 挂载应用
app.mount('#app'); 