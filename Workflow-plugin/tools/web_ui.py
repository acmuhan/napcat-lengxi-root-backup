# -*- coding: utf-8 -*-
"""工作流Web UI模块 - 与框架web模板风格一致"""


def get_html():
    """获取HTML内容"""
    return '''
<style>
/* 页面头部 - 与框架风格一致 */
.workflow-page { padding: 1rem; }
.workflow-header {
    background: var(--theme-gradient, linear-gradient(135deg, #5865F2, #7289DA));
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}
.header-content { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.header-title { display: flex; align-items: center; gap: 1rem; color: #fff; }
.header-icon { width: 56px; height: 56px; background: rgba(255,255,255,0.15); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
.header-title h4 { margin: 0; font-size: 1.25rem; font-weight: 600; }
.header-title p { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.85; }
.header-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.action-btn {
    padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); color: #fff; border: none;
    border-radius: 8px; font-size: 0.85rem; cursor: pointer; display: flex; align-items: center; gap: 0.4rem; transition: all 0.2s;
}
.action-btn:hover { background: rgba(255,255,255,0.3); }
.action-btn.primary { background: #fff; color: var(--theme-primary, #5865F2); }
.action-btn.primary:hover { background: #f0f0f0; }

/* 主容器 */
.workflow-main { display: flex; gap: 1rem; height: calc(100vh - 220px); min-height: 500px; }

/* 侧边栏 */
.workflow-sidebar {
    width: 280px; background: #fff; border-radius: 16px; padding: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); overflow-y: auto; flex-shrink: 0;
    border: 1px solid #e2e8f0;
}
.sidebar-section { margin-bottom: 1rem; }
.sidebar-title { font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 0.5rem; padding: 0 0.5rem; }

/* 节点面板 */
.node-palette-item {
    padding: 0.75rem; margin-bottom: 0.5rem; background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; cursor: grab; display: flex; align-items: center; gap: 0.75rem; transition: all 0.2s;
}
.node-palette-item:hover { border-color: var(--theme-primary, #5865F2); background: rgba(88, 101, 242, 0.05); transform: translateX(4px); }
.node-palette-item i { font-size: 1.25rem; width: 28px; text-align: center; }
.node-palette-item strong { font-size: 0.9rem; color: #1e293b; }
.node-palette-item small { font-size: 0.75rem; color: #94a3b8; }

/* 工作流列表 */
.workflow-list-item {
    padding: 0.75rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    margin-bottom: 0.5rem; cursor: pointer; transition: all 0.2s;
}
.workflow-list-item:hover { border-color: var(--theme-primary, #5865F2); }
.workflow-list-item.active { border-color: var(--theme-primary, #5865F2); background: rgba(88, 101, 242, 0.1); border-left: 3px solid var(--theme-primary, #5865F2); }
.workflow-list-item .wf-name { font-weight: 600; font-size: 0.9rem; color: #1e293b; }
.workflow-list-item .wf-trigger { font-size: 0.75rem; color: #64748b; margin-top: 2px; }
.workflow-list-item .wf-actions { display: flex; gap: 0.25rem; margin-top: 0.5rem; }
.wf-btn { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; border: none; cursor: pointer; transition: all 0.2s; }
.wf-btn.toggle-on { background: #d1fae5; color: #059669; }
.wf-btn.toggle-off { background: #fee2e2; color: #dc2626; }
.wf-btn.delete { background: #fef2f2; color: #ef4444; }
.wf-btn:hover { opacity: 0.8; }

/* 画布区域 */
.workflow-canvas {
    flex: 1; background: #fff; border-radius: 16px; position: relative; overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid #e2e8f0;
}
.canvas-inner {
    width: 3000px; height: 2000px; position: relative;
    background-image: radial-gradient(circle, #e2e8f0 1px, transparent 1px); background-size: 20px 20px;
}

/* 节点样式 */
.workflow-node {
    position: absolute; min-width: 180px; background: #fff; border: 2px solid #e2e8f0;
    border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); cursor: move; z-index: 10;
}
.workflow-node.selected { border-color: var(--theme-primary, #5865F2); box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.25); }
.workflow-node.trigger { border-color: #10b981; }
.workflow-node.condition { border-color: #f59e0b; }
.workflow-node.action { border-color: #3b82f6; }
.workflow-node.delay { border-color: #6b7280; }
.workflow-node.set_var { border-color: #06b6d4; }
.workflow-node.storage { border-color: #ef4444; }
.workflow-node.global_storage { border-color: #8b5cf6; }
.workflow-node.leaderboard { border-color: #f59e0b; }
.workflow-node.list_random { border-color: #ec4899; }
.workflow-node.comment { border-color: #9ca3af; background: #f9fafb; opacity: 0.85; }

.node-header {
    padding: 0.6rem 0.75rem; border-bottom: 1px solid #f1f5f9; display: flex;
    align-items: center; gap: 0.5rem; font-weight: 600; font-size: 0.85rem; color: #374151;
}
.node-body { padding: 0.6rem 0.75rem; font-size: 0.8rem; color: #64748b; }
.node-port {
    width: 12px; height: 12px; background: #fff; border: 2px solid #94a3b8;
    border-radius: 50%; position: absolute; cursor: crosshair; z-index: 20; transition: all 0.2s;
}
.node-port.input { top: 50%; left: -6px; transform: translateY(-50%); }
.node-port.output { top: 50%; right: -6px; transform: translateY(-50%); }
.node-port.output-1 { top: 35%; }
.node-port.output-2 { top: 65%; border-color: #ef4444; }
.node-port:hover { background: var(--theme-primary, #5865F2); border-color: var(--theme-primary, #5865F2); transform: scale(1.2); }
.node-port.waiting { background: #22c55e; border-color: #22c55e; animation: pulse 1s infinite; }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.3); } }

.btn-delete-node {
    position: absolute; top: -8px; right: -8px; width: 20px; height: 20px;
    border-radius: 50%; background: #ef4444; color: #fff; border: none;
    font-size: 10px; cursor: pointer; display: none; z-index: 30; transition: all 0.2s;
}
.workflow-node:hover .btn-delete-node { display: flex; align-items: center; justify-content: center; }
.btn-delete-node:hover { background: #dc2626; transform: scale(1.1); }

.connection-line { stroke: #94a3b8; stroke-width: 2; fill: none; }

/* 模态框样式 - 与框架一致 */
.modal-content { border: none; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.modal-header {
    background: var(--theme-gradient, linear-gradient(135deg, #5865F2, #7289DA));
    color: #fff; padding: 1rem 1.25rem; border: none;
}
.modal-header .modal-title { font-size: 1rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
.modal-header .btn-close { filter: brightness(0) invert(1); }
.modal-header-actions { display: flex; gap: 0.5rem; align-items: center; }
.modal-btn {
    padding: 0.4rem 0.75rem; border: none; border-radius: 6px; font-size: 0.8rem;
    cursor: pointer; display: flex; align-items: center; gap: 0.3rem;
    background: rgba(255,255,255,0.2); color: #fff; transition: all 0.2s;
}
.modal-btn:hover { background: rgba(255,255,255,0.3); }
.modal-btn.primary { background: #fff; color: var(--theme-primary, #5865F2); }
.modal-btn.primary:hover { background: #f0f0f0; }
.modal-btn.success { background: #10b981; color: #fff; }
.modal-btn.success:hover { background: #059669; }
.modal-body { padding: 1.25rem; }
.modal-footer { border-top: 1px solid #e2e8f0; padding: 1rem 1.25rem; }
.modal-footer .btn { border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.85rem; }
.modal-footer .btn-primary { background: var(--theme-gradient, linear-gradient(135deg, #5865F2, #7289DA)); border: none; }
.modal-footer .btn-primary:hover { opacity: 0.9; }

/* 表单控件 */
.form-label { font-weight: 500; color: #374151; font-size: 0.875rem; margin-bottom: 0.4rem; }
.form-control, .form-select {
    border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem 0.75rem; font-size: 0.9rem;
    transition: all 0.2s;
}
.form-control:focus, .form-select:focus {
    border-color: var(--theme-primary, #5865F2); outline: none;
    box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.1);
}
.form-control::placeholder { color: #9ca3af; }

/* 新建类型卡片 */
.new-type-card {
    padding: 1.5rem; border: 2px solid #e2e8f0; border-radius: 12px;
    cursor: pointer; text-align: center; transition: all 0.2s; background: #fff;
}
.new-type-card:hover { border-color: var(--theme-primary, #5865F2); background: rgba(88, 101, 242, 0.05); transform: translateY(-2px); }
.new-type-card i { font-size: 2.5rem; margin-bottom: 0.75rem; display: block; }
.new-type-card h6 { margin: 0 0 0.25rem; color: #1e293b; }
.new-type-card small { color: #64748b; }

/* 提示框 */
.hint-box { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 0.75rem; font-size: 0.85rem; color: #0369a1; }
.hint-box code { background: #e0f2fe; color: #0284c7; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; }

/* 变量表格 */
.var-table { font-size: 0.85rem; }
.var-table th { background: #f8fafc; font-weight: 600; color: #475569; }
.var-table code { background: #f1f5f9; color: #6366f1; padding: 2px 6px; border-radius: 4px; }

/* Toast */
.toast-msg {
    position: fixed; top: 80px; right: 20px; z-index: 9999; padding: 0.75rem 1.25rem;
    border-radius: 10px; display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15); animation: slideIn 0.3s ease;
}
.toast-msg.success { background: #d1fae5; color: #059669; }
.toast-msg.error { background: #fee2e2; color: #dc2626; }
.toast-msg.info { background: #dbeafe; color: #2563eb; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* 响应式 */
@media (max-width: 992px) {
    .workflow-main { flex-direction: column; height: auto; }
    .workflow-sidebar { width: 100%; max-height: 300px; }
}
@media (max-width: 768px) {
    .header-content { flex-direction: column; text-align: center; }
    .header-title { flex-direction: column; }
    .header-actions { justify-content: center; }
}
</style>

<div class="workflow-page">
    <!-- 页面头部 -->
    <div class="workflow-header">
        <div class="header-content">
            <div class="header-title">
                <div class="header-icon"><i class="bi bi-diagram-3"></i></div>
                <div>
                    <h4>可视化工作流</h4>
                    <p>拖拽节点创建自动化流程</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="action-btn" onclick="showAiModal()"><i class="bi bi-stars"></i> AI生成</button>
                <button class="action-btn" onclick="showNewModal()"><i class="bi bi-plus-lg"></i> 新建</button>
                <button class="action-btn primary" onclick="saveWorkflow()"><i class="bi bi-save"></i> 保存</button>
            </div>
        </div>
    </div>

    <!-- 主内容区 -->
    <div class="workflow-main">
        <div class="workflow-sidebar">
            <div class="sidebar-section">
                <div class="sidebar-title">基础节点</div>
                <div class="node-palette-item" draggable="true" data-type="trigger"><i class="bi bi-lightning text-success"></i><div><strong>触发器</strong><br><small>消息触发</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="condition"><i class="bi bi-signpost-split text-warning"></i><div><strong>条件</strong><br><small>分支判断</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="action"><i class="bi bi-play-circle text-primary"></i><div><strong>动作</strong><br><small>回复/API/运算</small></div></div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-title">数据节点</div>
                <div class="node-palette-item" draggable="true" data-type="storage"><i class="bi bi-database text-danger"></i><div><strong>用户存储</strong><br><small>个人数据</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="global_storage"><i class="bi bi-globe text-primary"></i><div><strong>全局存储</strong><br><small>共享数据</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="leaderboard"><i class="bi bi-trophy text-warning"></i><div><strong>排行榜</strong><br><small>获取排名</small></div></div>
            </div>
            <div class="sidebar-section">
                <div class="sidebar-title">辅助节点</div>
                <div class="node-palette-item" draggable="true" data-type="set_var"><i class="bi bi-braces text-info"></i><div><strong>变量</strong><br><small>临时变量</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="list_random"><i class="bi bi-shuffle text-danger"></i><div><strong>随机抽取</strong><br><small>奖池/抽奖</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="delay"><i class="bi bi-clock text-secondary"></i><div><strong>延时</strong><br><small>等待</small></div></div>
                <div class="node-palette-item" draggable="true" data-type="comment"><i class="bi bi-chat-quote text-muted"></i><div><strong>注释</strong><br><small>备注说明</small></div></div>
            </div>
            <hr class="my-3">
            <div class="sidebar-title">工作流列表</div>
            <div id="workflowList"></div>
        </div>
        <div class="workflow-canvas" id="canvas">
            <svg id="connectionsSvg" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:5;"></svg>
            <div class="canvas-inner" id="canvasInner"></div>
        </div>
    </div>
</div>

<!-- 新建模态框 -->
<div class="modal fade" id="newModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title"><i class="bi bi-plus-circle me-2"></i>新建工作流</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
    <div class="modal-body"><div class="row g-3">
        <div class="col-6"><div class="new-type-card" onclick="newWorkflow()"><i class="bi bi-diagram-3 text-primary"></i><h6>空白工作流</h6><small>拖拽创建</small></div></div>
        <div class="col-6"><div class="new-type-card" onclick="showApiWizard()"><i class="bi bi-link-45deg text-success"></i><h6>快速API</h6><small>自动生成节点</small></div></div>
    </div></div>
</div></div></div>

<!-- API向导模态框 -->
<div class="modal fade" id="apiWizardModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title"><i class="bi bi-link-45deg me-2"></i>快速API配置</h5>
        <div class="modal-header-actions">
            <button type="button" class="modal-btn" onclick="showVarList()"><i class="bi bi-list-ul"></i> 变量</button>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
    </div>
    <div class="modal-body">
        <div class="row mb-3">
            <div class="col-md-5"><label class="form-label">名称 *</label><input type="text" class="form-control" id="wizardName"></div>
            <div class="col-md-5"><label class="form-label">触发内容 *</label><input type="text" class="form-control" id="wizardTrigger" placeholder="例如: 天气 (.+)"></div>
            <div class="col-md-2"><label class="form-label">触发类型</label><select class="form-select" id="wizardTriggerType"><option value="exact">完全匹配</option><option value="startswith">前缀</option><option value="contains">包含</option><option value="regex">正则</option></select></div>
        </div>
        <div class="row mb-3">
            <div class="col-md-8"><label class="form-label">API地址 *</label><input type="text" class="form-control" id="wizardApiUrl" placeholder="https://api.example.com/data?key={$1}"><small class="text-muted">支持变量: {$1} {user_id} {group_id} {message}</small></div>
            <div class="col-md-2"><label class="form-label">方法</label><select class="form-select" id="wizardApiMethod"><option value="GET">GET</option><option value="POST">POST</option></select></div>
            <div class="col-md-2"><label class="form-label">响应</label><select class="form-select" id="wizardResponseType" onchange="updateWizardReplyOptions()"><option value="json">JSON</option><option value="text">文本</option><option value="binary">二进制</option></select></div>
        </div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">回复类型</label>
                <select class="form-select" id="wizardReplyType" onchange="updateWizardReplyConfig()">
                    <option value="text">普通文本</option>
                    <option value="markdown">原生Markdown</option>
                    <option value="template_markdown">模板Markdown</option>
                    <option value="image">图片</option>
                    <option value="voice">语音</option>
                    <option value="video">视频</option>
                    <option value="ark">ARK卡片</option>
                </select>
            </div>
            <div class="col-md-6" id="wizardMdTemplateWrap" style="display:none;"><label class="form-label">模板ID</label><input type="text" class="form-control" id="wizardMdTemplate" placeholder="1"></div>
            <div class="col-md-6" id="wizardArkTypeWrap" style="display:none;">
                <label class="form-label">ARK类型</label>
                <select class="form-select" id="wizardArkType"><option value="23">列表(23)</option><option value="24">信息(24)</option><option value="37">通知(37)</option></select>
            </div>
        </div>
        <div class="mb-3" id="wizardReplyHint"></div>
        <div class="mb-3"><label class="form-label">回复模板</label><textarea class="form-control" id="wizardReply" rows="3" placeholder="示例: 查询结果: {data.result}"></textarea></div>
        <div class="mb-3" id="wizardImageTextWrap" style="display:none;"><label class="form-label">图片描述(可选)</label><input type="text" class="form-control" id="wizardImageText"></div>
        <div class="mb-3" id="wizardKeyboardWrap" style="display:none;"><label class="form-label">按钮ID(可选)</label><input type="text" class="form-control" id="wizardKeyboard"></div>
        <div class="mb-3"><a class="btn btn-sm btn-outline-secondary" data-bs-toggle="collapse" href="#wizardAdv"><i class="bi bi-gear me-1"></i>高级设置</a>
            <div class="collapse mt-2" id="wizardAdv"><div class="card card-body" style="border-radius:10px;">
                <div class="mb-3"><label class="form-label">请求头(JSON)</label><textarea class="form-control" id="wizardHeaders" rows="2"></textarea></div>
                <div class="mb-3"><label class="form-label">请求体(JSON)</label><textarea class="form-control" id="wizardBody" rows="2"></textarea></div>
            </div></div>
        </div>
        <button class="btn btn-success btn-sm" onclick="testWizardApi()"><i class="bi bi-play me-1"></i>测试API</button>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" onclick="generateFromApi()"><i class="bi bi-magic me-1"></i>生成工作流</button>
    </div>
</div></div></div>

<!-- 节点编辑模态框 -->
<div class="modal fade" id="nodeEditModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">
    <div class="modal-header">
        <h5 class="modal-title" id="nodeEditTitle">编辑节点</h5>
        <div class="modal-header-actions">
            <button type="button" class="modal-btn" onclick="showAiNodeModal()" id="btnAiNode"><i class="bi bi-stars"></i> AI填写</button>
            <button type="button" class="modal-btn" onclick="showVarList()"><i class="bi bi-list-ul"></i> 变量</button>
            <button type="button" class="modal-btn success" id="btnTestApi" style="display:none" onclick="testNodeApi()"><i class="bi bi-play"></i> 测试</button>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
    </div>
    <div class="modal-body" id="nodeEditBody"></div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" onclick="saveNodeEdit()">确定</button>
    </div>
</div></div></div>

<!-- AI填写节点模态框 -->
<div class="modal fade" id="aiNodeModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title"><i class="bi bi-stars me-2"></i>AI填写节点</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
    <div class="modal-body">
        <div class="hint-box mb-3"><i class="bi bi-info-circle me-1"></i>描述你想要这个节点做什么，AI会自动填写配置</div>
        <div class="mb-3"><label class="form-label">AI模型</label><select class="form-select" id="aiNodeModel"><option>加载中...</option></select></div>
        <div class="mb-3"><label class="form-label">描述需求</label><textarea class="form-control" id="aiNodeDesc" rows="4" placeholder="例如：&#10;- 触发器：当用户发送 签到 时触发&#10;- 条件：判断今天是否已签到&#10;- 动作：调用天气API并回复结果&#10;- 存储：给用户积分加10"></textarea></div>
        <div id="aiNodeExamples" class="small text-muted"></div>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" id="aiNodeBtn" onclick="aiNodeGenerate()"><i class="bi bi-stars me-1"></i>生成</button>
    </div>
</div></div></div>

<!-- AI生成模态框 -->
<div class="modal fade" id="aiModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title"><i class="bi bi-stars me-2"></i>AI生成工作流</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
    <div class="modal-body">
        <div class="mb-3"><label class="form-label">AI模型</label><select class="form-select" id="aiModel"><option>加载中...</option></select></div>
        <div class="mb-3"><label class="form-label">描述工作流</label><textarea class="form-control" id="aiDescription" rows="5" placeholder="示例: 当用户发送 天气+城市名 时，调用天气API获取天气信息并回复"></textarea></div>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" id="aiGenerateBtn" onclick="aiGenerate()"><i class="bi bi-stars me-1"></i>生成</button>
    </div>
</div></div></div>

<!-- 变量列表模态框 -->
<div class="modal fade" id="varListModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title"><i class="bi bi-code-square me-2"></i>可用变量列表</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
    <div class="modal-body"><div class="row">
        <div class="col-md-6">
            <h6 class="text-primary border-bottom pb-2 mb-3"><i class="bi bi-braces me-1"></i>JSON数据变量</h6>
            <table class="table table-sm var-table">
                <tbody>
                    <tr><td><code>{data.xxx}</code></td><td>JSON路径</td></tr>
                    <tr><td><code>{data.items[0].name}</code></td><td>数组访问</td></tr>
                    <tr><td><code>{api_response}</code></td><td>原始响应</td></tr>
                    <tr><td><code>{api_status}</code></td><td>HTTP状态码</td></tr>
                </tbody>
            </table>
            <h6 class="text-success border-bottom pb-2 mb-3 mt-4"><i class="bi bi-regex me-1"></i>正则捕获组</h6>
            <table class="table table-sm var-table">
                <tbody>
                    <tr><td><code>{$1}</code> <code>{$2}</code></td><td>第N个捕获组</td></tr>
                </tbody>
            </table>
            <h6 class="text-warning border-bottom pb-2 mb-3 mt-4"><i class="bi bi-person me-1"></i>用户变量</h6>
            <table class="table table-sm var-table">
                <tbody>
                    <tr><td><code>{user_id}</code></td><td>用户ID</td></tr>
                    <tr><td><code>{group_id}</code></td><td>群组ID</td></tr>
                    <tr><td><code>{message}</code></td><td>原始消息</td></tr>
                    <tr><td><code>{at_user}</code></td><td>@用户</td></tr>
                </tbody>
            </table>
        </div>
        <div class="col-md-6">
            <h6 class="text-info border-bottom pb-2 mb-3"><i class="bi bi-clock me-1"></i>时间变量</h6>
            <table class="table table-sm var-table">
                <tbody>
                    <tr><td><code>{today}</code></td><td>今日日期YYYY-MM-DD</td></tr>
                    <tr><td><code>{timestamp}</code></td><td>时间戳</td></tr>
                    <tr><td><code>{hour}</code> <code>{minute}</code></td><td>时/分</td></tr>
                    <tr><td><code>{weekday_cn}</code></td><td>周一~周日</td></tr>
                    <tr><td><code>{random}</code> <code>{random6}</code></td><td>随机1-100/1-6</td></tr>
                </tbody>
            </table>
            <h6 class="text-danger border-bottom pb-2 mb-3 mt-4"><i class="bi bi-database me-1"></i>存储/运算结果</h6>
            <table class="table table-sm var-table">
                <tbody>
                    <tr><td><code>{storage.键名}</code></td><td>直接读取用户存储</td></tr>
                    <tr><td><code>{data_result}</code></td><td>用户存储节点结果</td></tr>
                    <tr><td><code>{global_result}</code></td><td>全局存储节点结果</td></tr>
                    <tr><td><code>{math_result}</code></td><td>数学运算结果</td></tr>
                    <tr><td><code>{string_result}</code></td><td>字符串操作结果</td></tr>
                    <tr><td><code>{list_result}</code></td><td>随机抽取结果</td></tr>
                    <tr><td><code>{leaderboard}</code></td><td>排行榜文本</td></tr>
                    <tr><td><code>{my_rank}</code> <code>{my_value}</code></td><td>我的排名/分数</td></tr>
                </tbody>
            </table>
        </div>
    </div></div>
    <div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button></div>
</div></div></div>

<!-- API测试模态框 -->
<div class="modal fade" id="apiTestModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content">
    <div class="modal-header"><h5 class="modal-title"><i class="bi bi-lightning me-2"></i>API测试结果</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
    <div class="modal-body">
        <div class="mb-3"><strong>状态码:</strong> <span id="apiTestStatus" class="badge bg-success"></span></div>
        <div class="mb-3"><strong>点击JSON字段复制变量路径:</strong></div>
        <div id="selectedPaths" class="mb-2"></div>
        <pre id="json-tree" style="background:#f8fafc;padding:1rem;border-radius:10px;max-height:400px;overflow:auto;font-size:0.85rem;border:1px solid #e2e8f0;"></pre>
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-outline-secondary btn-sm" onclick="document.getElementById('selectedPaths').innerHTML=''">清空选择</button>
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
    </div>
</div></div></div>
'''


def get_script():
    """获取JavaScript"""
    return '''
var nodes = {}, connections = [], nodeIdCounter = 0, editingNodeId = null, currentWorkflow = null, draggingNode = null, connecting = null;
var newModal, apiWizardModal, nodeEditModal, aiModal, varListModal, apiTestModal, aiNodeModal;

var NODE_EXAMPLES = {
    trigger: '当用户发送"签到"时触发',
    condition: '判断用户今天是否已经签到过',
    action: '调用天气API查询北京天气并回复用户',
    storage: '给用户的积分加10分',
    global_storage: '将全局活动计数器加1',
    leaderboard: '获取积分排行榜前10名',
    list_random: '从奖池中随机抽取一个奖品：金币x10、金币x50、钻石x1',
    delay: '等待3秒后继续',
    set_var: '将用户输入的第一个参数保存为城市名变量',
    comment: '这是签到功能的主流程'
};

var REPLY_TYPE_HINTS = {
    text: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>普通文本，支持变量如<code>{data.xxx}</code></div>',
    markdown: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>原生Markdown，需填写模板ID，使用<code>{{xxx}}</code>格式</div>',
    template_markdown: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>模板Markdown，需填写模板ID和按钮ID(可选)</div>',
    image: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>图片URL，支持<code>{data.url}</code>或<code>{api_response}</code></div>',
    voice: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>语音URL</div>',
    video: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>视频URL</div>',
    ark: '<div class="hint-box"><i class="bi bi-info-circle me-1"></i>ARK卡片，回复内容填JSON格式</div>'
};

var NODE_CONFIGS = {
    trigger: { title: '触发器', icon: 'bi-lightning', color: 'success', inputs: 0, outputs: 1, fields: [{name: 'trigger_type', label: '触发类型', type: 'select', options: [{value:'exact',label:'完全匹配'},{value:'startswith',label:'前缀匹配'},{value:'contains',label:'包含匹配'},{value:'regex',label:'正则匹配'}]},{name: 'trigger_content', label: '触发内容', type: 'text', placeholder: '正则示例: 天气 (.+)'}]},
    condition: { title: '条件', icon: 'bi-signpost-split', color: 'warning', inputs: 1, outputs: 2, fields: [{name: 'condition_type', label: '条件类型', type: 'select', options: [{value:'contains',label:'内容包含'},{value:'equals',label:'内容等于'},{value:'regex',label:'正则匹配'},{value:'random',label:'随机概率%'},{value:'user_id',label:'用户ID等于'},{value:'group_id',label:'群ID等于'},{value:'var_equals',label:'变量等于'},{value:'var_gt',label:'变量大于'},{value:'var_lt',label:'变量小于'},{value:'data_equals',label:'存储等于'},{value:'data_gt',label:'存储大于'},{value:'data_lt',label:'存储小于'},{value:'data_is_today',label:'今日已操作'},{value:'cooldown',label:'冷却时间'},{value:'time_range',label:'时间范围'},{value:'weekday_in',label:'星期几'},{value:'global_equals',label:'全局存储等于'},{value:'global_gt',label:'全局存储大于'},{value:'rank_top',label:'排行前N'},{value:'content_regex',label:'内容正则'},{value:'content_length',label:'内容长度'},{value:'is_number',label:'是否数字'},{value:'expression',label:'表达式'}]},{name: 'condition_value', label: '条件值', type: 'text', placeholder: '根据类型填写'},{name: 'var_name', label: '变量名(变量类型用)', type: 'text'}]},
    action: { title: '动作', icon: 'bi-play-circle', color: 'primary', inputs: 1, outputs: 1, customEdit: true },
    storage: { title: '用户存储', icon: 'bi-database', color: 'danger', inputs: 1, outputs: 1, fields: [{name: 'storage_type', label: '操作', type: 'select', options: [{value:'get',label:'读取'},{value:'set',label:'写入'},{value:'incr',label:'增加'},{value:'decr',label:'减少'},{value:'delete',label:'删除'}]},{name: 'storage_key', label: '键名', type: 'text', placeholder: 'score'},{name: 'storage_value', label: '值', type: 'text'},{name: 'default_value', label: '默认值', type: 'text', placeholder: '0'},{name: 'result_var', label: '结果变量', type: 'text', placeholder: 'data_result'}]},
    list_random: { title: '随机抽取', icon: 'bi-shuffle', color: 'danger', inputs: 1, outputs: 1, fields: [{name: 'list_items', label: '列表(|分隔)', type: 'textarea', placeholder: '金币x10|金币x50|钻石x1'},{name: 'weights', label: '权重(可选)', type: 'text', placeholder: '70|20|10'},{name: 'result_var', label: '结果变量', type: 'text', placeholder: 'list_result'},{name: 'index_var', label: '索引变量', type: 'text', placeholder: 'list_index'}]},
    global_storage: { title: '全局存储', icon: 'bi-globe', color: 'primary', inputs: 1, outputs: 1, fields: [{name: 'storage_type', label: '操作', type: 'select', options: [{value:'get',label:'读取'},{value:'set',label:'写入'},{value:'incr',label:'增加'},{value:'decr',label:'减少'}]},{name: 'storage_key', label: '键名', type: 'text'},{name: 'storage_value', label: '值', type: 'text'},{name: 'default_value', label: '默认值', type: 'text', placeholder: '0'},{name: 'result_var', label: '结果变量', type: 'text', placeholder: 'global_result'}]},
    leaderboard: { title: '排行榜', icon: 'bi-trophy', color: 'warning', inputs: 1, outputs: 1, fields: [{name: 'leaderboard_type', label: '操作', type: 'select', options: [{value:'top',label:'获取排行榜'},{value:'my_rank',label:'我的排名'},{value:'count',label:'统计人数'}]},{name: 'leaderboard_key', label: '排行键名', type: 'text', placeholder: 'score'},{name: 'limit', label: 'TOP数量', type: 'number', default: 10},{name: 'ascending', label: '排序', type: 'select', options: [{value:'false',label:'降序(大在前)'},{value:'true',label:'升序(小在前)'}]}]},
    delay: { title: '延时', icon: 'bi-clock', color: 'secondary', inputs: 1, outputs: 1, fields: [{name: 'seconds', label: '等待秒数', type: 'number', default: 1}]},
    set_var: { title: '变量', icon: 'bi-braces', color: 'info', inputs: 1, outputs: 1, fields: [{name: 'var_name', label: '变量名', type: 'text'},{name: 'var_value', label: '变量值', type: 'text', placeholder: '支持{$1}等'}]},
    comment: { title: '注释', icon: 'bi-chat-quote', color: 'secondary', inputs: 0, outputs: 0, fields: [{name: 'comment_text', label: '备注内容', type: 'textarea', placeholder: '流程说明...'}]}
};

function initCanvas() {
    var canvas = document.getElementById('canvasInner');
    if (!canvas) return;
    document.querySelectorAll('.node-palette-item').forEach(function(item) {
        item.addEventListener('dragstart', function(e) { e.dataTransfer.setData('nodeType', item.dataset.type); });
    });
    canvas.addEventListener('dragover', function(e) { e.preventDefault(); });
    canvas.addEventListener('drop', function(e) {
        e.preventDefault();
        var type = e.dataTransfer.getData('nodeType');
        if (type) {
            var rect = canvas.getBoundingClientRect();
            createNode(type, e.clientX - rect.left + canvas.parentElement.scrollLeft, e.clientY - rect.top + canvas.parentElement.scrollTop);
        }
    });
    canvas.addEventListener('mousedown', function(e) { if (e.target === canvas) deselectAll(); });
}

function createNode(type, x, y) {
    var id = 'node_' + (++nodeIdCounter);
    var config = NODE_CONFIGS[type];
    if (!config) { showToast('未知节点类型', 'error'); return; }
    nodes[id] = { id: id, type: type, x: x, y: y, data: {} };
    if (config.fields) config.fields.forEach(function(f) { if (f.default !== undefined) nodes[id].data[f.name] = f.default; });
    renderNode(id);
    return id;
}

function renderNode(id) {
    var node = nodes[id], config = NODE_CONFIGS[node.type];
    if (!config) return;
    var el = document.createElement('div');
    el.className = 'workflow-node ' + node.type;
    el.id = id;
    el.style.left = node.x + 'px';
    el.style.top = node.y + 'px';
    var summary = getNodeSummary(node);
    el.innerHTML = '<button class="btn-delete-node" onclick="deleteNode(\\'' + id + '\\')"><i class="bi bi-x"></i></button>' +
        '<div class="node-header"><i class="bi ' + config.icon + '"></i>' + config.title + '</div>' +
        '<div class="node-body">' + summary + '</div>' +
        (config.inputs > 0 ? '<div class="node-port input" data-node="' + id + '" data-port="input"></div>' : '') +
        (config.outputs === 1 ? '<div class="node-port output" data-node="' + id + '" data-port="output"></div>' : '') +
        (config.outputs === 2 ? '<div class="node-port output output-1" data-node="' + id + '" data-port="output-1"></div><div class="node-port output output-2" data-node="' + id + '" data-port="output-2"></div>' : '');
    el.addEventListener('mousedown', function(e) { if (!e.target.classList.contains('node-port') && !e.target.classList.contains('btn-delete-node')) startDrag(e, id); });
    el.addEventListener('dblclick', function() { editNode(id); });
    el.querySelectorAll('.node-port').forEach(function(port) {
        port.addEventListener('mousedown', function(e) { e.stopPropagation(); startConnect(e, id, port.dataset.port); });
        port.addEventListener('click', function(e) { e.stopPropagation(); handlePortClick(id, port.dataset.port); });
    });
    var old = document.getElementById(id);
    if (old) old.remove();
    document.getElementById('canvasInner').appendChild(el);
}

function getNodeSummary(node) {
    var d = node.data;
    if (node.type === 'trigger') return (d.trigger_content || '未设置').substring(0, 20);
    if (node.type === 'condition') return (d.condition_type || 'contains') + ': ' + (d.condition_value || '').substring(0, 15);
    if (node.type === 'action') return d.action_type === 'custom_api' ? 'API: ' + (d.api_url || '').substring(0, 20) : (d.action_type || 'reply_text');
    if (node.type === 'storage' || node.type === 'global_storage') return (d.storage_type || 'get') + ': ' + (d.storage_key || '');
    if (node.type === 'leaderboard') return (d.leaderboard_type || 'top') + ': ' + (d.leaderboard_key || '');
    if (node.type === 'delay') return (d.seconds || 1) + '秒';
    if (node.type === 'set_var') return (d.var_name || '') + '=' + (d.var_value || '').substring(0, 10);
    if (node.type === 'list_random') return '随机: ' + (d.list_items || '').substring(0, 15);
    if (node.type === 'comment') return (d.comment_text || '').substring(0, 20);
    return '';
}

function startDrag(e, id) {
    e.preventDefault();
    deselectAll();
    var node = nodes[id], el = document.getElementById(id);
    el.classList.add('selected');
    draggingNode = { id: id, offsetX: e.clientX - node.x, offsetY: e.clientY - node.y };
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
}

function onDrag(e) {
    if (!draggingNode) return;
    var node = nodes[draggingNode.id];
    node.x = Math.max(0, e.clientX - draggingNode.offsetX);
    node.y = Math.max(0, e.clientY - draggingNode.offsetY);
    var el = document.getElementById(draggingNode.id);
    el.style.left = node.x + 'px';
    el.style.top = node.y + 'px';
    renderConnections();
}

function stopDrag() {
    draggingNode = null;
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);
}

function startConnect(e, nodeId, port) {
    connecting = { from: nodeId, port: port };
    document.addEventListener('mouseup', stopConnect);
}

function stopConnect(e) {
    document.removeEventListener('mouseup', stopConnect);
    if (!connecting) return;
    var target = e.target;
    if (target.classList.contains('node-port') && target.dataset.port === 'input') {
        var toNode = target.dataset.node;
        if (toNode !== connecting.from) {
            connections = connections.filter(function(c) { return !(c.from === connecting.from && c.port === connecting.port); });
            connections.push({ from: connecting.from, to: toNode, port: connecting.port });
            renderConnections();
        }
    }
    connecting = null;
}

function renderConnections() {
    var svg = document.getElementById('connectionsSvg');
    svg.innerHTML = '';
    console.log('[工作流] 渲染连接线, 数量:', connections.length, connections);
    connections.forEach(function(conn) {
        var fromEl = document.getElementById(conn.from), toEl = document.getElementById(conn.to);
        if (!fromEl || !toEl) { console.log('[工作流] 节点未找到:', conn.from, conn.to); return; }
        // 查找输出端口：先尝试精确匹配，再尝试通用output
        var portClass = conn.port === 'output' ? 'output' : conn.port;
        var fromPort = fromEl.querySelector('.node-port.' + portClass) || fromEl.querySelector('.node-port.output');
        var toPort = toEl.querySelector('.node-port.input');
        if (!fromPort || !toPort) { console.log('[工作流] 端口未找到:', portClass, fromPort, toPort); return; }
        var x1 = fromEl.offsetLeft + fromPort.offsetLeft + 6, y1 = fromEl.offsetTop + fromPort.offsetTop + 6;
        var x2 = toEl.offsetLeft + toPort.offsetLeft + 6, y2 = toEl.offsetTop + toPort.offsetTop + 6;
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        var midX = (x1 + x2) / 2;
        path.setAttribute('d', 'M' + x1 + ',' + y1 + ' C' + midX + ',' + y1 + ' ' + midX + ',' + y2 + ' ' + x2 + ',' + y2);
        path.setAttribute('class', 'connection-line');
        if (conn.port === 'output-2') path.style.stroke = '#ef4444';
        svg.appendChild(path);
    });
}

// 点击连接模式
var clickConnectMode = null; // {from: nodeId, port: portName}

function handlePortClick(nodeId, portType) {
    if (portType === 'input') {
        // 点击输入端口 - 如果有等待连接，则建立连接
        if (clickConnectMode) {
            if (clickConnectMode.from !== nodeId) {
                connections = connections.filter(function(c) { return !(c.from === clickConnectMode.from && c.port === clickConnectMode.port); });
                connections.push({ from: clickConnectMode.from, to: nodeId, port: clickConnectMode.port });
                renderConnections();
                showToast('连接成功', 'success');
            }
            clickConnectMode = null;
            document.querySelectorAll('.node-port.waiting').forEach(function(p) { p.classList.remove('waiting'); });
        }
    } else {
        // 点击输出端口 - 进入等待连接模式
        document.querySelectorAll('.node-port.waiting').forEach(function(p) { p.classList.remove('waiting'); });
        var el = document.getElementById(nodeId);
        var port = el.querySelector('.node-port[data-port="' + portType + '"]');
        if (port) {
            port.classList.add('waiting');
            clickConnectMode = { from: nodeId, port: portType === 'output' ? 'output' : portType };
            showToast('请点击目标节点的输入端口', 'info');
        }
    }
}

function deleteNode(id) {
    var el = document.getElementById(id);
    if (el) el.remove();
    delete nodes[id];
    connections = connections.filter(function(c) { return c.from !== id && c.to !== id; });
    renderConnections();
}

function deselectAll() { document.querySelectorAll('.workflow-node.selected').forEach(function(el) { el.classList.remove('selected'); }); }

function editNode(id) {
    editingNodeId = id;
    var node = nodes[id], config = NODE_CONFIGS[node.type];
    if (!config) return;
    var html = '';
    if (config.customEdit && node.type === 'action') {
        html = buildActionEditForm(node.data);
    } else if (config.fields) {
        config.fields.forEach(function(f) {
            var value = node.data[f.name] !== undefined ? node.data[f.name] : (f.default || '');
            html += '<div class="mb-3"><label class="form-label">' + f.label + '</label>';
            if (f.type === 'select') {
                html += '<select class="form-select" id="field_' + f.name + '">';
                f.options.forEach(function(o) { html += '<option value="' + o.value + '"' + (value === o.value ? ' selected' : '') + '>' + o.label + '</option>'; });
                html += '</select>';
            } else if (f.type === 'textarea') {
                html += '<textarea class="form-control" id="field_' + f.name + '" rows="3">' + value + '</textarea>';
            } else {
                html += '<input type="' + (f.type || 'text') + '" class="form-control" id="field_' + f.name + '" value="' + value + '"' + (f.placeholder ? ' placeholder="' + f.placeholder + '"' : '') + '>';
            }
            html += '</div>';
        });
    }
    document.getElementById('nodeEditBody').innerHTML = html;
    document.getElementById('nodeEditTitle').textContent = '编辑' + config.title;
    var btnTest = document.getElementById('btnTestApi');
    if (btnTest) btnTest.style.display = (node.type === 'action' && node.data.action_type === 'custom_api') ? '' : 'none';
    if (nodeEditModal) nodeEditModal.show();
}

function buildActionEditForm(data) {
    var actionType = data.action_type || 'reply_text';
    var html = '<div class="row mb-3"><div class="col-md-6"><label class="form-label">动作类型</label><select class="form-select" id="field_action_type" onchange="updateNodeActionType()">';
    html += '<optgroup label="回复消息">';
    html += '<option value="reply_text"' + (actionType === 'reply_text' ? ' selected' : '') + '>回复文字</option>';
    html += '<option value="reply_image"' + (actionType === 'reply_image' ? ' selected' : '') + '>图片</option>';
    html += '<option value="reply_voice"' + (actionType === 'reply_voice' ? ' selected' : '') + '>语音</option>';
    html += '<option value="reply_video"' + (actionType === 'reply_video' ? ' selected' : '') + '>视频</option>';
    html += '<option value="reply_markdown"' + (actionType === 'reply_markdown' ? ' selected' : '') + '>Markdown</option>';
    html += '<option value="reply_markdown_aj"' + (actionType === 'reply_markdown_aj' ? ' selected' : '') + '>AJ Markdown</option>';
    html += '</optgroup><optgroup label="数据操作">';
    html += '<option value="custom_api"' + (actionType === 'custom_api' ? ' selected' : '') + '>调用API</option>';
    html += '<option value="math"' + (actionType === 'math' ? ' selected' : '') + '>数学运算</option>';
    html += '<option value="string_op"' + (actionType === 'string_op' ? ' selected' : '') + '>字符串操作</option>';
    html += '</optgroup></select></div></div>';
    html += '<div id="actionFieldsContainer">';
    html += getActionFieldsHtml(actionType, data);
    html += '</div>';
    return html;
}

function getActionFieldsHtml(actionType, data) {
    var html = '';
    data = data || {};
    if (actionType === 'custom_api') {
        html += '<div class="row mb-3"><div class="col-md-8"><label class="form-label">API地址 *</label><input type="text" class="form-control" id="field_api_url" value="' + (data.api_url || '') + '" placeholder="https://api.example.com/data?key={$1}"><small class="text-muted">支持变量: {$1} {user_id} {group_id}</small></div>';
        html += '<div class="col-md-2"><label class="form-label">方法</label><select class="form-select" id="field_api_method"><option value="GET"' + (data.api_method === 'GET' || !data.api_method ? ' selected' : '') + '>GET</option><option value="POST"' + (data.api_method === 'POST' ? ' selected' : '') + '>POST</option></select></div>';
        html += '<div class="col-md-2"><label class="form-label">响应</label><select class="form-select" id="field_response_type" onchange="updateNodeReplyOptions()"><option value="json"' + (data.response_type === 'json' || !data.response_type ? ' selected' : '') + '>JSON</option><option value="text"' + (data.response_type === 'text' ? ' selected' : '') + '>文本</option><option value="binary"' + (data.response_type === 'binary' ? ' selected' : '') + '>二进制</option></select></div></div>';
        var rt = data.reply_type || 'text';
        html += '<div class="row mb-3"><div class="col-md-6"><label class="form-label">回复类型</label><select class="form-select" id="field_reply_type" onchange="updateNodeReplyOptions()"><option value="text"' + (rt === 'text' ? ' selected' : '') + '>文本</option><option value="markdown"' + (rt === 'markdown' ? ' selected' : '') + '>原生MD</option><option value="template_markdown"' + (rt === 'template_markdown' ? ' selected' : '') + '>模板MD</option><option value="image"' + (rt === 'image' ? ' selected' : '') + '>图片</option></select></div><div class="col-md-6" id="nodeReplyExtra"></div></div>';
        html += '<div class="mb-3"><label class="form-label">回复模板</label><textarea class="form-control" id="field_api_reply" rows="3" placeholder="{data.result}">' + (data.api_reply || '') + '</textarea></div>';
        html += '<div id="nodeImageTextWrap" style="display:' + (rt === 'image' ? 'block' : 'none') + ';"><div class="mb-3"><label class="form-label">图片描述</label><input type="text" class="form-control" id="field_image_text" value="' + (data.image_text || '') + '"></div></div>';
        html += '<div id="nodeKeyboardWrap" style="display:' + (rt === 'template_markdown' ? 'block' : 'none') + ';"><div class="mb-3"><label class="form-label">按钮ID</label><input type="text" class="form-control" id="field_keyboard_id" value="' + (data.keyboard_id || '') + '"></div></div>';
        html += '<div class="mb-3"><a class="btn btn-sm btn-outline-secondary" data-bs-toggle="collapse" href="#nodeAdvSettings"><i class="bi bi-gear me-1"></i>高级设置</a><div class="collapse mt-2" id="nodeAdvSettings"><div class="card card-body" style="border-radius:10px;">';
        html += '<div class="mb-3"><label class="form-label">请求头(JSON)</label><textarea class="form-control" id="field_api_headers" rows="2">' + (data.api_headers || '') + '</textarea></div>';
        html += '<div class="mb-3"><label class="form-label">请求体(JSON)</label><textarea class="form-control" id="field_api_body" rows="2">' + (data.api_body || '') + '</textarea></div>';
        html += '</div></div></div>';
    } else if (actionType === 'math') {
        html += '<div class="row mb-3"><div class="col-md-4"><label class="form-label">运算类型</label><select class="form-select" id="field_math_type">';
        var mathOpts = [{v:'add',l:'加(+)'},{v:'sub',l:'减(-)'},{v:'mul',l:'乘(*)'},{v:'div',l:'除(/)'},{v:'mod',l:'取余(%)'},{v:'pow',l:'幂(^)'},{v:'min',l:'最小值'},{v:'max',l:'最大值'},{v:'random',l:'随机(范围)'}];
        mathOpts.forEach(function(o) { html += '<option value="' + o.v + '"' + (data.math_type === o.v ? ' selected' : '') + '>' + o.l + '</option>'; });
        html += '</select></div>';
        html += '<div class="col-md-4"><label class="form-label">操作数1</label><input type="text" class="form-control" id="field_operand1" value="' + (data.operand1 || '') + '" placeholder="数字或{变量}"></div>';
        html += '<div class="col-md-4"><label class="form-label">操作数2</label><input type="text" class="form-control" id="field_operand2" value="' + (data.operand2 || '') + '" placeholder="数字或{变量}"></div></div>';
        html += '<div class="mb-3"><label class="form-label">结果变量名</label><input type="text" class="form-control" id="field_result_var" value="' + (data.result_var || 'math_result') + '"></div>';
    } else if (actionType === 'string_op') {
        html += '<div class="row mb-3"><div class="col-md-4"><label class="form-label">操作类型</label><select class="form-select" id="field_string_type">';
        var strOpts = [{v:'concat',l:'拼接'},{v:'replace',l:'替换'},{v:'split',l:'分割'},{v:'substr',l:'截取'},{v:'length',l:'长度'},{v:'upper',l:'大写'},{v:'lower',l:'小写'},{v:'trim',l:'去空格'},{v:'contains',l:'包含检测'},{v:'repeat',l:'重复'}];
        strOpts.forEach(function(o) { html += '<option value="' + o.v + '"' + (data.string_type === o.v ? ' selected' : '') + '>' + o.l + '</option>'; });
        html += '</select></div>';
        html += '<div class="col-md-4"><label class="form-label">输入1</label><input type="text" class="form-control" id="field_input1" value="' + (data.input1 || '') + '" placeholder="字符串或{变量}"></div>';
        html += '<div class="col-md-4"><label class="form-label">输入2/分隔符</label><input type="text" class="form-control" id="field_input2" value="' + (data.input2 || '') + '"></div></div>';
        html += '<div class="mb-3"><label class="form-label">结果变量名</label><input type="text" class="form-control" id="field_result_var" value="' + (data.result_var || 'string_result') + '"></div>';
    } else {
        var placeholder = '消息内容，支持变量';
        if (actionType === 'reply_text') placeholder = '多个回复用 ||| 分隔可随机选择';
        else if (actionType === 'reply_image' || actionType === 'reply_voice' || actionType === 'reply_video') placeholder = '媒体URL，支持变量';
        html += '<div class="mb-3"><label class="form-label">内容</label><textarea class="form-control" id="field_action_value" rows="4" placeholder="' + placeholder + '">' + (data.action_value || '') + '</textarea></div>';
        if (actionType === 'reply_markdown') {
            html += '<div class="row mb-3"><div class="col-md-6"><label class="form-label">模板ID</label><input type="text" class="form-control" id="field_template_id" value="' + (data.template_id || '') + '"></div>';
            html += '<div class="col-md-6"><label class="form-label">按钮ID(可选)</label><input type="text" class="form-control" id="field_keyboard_id" value="' + (data.keyboard_id || '') + '"></div></div>';
        } else if (actionType === 'reply_markdown_aj') {
            html += '<div class="mb-3"><label class="form-label">按钮ID(可选)</label><input type="text" class="form-control" id="field_keyboard_id" value="' + (data.keyboard_id || '') + '"></div>';
        }
    }
    return html;
}

window.updateNodeActionType = function() {
    var select = document.getElementById('field_action_type');
    if (!select) return;
    var actionType = select.value;
    var node = nodes[editingNodeId];
    if (!node) return;
    var container = document.getElementById('actionFieldsContainer');
    if (container) container.innerHTML = getActionFieldsHtml(actionType, node.data);
    var btnTest = document.getElementById('btnTestApi');
    if (btnTest) btnTest.style.display = (actionType === 'custom_api') ? '' : 'none';
};

window.updateNodeReplyOptions = function() {
    var rtEl = document.getElementById('field_reply_type');
    if (!rtEl) return;
    var rt = rtEl.value;
    var extraEl = document.getElementById('nodeReplyExtra');
    if (extraEl) {
        if (rt === 'template_markdown') {
            var oldVal = (document.getElementById('field_markdown_template') || {}).value || '';
            extraEl.innerHTML = '<label class="form-label">模板ID</label><input type="text" class="form-control" id="field_markdown_template" value="' + oldVal + '">';
        } else if (rt === 'ark') {
            var oldArkVal = (document.getElementById('field_ark_type') || {}).value || '23';
            extraEl.innerHTML = '<label class="form-label">ARK类型</label><select class="form-select" id="field_ark_type"><option value="23"' + (oldArkVal === '23' ? ' selected' : '') + '>列表(23)</option><option value="24"' + (oldArkVal === '24' ? ' selected' : '') + '>信息(24)</option></select>';
        } else {
            extraEl.innerHTML = '';
        }
    }
    var imageWrap = document.getElementById('nodeImageTextWrap');
    if (imageWrap) imageWrap.style.display = (rt === 'image') ? 'block' : 'none';
    var kbWrap = document.getElementById('nodeKeyboardWrap');
    if (kbWrap) kbWrap.style.display = (rt === 'template_markdown') ? 'block' : 'none';
};

window.saveNodeEdit = function() {
    var node = nodes[editingNodeId];
    if (!node) return;
    if (node.type === 'action') {
        var at = document.getElementById('field_action_type');
        if (at) node.data.action_type = at.value;
        ['action_value', 'template_id', 'keyboard_id', 'api_url', 'api_method', 'response_type', 'reply_type', 'api_headers', 'api_body', 'api_reply', 'image_text', 'markdown_template', 'ark_type', 'math_type', 'operand1', 'operand2', 'string_type', 'input1', 'input2', 'result_var'].forEach(function(fn) {
            var el = document.getElementById('field_' + fn);
            if (el) node.data[fn] = el.value;
        });
    } else {
        var config = NODE_CONFIGS[node.type];
        if (config && config.fields) {
            config.fields.forEach(function(f) {
                var el = document.getElementById('field_' + f.name);
                if (el) node.data[f.name] = el.value;
            });
        }
    }
    renderNode(editingNodeId);
    renderConnections();
    if (nodeEditModal) nodeEditModal.hide();
};

window.showNewModal = function() { if (newModal) newModal.show(); };
window.showAiModal = function() { loadAiModels(); if (aiModal) aiModal.show(); };
window.showVarList = function() { if (varListModal) varListModal.show(); };

window.showApiWizard = function() {
    if (newModal) newModal.hide();
    setTimeout(function() { if (apiWizardModal) apiWizardModal.show(); }, 300);
};

window.newWorkflow = function() {
    if (newModal) newModal.hide();
    currentWorkflow = null;
    nodes = {}; connections = []; nodeIdCounter = 0;
    document.getElementById('canvasInner').innerHTML = '';
    document.getElementById('connectionsSvg').innerHTML = '';
    document.querySelectorAll('.workflow-list-item').forEach(function(el) { el.classList.remove('active'); });
    var triggerId = createNode('trigger', 100, 100);
    var actionId = createNode('action', 400, 100);
    connections.push({ from: triggerId, to: actionId, port: 'output' });
    renderConnections();
};

function loadWorkflows() {
    fetch('/web/api/plugin/workflow/list?token=' + getToken()).then(function(r) { return r.json(); }).then(function(data) {
        if (data.success) renderWorkflowList(data.workflows || []);
    });
}

function renderWorkflowList(workflows) {
    var container = document.getElementById('workflowList');
    if (!container) return;
    if (workflows.length === 0) { container.innerHTML = '<div class="text-muted text-center py-3"><i class="bi bi-inbox"></i><br>暂无工作流</div>'; return; }
    var html = '';
    workflows.forEach(function(wf) {
        var isActive = currentWorkflow && currentWorkflow.id === wf.id;
        html += '<div class="workflow-list-item' + (isActive ? ' active' : '') + '" onclick="loadWorkflow(\\'' + wf.id + '\\')">';
        html += '<div class="wf-name">' + (wf.name || '未命名') + '</div>';
        html += '<div class="wf-trigger">' + (wf.trigger_type || 'regex') + ': ' + (wf.trigger_content || '').substring(0, 20) + '</div>';
        html += '<div class="wf-actions">';
        html += '<button class="wf-btn ' + (wf.enabled !== false ? 'toggle-on' : 'toggle-off') + '" onclick="event.stopPropagation();toggleWorkflow(\\'' + wf.id + '\\')">' + (wf.enabled !== false ? '启用' : '禁用') + '</button>';
        html += '<button class="wf-btn delete" onclick="event.stopPropagation();deleteWorkflow(\\'' + wf.id + '\\')"><i class="bi bi-trash"></i></button>';
        html += '</div></div>';
    });
    container.innerHTML = html;
}

window.loadWorkflow = function(id) {
    fetch('/web/api/plugin/workflow/list?token=' + getToken()).then(function(r) { return r.json(); }).then(function(data) {
        if (!data.success) return;
        var wf = (data.workflows || []).find(function(w) { return w.id === id; });
        if (!wf) return;
        currentWorkflow = wf;
        nodes = {}; connections = []; nodeIdCounter = 0;
        document.getElementById('canvasInner').innerHTML = '';
        document.getElementById('connectionsSvg').innerHTML = '';
        if (wf.nodes) {
            // 兼容数组和对象两种格式
            var nodeList = Array.isArray(wf.nodes) ? wf.nodes : Object.values(wf.nodes);
            nodeList.forEach(function(n) {
                var numId = parseInt(n.id.replace('node_', '')) || 0;
                if (numId > nodeIdCounter) nodeIdCounter = numId;
                nodes[n.id] = n;
                renderNode(n.id);
            });
        }
        if (wf.connections) {
            // 转换格式兼容性
            connections = wf.connections.map(function(c) {
                return {
                    from: c.from_node || c.from,
                    to: c.to_node || c.to,
                    port: (c.from_output || c.port || 'output_1').replace('output_1', 'output')
                };
            });
            // 延迟渲染确保节点DOM已就绪
            setTimeout(function() { renderConnections(); }, 100);
        }
        document.querySelectorAll('.workflow-list-item').forEach(function(el) { el.classList.remove('active'); });
        document.querySelectorAll('.workflow-list-item').forEach(function(el) { if (el.onclick && el.onclick.toString().includes(id)) el.classList.add('active'); });
    });
};

window.saveWorkflow = function() {
    var triggerNode = Object.values(nodes).find(function(n) { return n.type === 'trigger'; });
    if (!triggerNode || !triggerNode.data.trigger_content) { showToast('请设置触发器', 'error'); return; }
    // 转换连接格式为后端格式
    var saveConnections = connections.map(function(c) {
        var portStr = c.port || 'output';
        return {
            from_node: c.from,
            from_output: portStr === 'output' ? 'output_1' : portStr,
            to_node: c.to
        };
    });
    var wfData = {
        id: currentWorkflow ? currentWorkflow.id : null,
        name: triggerNode.data.trigger_content.substring(0, 20),
        trigger_type: triggerNode.data.trigger_type || 'regex',
        trigger_content: triggerNode.data.trigger_content,
        enabled: currentWorkflow ? currentWorkflow.enabled : true,
        nodes: Object.values(nodes),
        connections: saveConnections
    };
    fetch('/web/api/plugin/workflow/save?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(wfData) })
    .then(function(r) { return r.json(); }).then(function(data) {
        if (data.success) { 
            showToast('保存成功', 'success'); 
            currentWorkflow = wfData; 
            // ID在data.data.id中
            if (data.data && data.data.id) currentWorkflow.id = data.data.id;
            else if (data.id) currentWorkflow.id = data.id;
            loadWorkflows(); 
        }
        else showToast(data.error || data.message || '保存失败', 'error');
    });
};

window.toggleWorkflow = function(id) {
    fetch('/web/api/plugin/workflow/toggle?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: id }) })
    .then(function(r) { return r.json(); }).then(function(data) {
        if (data.success) { showToast('状态已更新', 'success'); loadWorkflows(); }
        else showToast(data.error || '操作失败', 'error');
    });
};

window.deleteWorkflow = function(id) {
    if (!confirm('确定删除此工作流？')) return;
    fetch('/web/api/plugin/workflow/delete?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: id }) })
    .then(function(r) { return r.json(); }).then(function(data) {
        if (data.success) { showToast('已删除', 'success'); if (currentWorkflow && currentWorkflow.id === id) { currentWorkflow = null; nodes = {}; connections = []; document.getElementById('canvasInner').innerHTML = ''; document.getElementById('connectionsSvg').innerHTML = ''; } loadWorkflows(); }
        else showToast(data.error || '删除失败', 'error');
    });
};

function loadAiModels() {
    fetch('/web/api/plugin/workflow/ai_models?token=' + getToken()).then(function(r) { return r.json(); }).then(function(data) {
        var select = document.getElementById('aiModel');
        if (!select) return;
        select.innerHTML = '';
        if (data.success && data.models && data.models.length > 0) {
            data.models.forEach(function(m) { var opt = document.createElement('option'); opt.value = m; opt.textContent = m; select.appendChild(opt); });
        } else {
            select.innerHTML = '<option>无可用模型</option>';
        }
    });
}

window.aiGenerate = function() {
    var model = document.getElementById('aiModel').value;
    var desc = document.getElementById('aiDescription').value;
    if (!desc) { showToast('请输入描述', 'error'); return; }
    var btn = document.getElementById('aiGenerateBtn');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>生成中...';
    fetch('/web/api/plugin/workflow/ai_generate?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model: model, description: desc }) })
    .then(function(r) { return r.json(); }).then(function(data) {
        btn.disabled = false; btn.innerHTML = '<i class="bi bi-stars me-1"></i>生成';
        if (data.success && data.workflow) {
            if (aiModal) aiModal.hide();
            currentWorkflow = null; nodes = {}; connections = []; nodeIdCounter = 0;
            document.getElementById('canvasInner').innerHTML = '';
            document.getElementById('connectionsSvg').innerHTML = '';
            if (data.workflow.nodes) {
                // 兼容数组和对象两种格式
                var nodeList = Array.isArray(data.workflow.nodes) ? data.workflow.nodes : Object.values(data.workflow.nodes);
                nodeList.forEach(function(n) {
                    var numId = parseInt(n.id.replace('node_', '')) || 0;
                    if (numId > nodeIdCounter) nodeIdCounter = numId;
                    nodes[n.id] = n;
                    renderNode(n.id);
                });
            }
            if (data.workflow.connections) {
                // 转换AI格式 {from_node, from_output, to_node} 为前端格式 {from, to, port}
                connections = data.workflow.connections.map(function(c) {
                    return {
                        from: c.from_node || c.from,
                        to: c.to_node || c.to,
                        port: (c.from_output || c.port || 'output_1').replace('output_1', 'output')
                    };
                });
                console.log('[工作流] AI连接转换后:', connections);
                // 延迟渲染确保节点DOM已就绪
                setTimeout(function() { renderConnections(); }, 100);
            }
            showToast('生成成功，节点数: ' + Object.keys(nodes).length, 'success');
        } else { showToast(data.error || '生成失败', 'error'); }
    }).catch(function(e) { console.error('AI生成错误:', e); btn.disabled = false; btn.innerHTML = '<i class="bi bi-stars me-1"></i>生成'; showToast('请求失败', 'error'); });
};

window.showAiNodeModal = function() {
    if (!editingNodeId) return;
    var node = nodes[editingNodeId];
    if (!node) return;
    var config = NODE_CONFIGS[node.type];
    
    // 加载AI模型
    fetch('/web/api/plugin/workflow/ai_models?token=' + getToken()).then(function(r) { return r.json(); }).then(function(data) {
        var select = document.getElementById('aiNodeModel');
        if (!select) return;
        select.innerHTML = '';
        if (data.success && data.models && data.models.length > 0) {
            data.models.forEach(function(m) { var opt = document.createElement('option'); opt.value = m; opt.textContent = m; select.appendChild(opt); });
        } else {
            select.innerHTML = '<option>无可用模型</option>';
        }
    });
    
    // 显示示例
    var examples = document.getElementById('aiNodeExamples');
    if (examples) {
        examples.innerHTML = '<strong>示例：</strong>' + (NODE_EXAMPLES[node.type] || '描述这个节点需要做什么');
    }
    
    document.getElementById('aiNodeDesc').value = '';
    if (aiNodeModal) aiNodeModal.show();
};

window.aiNodeGenerate = function() {
    if (!editingNodeId) return;
    var node = nodes[editingNodeId];
    if (!node) return;
    
    var model = document.getElementById('aiNodeModel').value;
    var desc = document.getElementById('aiNodeDesc').value;
    if (!desc) { showToast('请输入描述', 'error'); return; }
    
    var btn = document.getElementById('aiNodeBtn');
    btn.disabled = true; btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>生成中...';
    
    fetch('/web/api/plugin/workflow/ai_node?token=' + getToken(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: model, node_type: node.type, description: desc, current_data: node.data })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        btn.disabled = false; btn.innerHTML = '<i class="bi bi-stars me-1"></i>生成';
        if (data.success && data.node_data) {
            // 更新节点数据
            Object.assign(node.data, data.node_data);
            // 关闭AI模态框
            if (aiNodeModal) aiNodeModal.hide();
            // 重新渲染编辑表单
            var config = NODE_CONFIGS[node.type];
            var html = '';
            if (config.customEdit && node.type === 'action') {
                html = buildActionEditForm(node.data);
            } else if (config.fields) {
                config.fields.forEach(function(f) {
                    var value = node.data[f.name] !== undefined ? node.data[f.name] : (f.default || '');
                    html += '<div class="mb-3"><label class="form-label">' + f.label + '</label>';
                    if (f.type === 'select') {
                        html += '<select class="form-select" id="field_' + f.name + '">';
                        f.options.forEach(function(o) { html += '<option value="' + o.value + '"' + (value === o.value ? ' selected' : '') + '>' + o.label + '</option>'; });
                        html += '</select>';
                    } else if (f.type === 'textarea') {
                        html += '<textarea class="form-control" id="field_' + f.name + '" rows="3">' + value + '</textarea>';
                    } else {
                        html += '<input type="' + (f.type || 'text') + '" class="form-control" id="field_' + f.name + '" value="' + value + '">';
                    }
                    html += '</div>';
                });
            }
            document.getElementById('nodeEditBody').innerHTML = html;
            var btnTest = document.getElementById('btnTestApi');
            if (btnTest) btnTest.style.display = (node.type === 'action' && node.data.action_type === 'custom_api') ? '' : 'none';
            showToast('AI已填写', 'success');
        } else {
            showToast(data.error || 'AI生成失败', 'error');
        }
    })
    .catch(function() {
        btn.disabled = false; btn.innerHTML = '<i class="bi bi-stars me-1"></i>生成';
        showToast('请求失败', 'error');
    });
};

window.updateWizardReplyOptions = function() {
    var rt = document.getElementById('wizardResponseType').value;
    var replyType = document.getElementById('wizardReplyType');
    if (rt === 'binary') { replyType.value = 'image'; replyType.disabled = true; }
    else { replyType.disabled = false; }
    updateWizardReplyConfig();
};

window.updateWizardReplyConfig = function() {
    var rt = document.getElementById('wizardReplyType').value;
    document.getElementById('wizardMdTemplateWrap').style.display = (rt === 'markdown' || rt === 'template_markdown') ? '' : 'none';
    document.getElementById('wizardArkTypeWrap').style.display = (rt === 'ark') ? '' : 'none';
    document.getElementById('wizardImageTextWrap').style.display = (rt === 'image') ? '' : 'none';
    document.getElementById('wizardKeyboardWrap').style.display = (rt === 'template_markdown') ? '' : 'none';
    var hint = document.getElementById('wizardReplyHint');
    if (hint) hint.innerHTML = REPLY_TYPE_HINTS[rt] || '';
};

window.testWizardApi = function() {
    var url = document.getElementById('wizardApiUrl').value;
    if (!url) { showToast('请输入API地址', 'error'); return; }
    var data = { url: url, method: document.getElementById('wizardApiMethod').value, headers: document.getElementById('wizardHeaders').value, body: document.getElementById('wizardBody').value };
    fetch('/web/api/plugin/workflow/test_api?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
    .then(function(r) { return r.json(); }).then(function(result) {
        if (result.success) { showApiTestResult(result); }
        else { showToast(result.error || '测试失败', 'error'); }
    });
};

window.testNodeApi = function() {
    var url = document.getElementById('field_api_url').value;
    if (!url) { showToast('请输入API地址', 'error'); return; }
    var data = { url: url, method: (document.getElementById('field_api_method') || {}).value || 'GET', headers: (document.getElementById('field_api_headers') || {}).value || '', body: (document.getElementById('field_api_body') || {}).value || '' };
    fetch('/web/api/plugin/workflow/test_api?token=' + getToken(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
    .then(function(r) { return r.json(); }).then(function(result) {
        if (result.success) { showApiTestResult(result); }
        else { showToast(result.error || '测试失败', 'error'); }
    });
};

function showApiTestResult(result) {
    document.getElementById('apiTestStatus').textContent = result.status_code;
    document.getElementById('apiTestStatus').className = 'badge ' + (result.status_code >= 200 && result.status_code < 300 ? 'bg-success' : 'bg-danger');
    var tree = document.getElementById('json-tree');
    document.getElementById('selectedPaths').innerHTML = '';
    if (result.is_json && result.json_data) {
        tree.innerHTML = renderJsonTree(result.json_data, 'data');
    } else if (result.is_binary) {
        tree.innerHTML = '<span class="text-muted">[二进制数据，可用 {api_response} 获取URL]</span>';
    } else {
        tree.innerHTML = '<span class="text-muted">' + (result.response || '').substring(0, 2000) + '</span>';
    }
    if (apiTestModal) apiTestModal.show();
}

function renderJsonTree(obj, path) {
    if (obj === null) return '<span class="text-muted" onclick="copyPath(\\'' + path + '\\')" style="cursor:pointer">null</span>';
    if (typeof obj !== 'object') {
        var val = typeof obj === 'string' ? '"' + obj.substring(0, 50) + (obj.length > 50 ? '...' : '') + '"' : String(obj);
        return '<span onclick="copyPath(\\'' + path + '\\')" style="cursor:pointer;color:#059669">' + val + '</span>';
    }
    var html = '';
    if (Array.isArray(obj)) {
        html = '[<br>';
        obj.slice(0, 10).forEach(function(item, i) {
            html += '&nbsp;&nbsp;' + renderJsonTree(item, path + '[' + i + ']') + (i < obj.length - 1 ? ',' : '') + '<br>';
        });
        if (obj.length > 10) html += '&nbsp;&nbsp;...(共' + obj.length + '项)<br>';
        html += ']';
    } else {
        html = '{<br>';
        var keys = Object.keys(obj);
        keys.slice(0, 20).forEach(function(key, i) {
            html += '&nbsp;&nbsp;<span onclick="copyPath(\\'' + path + '.' + key + '\\')" style="cursor:pointer;color:#2563eb">"' + key + '"</span>: ' + renderJsonTree(obj[key], path + '.' + key) + (i < keys.length - 1 ? ',' : '') + '<br>';
        });
        if (keys.length > 20) html += '&nbsp;&nbsp;...(共' + keys.length + '个字段)<br>';
        html += '}';
    }
    return html;
}

window.copyPath = function(path) {
    var varPath = '{' + path + '}';
    navigator.clipboard.writeText(varPath).then(function() { showToast('已复制: ' + varPath, 'info'); });
    var container = document.getElementById('selectedPaths');
    if (container && !container.innerHTML.includes(varPath)) {
        container.innerHTML += '<span class="badge bg-primary me-1 mb-1">' + varPath + '</span>';
    }
};

window.generateFromApi = function() {
    var name = document.getElementById('wizardName').value;
    var trigger = document.getElementById('wizardTrigger').value;
    var triggerType = document.getElementById('wizardTriggerType').value;
    var url = document.getElementById('wizardApiUrl').value;
    if (!name || !trigger || !url) { showToast('请填写必填项', 'error'); return; }
    if (apiWizardModal) apiWizardModal.hide();
    currentWorkflow = null; nodes = {}; connections = []; nodeIdCounter = 0;
    document.getElementById('canvasInner').innerHTML = '';
    var triggerId = createNode('trigger', 100, 100);
    nodes[triggerId].data = { trigger_type: triggerType, trigger_content: trigger };
    var actionId = createNode('action', 400, 100);
    var replyType = document.getElementById('wizardReplyType').value;
    var actionType = 'reply_text';
    if (replyType === 'image') actionType = 'reply_image';
    else if (replyType === 'markdown') actionType = 'reply_markdown';
    nodes[actionId].data = {
        action_type: 'custom_api',
        api_url: url,
        api_method: document.getElementById('wizardApiMethod').value,
        response_type: document.getElementById('wizardResponseType').value,
        api_headers: document.getElementById('wizardHeaders').value,
        api_body: document.getElementById('wizardBody').value,
        reply_type: replyType,
        api_reply: document.getElementById('wizardReply').value,
        image_text: document.getElementById('wizardImageText').value,
        keyboard_id: document.getElementById('wizardKeyboard').value,
        markdown_template: document.getElementById('wizardMdTemplate').value,
        ark_type: document.getElementById('wizardArkType').value
    };
    connections.push({ from: triggerId, to: actionId, port: 'output' });
    renderNode(triggerId); renderNode(actionId); renderConnections();
    showToast('工作流已生成', 'success');
};

function getToken() { return new URLSearchParams(window.location.search).get('token') || ''; }

function showToast(msg, type) {
    var toast = document.createElement('div');
    toast.className = 'toast-msg ' + (type || 'info');
    toast.innerHTML = '<i class="bi bi-' + (type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle') + '-fill"></i> ' + msg;
    document.body.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 3000);
}

// 初始化函数
function initWorkflowPage() {
    try {
        newModal = new bootstrap.Modal(document.getElementById('newModal'));
        apiWizardModal = new bootstrap.Modal(document.getElementById('apiWizardModal'));
        nodeEditModal = new bootstrap.Modal(document.getElementById('nodeEditModal'));
        aiModal = new bootstrap.Modal(document.getElementById('aiModal'));
        varListModal = new bootstrap.Modal(document.getElementById('varListModal'));
        apiTestModal = new bootstrap.Modal(document.getElementById('apiTestModal'));
        aiNodeModal = new bootstrap.Modal(document.getElementById('aiNodeModal'));
        console.log('[工作流] 模态框初始化完成');
    } catch(e) {
        console.error('[工作流] 模态框初始化失败:', e);
    }
    initCanvas();
    loadWorkflows();
    console.log('[工作流] 页面初始化完成');
}

// 立即执行初始化（插件页面通过AJAX加载，DOMContentLoaded已触发）
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWorkflowPage);
} else {
    // DOM已就绪，延迟执行确保HTML已渲染
    setTimeout(initWorkflowPage, 50);
}
'''
