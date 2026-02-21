# -*- coding: utf-8 -*-
"""工作流Web API处理模块"""

import time
import logging
from datetime import datetime
from .storage import load_workflows, save_workflows

log = logging.getLogger(__name__)


class WorkflowAPIHandlers:
    """工作流API处理器 - 不在此处重载，由主插件处理"""
    
    _plugin_class = None
    
    @classmethod
    def set_plugin_class(cls, plugin_class):
        """设置插件类引用"""
        cls._plugin_class = plugin_class
    
    @classmethod
    def api_list(cls, data):
        """获取工作流列表"""
        workflows = load_workflows()
        log.info(f"[工作流] api_list 返回 {len(workflows)} 个工作流")
        return {'success': True, 'workflows': workflows}
    
    @classmethod
    def api_save(cls, data):
        """保存工作流"""
        from .storage import WORKFLOW_FILE
        log.info(f"[工作流] 保存请求: {data.get('name')}, 文件: {WORKFLOW_FILE}")
        
        workflows = load_workflows()
        workflow_id = data.get('id')
        workflow_data = {
            'id': workflow_id or str(int(time.time() * 1000)),
            'name': data.get('name', '未命名'),
            'enabled': data.get('enabled', True),
            'stop_propagation': data.get('stop_propagation', False),
            'nodes': data.get('nodes', {}),
            'connections': data.get('connections', []),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 提取触发器信息用于快速匹配
        nodes = data.get('nodes', [])
        if isinstance(nodes, list):
            for n in nodes:
                if n.get('type') == 'trigger':
                    workflow_data['trigger_type'] = n.get('data', {}).get('trigger_type', 'exact')
                    workflow_data['trigger_content'] = n.get('data', {}).get('trigger_content', '')
                    break
        
        if workflow_id:
            found = False
            for i, w in enumerate(workflows):
                if w.get('id') == workflow_id:
                    workflow_data['created_at'] = w.get('created_at')
                    workflows[i] = workflow_data
                    found = True
                    break
            if not found:
                workflow_data['created_at'] = workflow_data['updated_at']
                workflows.append(workflow_data)
        else:
            workflow_data['created_at'] = workflow_data['updated_at']
            workflows.append(workflow_data)
        
        result = save_workflows(workflows)
        log.info(f"[工作流] 保存结果: {result}, 总数: {len(workflows)}")
        
        if result:
            return {'success': True, 'id': workflow_data['id'], 'data': workflow_data}
        else:
            return {'success': False, 'message': '保存文件失败'}
    
    @classmethod
    def api_delete(cls, data):
        """删除工作流"""
        workflow_id = data.get('id')
        if not workflow_id:
            return {'success': False, 'message': '缺少ID'}
        workflows = load_workflows()
        workflows = [w for w in workflows if w.get('id') != workflow_id]
        if save_workflows(workflows):
            return {'success': True}
        return {'success': False, 'message': '删除失败'}
    
    @classmethod
    def api_toggle(cls, data):
        """切换工作流状态"""
        workflow_id = data.get('id')
        if not workflow_id:
            return {'success': False, 'message': '缺少ID'}
        workflows = load_workflows()
        for w in workflows:
            if w.get('id') == workflow_id:
                w['enabled'] = not w.get('enabled', True)
                w['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if save_workflows(workflows):
                    return {'success': True, 'data': w}
                return {'success': False, 'message': '保存失败'}
        return {'success': False, 'message': '不存在'}
