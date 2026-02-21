# -*- coding: utf-8 -*-

import os
import re
import logging
import importlib

from core.plugin.PluginManager import Plugin

_current_dir = os.path.dirname(os.path.abspath(__file__))
_plugin_dir_name = os.path.basename(_current_dir)

def _import_tools():
    import sys
    tools_path = os.path.join(_current_dir, 'tools')
    if tools_path not in sys.path:
        sys.path.insert(0, _current_dir)
    try:
        from tools import load_workflows, save_workflows, WorkflowExecutor, WorkflowAPIHandlers, AIGenerator, get_html, get_script
        from tools.storage import WORKFLOW_FILE
        return load_workflows, save_workflows, WorkflowExecutor, WorkflowAPIHandlers, AIGenerator, get_html, get_script, WORKFLOW_FILE
    except ImportError:
        module_name = f"plugins.{_plugin_dir_name}.tools"
        tools_module = importlib.import_module(module_name)
        storage_module = importlib.import_module(f"{module_name}.storage")
        return (tools_module.load_workflows, tools_module.save_workflows, tools_module.WorkflowExecutor,
                tools_module.WorkflowAPIHandlers, tools_module.AIGenerator, tools_module.get_html,
                tools_module.get_script, storage_module.WORKFLOW_FILE)

load_workflows, save_workflows, WorkflowExecutor, WorkflowAPIHandlers, AIGenerator, get_html, get_script, WORKFLOW_FILE = _import_tools()

log = logging.getLogger(__name__)


class WorkflowPlugin(Plugin):
    """可视化工作流插件 - 动态正则 + 热重载"""
    priority = 9998
    _is_hot_reload = True  # 标记为可热重载
    
    def __init__(self):
        """初始化插件"""
        WorkflowAPIHandlers.set_plugin_class(WorkflowPlugin)
        log.info(f"[工作流] 初始化完成，配置文件: {WORKFLOW_FILE}")
    
    @classmethod
    def get_regex_handlers(cls):
        """从 JSON 动态加载触发器正则（与自定义API相同模式）"""
        handlers = {}
        
        try:
            # 检查文件是否存在
            if not os.path.exists(WORKFLOW_FILE):
                return {}
            
            workflows = load_workflows()
            for workflow in workflows:
                if not workflow.get('enabled', True):
                    continue
                    
                nodes = workflow.get('nodes', {})
                # 兼容列表和字典两种格式
                node_list = nodes.values() if isinstance(nodes, dict) else nodes
                
                for node in node_list:
                    if node.get('type') != 'trigger':
                        continue
                        
                    data = node.get('data', {})
                    trigger_type = data.get('trigger_type', 'exact')
                    # 兼容 trigger_content 和 trigger_value 两种字段名
                    trigger_value = data.get('trigger_content') or data.get('trigger_value', '')
                    
                    if not trigger_value:
                        continue
                    
                    # 根据触发类型生成正则
                    if trigger_type == 'exact':
                        pattern = f'^{re.escape(trigger_value)}$'
                    elif trigger_type == 'contains':
                        pattern = re.escape(trigger_value)
                    elif trigger_type == 'startswith':
                        pattern = f'^{re.escape(trigger_value)}'
                    elif trigger_type == 'regex':
                        pattern = trigger_value
                    elif trigger_type == 'any':
                        keywords = [re.escape(k.strip()) for k in trigger_value.split('|') if k.strip()]
                        if keywords:
                            pattern = f'({"|".join(keywords)})'
                        else:
                            continue
                    else:
                        continue
                    
                    # 每个模式只注册一次，使用统一的处理器
                    if pattern not in handlers:
                        handlers[pattern] = {'handler': 'handle_message'}
                        
        except Exception as e:
            log.error(f"[工作流] 加载触发器失败: {e}")
        
        log.debug(f"[工作流] 已注册 {len(handlers)} 个触发器")
        return handlers
    
    @staticmethod
    def handle_message(event):
        """处理匹配的消息"""
        content = event.content.strip()
        if not content:
            return None
        
        try:
            workflows = load_workflows()
            if not workflows:
                return None
            
            # 遍历工作流，找到第一个匹配的执行
            for workflow in workflows:
                if not workflow.get('enabled', True):
                    continue
                
                try:
                    executed = WorkflowExecutor.execute(workflow, event, content)
                    if executed:
                        # 执行成功，根据设置决定是否阻止其他插件
                        if workflow.get('stop_propagation', False):
                            return True
                        return None  # 执行完毕但不阻止其他插件
                except Exception as e:
                    log.error(f"[工作流] 执行失败: {e}")
        except Exception as e:
            log.error(f"[工作流] 处理消息失败: {e}")
            
        return None
    
    @classmethod
    def _reload_plugin(cls):
        """热重载插件以更新正则处理器"""
        try:
            from core.plugin.PluginManager import PluginManager
            PluginManager.reload_plugin(cls)
            log.info("[工作流] 插件已热重载")
        except Exception as e:
            log.error(f"[工作流] 热重载失败: {e}")
    
    # ========== Web API ==========
    
    @classmethod
    def get_web_routes(cls):
        return {
            'path': 'workflow',
            'menu_name': '工作流',
            'menu_icon': 'bi-diagram-3',
            'handler': 'render_page',
            'priority': 25,
            'api_routes': [
                {'path': '/api/workflow/list', 'methods': ['GET'], 'handler': 'api_list', 'require_auth': True},
                {'path': '/api/workflow/save', 'methods': ['POST'], 'handler': 'api_save', 'require_auth': True},
                {'path': '/api/workflow/delete', 'methods': ['POST'], 'handler': 'api_delete', 'require_auth': True},
                {'path': '/api/workflow/toggle', 'methods': ['POST'], 'handler': 'api_toggle', 'require_auth': True},
                {'path': '/api/workflow/ai_generate', 'methods': ['POST'], 'handler': 'api_ai_generate', 'require_auth': True},
                {'path': '/api/workflow/ai_node', 'methods': ['POST'], 'handler': 'api_ai_node', 'require_auth': True},
                {'path': '/api/workflow/ai_models', 'methods': ['GET'], 'handler': 'api_ai_models', 'require_auth': True},
                {'path': '/api/workflow/test_api', 'methods': ['POST'], 'handler': 'api_test_api', 'require_auth': True},
            ]
        }
    
    @classmethod
    def api_list(cls, data):
        return WorkflowAPIHandlers.api_list(data)
    
    @classmethod
    def api_save(cls, data):
        """保存工作流并热重载"""
        result = WorkflowAPIHandlers.api_save(data)
        if result.get('success'):
            cls._reload_plugin()
        return result
    
    @classmethod
    def api_delete(cls, data):
        """删除工作流并热重载"""
        result = WorkflowAPIHandlers.api_delete(data)
        if result.get('success'):
            cls._reload_plugin()
        return result
    
    @classmethod
    def api_toggle(cls, data):
        """切换工作流状态并热重载"""
        result = WorkflowAPIHandlers.api_toggle(data)
        if result.get('success'):
            cls._reload_plugin()
        return result
    
    @classmethod
    def api_ai_models(cls, data):
        return AIGenerator.get_models()
    
    @classmethod
    def api_ai_generate(cls, data):
        description = data.get('description', '')
        model = data.get('model', 'gpt-4o-mini')
        return AIGenerator.generate(description, model)
    
    @classmethod
    def api_ai_node(cls, data):
        """AI填写单个节点"""
        node_type = data.get('node_type', '')
        description = data.get('description', '')
        model = data.get('model', 'gpt-4o-mini')
        current_data = data.get('current_data', {})
        return AIGenerator.generate_node(node_type, description, model, current_data)
    
    @classmethod
    def api_test_api(cls, data):
        try:
            from tools import test_api
        except ImportError:
            import importlib
            tools_module = importlib.import_module(f"plugins.{_plugin_dir_name}.tools")
            test_api = tools_module.test_api
        return test_api(data)
    
    @staticmethod
    def render_page():
        return {'html': get_html(), 'script': get_script(), 'title': '可视化工作流'}
