# -*- coding: utf-8 -*-
"""工作流执行器模块 - 包含完整的API调用和响应处理功能"""

import re
import time
import random
import logging
import requests
from datetime import datetime

log = logging.getLogger(__name__)

# 默认请求头
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache'
}


class WorkflowExecutor:
    """工作流执行器"""
    
    @staticmethod
    def execute(workflow, event, content):
        """执行工作流"""
        nodes_raw = workflow.get('nodes', {})
        connections_raw = workflow.get('connections', [])
        
        # 兼容列表和字典两种格式，统一转换为字典
        if isinstance(nodes_raw, list):
            nodes = {n.get('id'): n for n in nodes_raw if n.get('id')}
        else:
            nodes = nodes_raw
        
        # 兼容连接格式 {from_node, to_node} 和 {from, to}
        connections = []
        for c in connections_raw:
            connections.append({
                'from_node': c.get('from_node') or c.get('from'),
                'to_node': c.get('to_node') or c.get('to'),
                'from_output': c.get('from_output') or c.get('port', 'output_1').replace('output', 'output_1')
            })
        
        trigger_nodes = [n for n in nodes.values() if n.get('type') == 'trigger']
        if not trigger_nodes:
            return False
        
        for trigger in trigger_nodes:
            match_result = WorkflowExecutor._check_trigger(trigger, content)
            if match_result is not None:
                context = {'regex_groups': match_result if isinstance(match_result, tuple) else ()}
                return WorkflowExecutor._execute_from_node(trigger['id'], nodes, connections, event, content, context)
        
        return False
    
    @staticmethod
    def _check_trigger(node, content):
        """检查触发条件，返回匹配的捕获组"""
        data = node.get('data', {})
        trigger_type = data.get('trigger_type', 'exact')
        # 兼容 trigger_content 和 trigger_value 两种字段名
        trigger_value = data.get('trigger_content') or data.get('trigger_value', '')
        
        if not trigger_value:
            return None
        
        if trigger_type == 'exact':
            return () if content == trigger_value else None
        elif trigger_type == 'contains':
            return () if trigger_value in content else None
        elif trigger_type == 'startswith':
            return () if content.startswith(trigger_value) else None
        elif trigger_type == 'regex':
            try:
                match = re.search(trigger_value, content)
                if match:
                    return match.groups()
            except:
                pass
            return None
        elif trigger_type == 'any':
            keywords = [k.strip() for k in trigger_value.split('|') if k.strip()]
            return () if any(kw in content for kw in keywords) else None
        return None
    
    @staticmethod
    def _execute_from_node(node_id, nodes, connections, event, content, context):
        """从指定节点开始执行"""
        node = nodes.get(node_id)
        if not node:
            return False
        
        node_type = node.get('type')
        data = node.get('data', {})
        result = True
        
        if node_type == 'trigger':
            pass
        elif node_type == 'condition':
            result = WorkflowExecutor._check_condition(data, event, content, context)
        elif node_type == 'action':
            WorkflowExecutor._execute_action(data, event, content, context)
        elif node_type == 'delay':
            delay_seconds = float(data.get('seconds', 1))
            time.sleep(min(delay_seconds, 10))
        elif node_type == 'set_var':
            var_name = data.get('var_name', '')
            var_value = WorkflowExecutor._replace_vars(data.get('var_value', ''), event, content, context)
            if var_name:
                context[var_name] = var_value
        elif node_type == 'storage':
            WorkflowExecutor._execute_storage(data, event, content, context)
        elif node_type == 'math':
            WorkflowExecutor._execute_math(data, event, content, context)
        elif node_type == 'random_branch':
            result = WorkflowExecutor._execute_random_branch(data, context)
        elif node_type == 'list_random':
            WorkflowExecutor._execute_list_random(data, event, content, context)
        elif node_type == 'switch':
            result = WorkflowExecutor._execute_switch(data, event, content, context)
        elif node_type == 'global_storage':
            WorkflowExecutor._execute_global_storage(data, event, content, context)
        elif node_type == 'leaderboard':
            WorkflowExecutor._execute_leaderboard(data, event, content, context)
        elif node_type == 'string_op':
            WorkflowExecutor._execute_string_op(data, event, content, context)
        elif node_type == 'format':
            WorkflowExecutor._execute_format(data, event, content, context)
        elif node_type == 'comment':
            pass
        
        if result:
            # 条件满足或普通节点：走 output_1 或 output-1 或 output
            next_conns = [c for c in connections if c.get('from_node') == node_id and 
                         c.get('from_output', 'output_1') in ('output_1', 'output-1', 'output')]
        else:
            # 条件不满足：走 output_2 或 output-2
            next_conns = [c for c in connections if c.get('from_node') == node_id and 
                         c.get('from_output') in ('output_2', 'output-2')]
        
        for conn in next_conns:
            next_node_id = conn.get('to_node')
            if next_node_id:
                WorkflowExecutor._execute_from_node(next_node_id, nodes, connections, event, content, context)
        
        return True
    
    @staticmethod
    def _check_condition(data, event, content, context):
        """检查条件"""
        cond_type = data.get('condition_type', 'is_group')
        cond_value = data.get('condition_value', '')
        
        if cond_type == 'is_group':
            return event.is_group
        elif cond_type == 'is_private':
            return not event.is_group
        elif cond_type == 'user_in':
            users = [u.strip() for u in cond_value.split('|') if u.strip()]
            return event.user_id in users
        elif cond_type == 'group_in':
            groups = [g.strip() for g in cond_value.split('|') if g.strip()]
            return event.is_group and event.group_id in groups
        elif cond_type == 'content_contains':
            return cond_value in content
        elif cond_type == 'random':
            try:
                prob = float(cond_value)
                return random.random() * 100 < prob
            except:
                return False
        elif cond_type == 'var_equals':
            parts = cond_value.split('=', 1)
            if len(parts) == 2:
                return context.get(parts[0].strip()) == parts[1].strip()
        elif cond_type == 'var_gt':
            parts = cond_value.split('>', 1)
            if len(parts) == 2:
                try:
                    return float(context.get(parts[0].strip(), 0)) > float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'var_lt':
            parts = cond_value.split('<', 1)
            if len(parts) == 2:
                try:
                    return float(context.get(parts[0].strip(), 0)) < float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'var_gte':
            parts = cond_value.split('>=', 1)
            if len(parts) == 2:
                try:
                    return float(context.get(parts[0].strip(), 0)) >= float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'data_equals':
            parts = cond_value.split('=', 1)
            if len(parts) == 2:
                from .storage import get_user_value
                stored = get_user_value(event.user_id, parts[0].strip(), '')
                return str(stored) == parts[1].strip()
        elif cond_type == 'data_gt':
            parts = cond_value.split('>', 1)
            if len(parts) == 2:
                try:
                    from .storage import get_user_value
                    stored = get_user_value(event.user_id, parts[0].strip(), 0)
                    return float(stored) > float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'data_exists':
            from .storage import get_user_value
            return get_user_value(event.user_id, cond_value.strip()) is not None
        elif cond_type == 'data_is_today':
            from .storage import get_user_value
            stored = get_user_value(event.user_id, cond_value.strip(), '')
            today = datetime.now().strftime('%Y-%m-%d')
            return str(stored) == today
        elif cond_type == 'data_not_today':
            from .storage import get_user_value
            stored = get_user_value(event.user_id, cond_value.strip(), '')
            today = datetime.now().strftime('%Y-%m-%d')
            return str(stored) != today
        elif cond_type == 'data_lt':
            parts = cond_value.split('<', 1)
            if len(parts) == 2:
                try:
                    from .storage import get_user_value
                    stored = get_user_value(event.user_id, parts[0].strip(), 0)
                    return float(stored) < float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'data_gte':
            parts = cond_value.split('>=', 1)
            if len(parts) == 2:
                try:
                    from .storage import get_user_value
                    stored = get_user_value(event.user_id, parts[0].strip(), 0)
                    return float(stored) >= float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'data_lte':
            parts = cond_value.split('<=', 1)
            if len(parts) == 2:
                try:
                    from .storage import get_user_value
                    stored = get_user_value(event.user_id, parts[0].strip(), 0)
                    return float(stored) <= float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'cooldown':
            parts = cond_value.split(',')
            if len(parts) >= 2:
                key = parts[0].strip()
                try:
                    seconds = int(parts[1].strip())
                    from .storage import get_user_value
                    last_time = get_user_value(event.user_id, key, 0)
                    return (time.time() - float(last_time)) >= seconds
                except:
                    return True
            return True
        elif cond_type == 'in_cooldown':
            parts = cond_value.split(',')
            if len(parts) >= 2:
                key = parts[0].strip()
                try:
                    seconds = int(parts[1].strip())
                    from .storage import get_user_value
                    last_time = get_user_value(event.user_id, key, 0)
                    return (time.time() - float(last_time)) < seconds
                except:
                    return False
            return False
        elif cond_type == 'time_range':
            parts = cond_value.split('-')
            if len(parts) == 2:
                try:
                    start_hour = int(parts[0].strip())
                    end_hour = int(parts[1].strip())
                    current_hour = datetime.now().hour
                    if start_hour <= end_hour:
                        return start_hour <= current_hour <= end_hour
                    else:
                        return current_hour >= start_hour or current_hour <= end_hour
                except:
                    return True
        elif cond_type == 'weekday_in':
            weekdays = [w.strip() for w in cond_value.split('|') if w.strip()]
            current_wd = str(datetime.now().weekday())
            wd_map = {'周一':'0','周二':'1','周三':'2','周四':'3','周五':'4','周六':'5','周日':'6',
                      '一':'0','二':'1','三':'2','四':'3','五':'4','六':'5','日':'6','天':'6',
                      '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6'}
            return any(wd_map.get(w, w) == current_wd for w in weekdays)
        elif cond_type == 'expression':
            try:
                expr = WorkflowExecutor._replace_vars(cond_value, event, content, context)
                expr = expr.replace('==', ' == ').replace('!=', ' != ')
                expr = expr.replace('>=', ' >= ').replace('<=', ' <= ')
                expr = expr.replace('>', ' > ').replace('<', ' < ')
                expr = expr.replace('&&', ' and ').replace('||', ' or ')
                result = eval(expr, {"__builtins__": {}}, {})
                return bool(result)
            except:
                return False
        elif cond_type == 'global_equals':
            parts = cond_value.split('=', 1)
            if len(parts) == 2:
                from .storage import get_global_value
                stored = get_global_value(parts[0].strip(), '')
                return str(stored) == parts[1].strip()
        elif cond_type == 'global_gt':
            parts = cond_value.split('>', 1)
            if len(parts) == 2:
                try:
                    from .storage import get_global_value
                    stored = get_global_value(parts[0].strip(), 0)
                    return float(stored) > float(parts[1].strip())
                except:
                    return False
        elif cond_type == 'rank_top':
            parts = cond_value.split(',')
            if len(parts) >= 2:
                try:
                    key = parts[0].strip()
                    n = int(parts[1].strip())
                    from .storage import get_user_rank
                    rank, _, _ = get_user_rank(event.user_id, key)
                    return 0 < rank <= n
                except:
                    return False
        elif cond_type == 'content_regex':
            try:
                import re as regex_module
                return bool(regex_module.search(cond_value, content))
            except:
                return False
        elif cond_type == 'content_length':
            parts = cond_value.split('-')
            if len(parts) == 2:
                try:
                    min_len = int(parts[0].strip())
                    max_len = int(parts[1].strip())
                    return min_len <= len(content) <= max_len
                except:
                    return True
            try:
                return len(content) == int(cond_value)
            except:
                return True
        elif cond_type == 'is_number':
            target = WorkflowExecutor._replace_vars(cond_value or '{content}', event, content, context)
            try:
                float(target)
                return True
            except:
                return False
        return True
    
    @staticmethod
    def _execute_storage(data, event, content, context):
        """执行存储操作"""
        from .storage import get_user_value, set_user_value, incr_user_value, delete_user_value
        
        storage_type = data.get('storage_type', 'get')
        key = WorkflowExecutor._replace_vars(data.get('storage_key', ''), event, content, context)
        value = WorkflowExecutor._replace_vars(data.get('storage_value', ''), event, content, context)
        var_name = data.get('result_var', 'data_result')
        
        if not key:
            return
        
        try:
            if storage_type == 'get':
                result = get_user_value(event.user_id, key, data.get('default_value', ''))
                context[var_name] = result
            elif storage_type == 'set':
                try:
                    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                        value = int(value)
                    elif '.' in value:
                        value = float(value)
                except:
                    pass
                set_user_value(event.user_id, key, value)
                context[var_name] = value
            elif storage_type == 'incr':
                try:
                    amount = float(value) if value else 1
                except:
                    amount = 1
                result = incr_user_value(event.user_id, key, amount, 0)
                context[var_name] = result
            elif storage_type == 'decr':
                try:
                    amount = float(value) if value else 1
                except:
                    amount = 1
                result = incr_user_value(event.user_id, key, -amount, 0)
                context[var_name] = result
            elif storage_type == 'delete':
                delete_user_value(event.user_id, key)
                context[var_name] = ''
        except Exception as e:
            log.error(f"存储操作失败: {e}")
    
    @staticmethod
    def _execute_math(data, event, content, context):
        """执行数学运算"""
        math_type = data.get('math_type', 'add')
        operand1 = WorkflowExecutor._replace_vars(data.get('operand1', '0'), event, content, context)
        operand2 = WorkflowExecutor._replace_vars(data.get('operand2', '0'), event, content, context)
        result_var = data.get('result_var', 'math_result')
        
        try:
            a = float(operand1)
            b = float(operand2)
            
            if math_type == 'add':
                result = a + b
            elif math_type == 'sub':
                result = a - b
            elif math_type == 'mul':
                result = a * b
            elif math_type == 'div':
                result = a / b if b != 0 else 0
            elif math_type == 'mod':
                result = a % b if b != 0 else 0
            elif math_type == 'pow':
                result = a ** b
            elif math_type == 'min':
                result = min(a, b)
            elif math_type == 'max':
                result = max(a, b)
            elif math_type == 'random':
                result = random.randint(int(a), int(b))
            else:
                result = a
            
            if result == int(result):
                result = int(result)
            context[result_var] = result
        except Exception as e:
            log.error(f"数学运算失败: {e}")
            context[result_var] = 0
    
    @staticmethod
    def _execute_random_branch(data, context):
        """随机分支 - 返回True走output_1，False走output_2"""
        try:
            probability = float(data.get('probability', 50))
            return random.random() * 100 < probability
        except:
            return True
    
    @staticmethod
    def _execute_list_random(data, event, content, context):
        """从列表随机选择"""
        list_str = data.get('list_items', '')
        result_var = data.get('result_var', 'list_result')
        index_var = data.get('index_var', 'list_index')
        
        list_str = WorkflowExecutor._replace_vars(list_str, event, content, context)
        
        items = [item.strip() for item in list_str.split('|') if item.strip()]
        
        if items:
            weights_str = data.get('weights', '')
            if weights_str:
                try:
                    weights = [float(w.strip()) for w in weights_str.split('|')]
                    if len(weights) == len(items):
                        total = sum(weights)
                        r = random.random() * total
                        cumulative = 0
                        for i, w in enumerate(weights):
                            cumulative += w
                            if r <= cumulative:
                                context[result_var] = items[i]
                                context[index_var] = i
                                return
                except:
                    pass
            
            idx = random.randint(0, len(items) - 1)
            context[result_var] = items[idx]
            context[index_var] = idx
        else:
            context[result_var] = ''
            context[index_var] = -1
    
    @staticmethod
    def _execute_switch(data, event, content, context):
        """多路分支 - 根据值选择不同输出"""
        return True
    
    @staticmethod
    def _execute_global_storage(data, event, content, context):
        """执行全局存储操作"""
        from .storage import get_global_value, set_global_value, incr_global_value
        
        storage_type = data.get('storage_type', 'get')
        key = WorkflowExecutor._replace_vars(data.get('storage_key', ''), event, content, context)
        value = WorkflowExecutor._replace_vars(data.get('storage_value', ''), event, content, context)
        var_name = data.get('result_var', 'global_result')
        
        if not key:
            return
        
        try:
            if storage_type == 'get':
                result = get_global_value(key, data.get('default_value', ''))
                context[var_name] = result
            elif storage_type == 'set':
                try:
                    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                        value = int(value)
                    elif '.' in value:
                        value = float(value)
                except:
                    pass
                set_global_value(key, value)
                context[var_name] = value
            elif storage_type == 'incr':
                try:
                    amount = float(value) if value else 1
                except:
                    amount = 1
                result = incr_global_value(key, amount, 0)
                context[var_name] = result
            elif storage_type == 'decr':
                try:
                    amount = float(value) if value else 1
                except:
                    amount = 1
                result = incr_global_value(key, -amount, 0)
                context[var_name] = result
        except Exception as e:
            log.error(f"全局存储操作失败: {e}")
    
    @staticmethod
    def _execute_leaderboard(data, event, content, context):
        """获取排行榜数据"""
        from .storage import get_leaderboard, get_user_rank, count_users_with_key
        
        lb_type = data.get('leaderboard_type', 'top')
        key = data.get('leaderboard_key', 'score')
        limit = int(data.get('limit', 10))
        ascending = data.get('ascending', False)
        
        try:
            if lb_type == 'top':
                results = get_leaderboard(key, limit, ascending)
                formatted = []
                for i, (user_id, value) in enumerate(results, 1):
                    if value == int(value):
                        value = int(value)
                    formatted.append(f"{i}. {user_id[:8]}... : {value}")
                context['leaderboard'] = '\n'.join(formatted)
                context['leaderboard_list'] = results
            elif lb_type == 'my_rank':
                rank, value, total = get_user_rank(event.user_id, key, ascending)
                context['my_rank'] = rank
                context['my_value'] = value if value == int(value) else value
                context['total_users'] = total
            elif lb_type == 'count':
                count = count_users_with_key(key)
                context['user_count'] = count
        except Exception as e:
            log.error(f"排行榜操作失败: {e}")
    
    @staticmethod
    def _execute_string_op(data, event, content, context):
        """字符串操作"""
        op_type = data.get('string_type', 'concat')
        input1 = WorkflowExecutor._replace_vars(data.get('input1', ''), event, content, context)
        input2 = WorkflowExecutor._replace_vars(data.get('input2', ''), event, content, context)
        result_var = data.get('result_var', 'string_result')
        
        try:
            if op_type == 'concat':
                result = input1 + input2
            elif op_type == 'replace':
                target = data.get('target', '')
                result = input1.replace(target, input2)
            elif op_type == 'split':
                delimiter = input2 if input2 else '|'
                parts = input1.split(delimiter)
                context['split_list'] = parts
                context['split_count'] = len(parts)
                result = parts[0] if parts else ''
            elif op_type == 'length':
                result = len(input1)
            elif op_type == 'upper':
                result = input1.upper()
            elif op_type == 'lower':
                result = input1.lower()
            elif op_type == 'trim':
                result = input1.strip()
            elif op_type == 'substr':
                try:
                    start = int(input2.split(',')[0]) if input2 else 0
                    end = int(input2.split(',')[1]) if ',' in input2 else None
                    result = input1[start:end]
                except:
                    result = input1
            elif op_type == 'contains':
                result = '1' if input2 in input1 else '0'
                context['contains'] = input2 in input1
            elif op_type == 'startswith':
                result = '1' if input1.startswith(input2) else '0'
            elif op_type == 'endswith':
                result = '1' if input1.endswith(input2) else '0'
            elif op_type == 'reverse':
                result = input1[::-1]
            elif op_type == 'repeat':
                try:
                    times = int(input2) if input2 else 1
                    result = input1 * min(times, 100)
                except:
                    result = input1
            else:
                result = input1
            
            context[result_var] = result
        except Exception as e:
            log.error(f"字符串操作失败: {e}")
            context[result_var] = ''
    
    @staticmethod
    def _execute_format(data, event, content, context):
        """格式化输出"""
        template = data.get('template', '')
        result_var = data.get('result_var', 'format_result')
        
        result = WorkflowExecutor._replace_vars(template, event, content, context)
        context[result_var] = result
    
    @staticmethod
    def _execute_action(data, event, content, context):
        """执行动作"""
        action_type = data.get('action_type', 'reply_text')
        action_value = WorkflowExecutor._replace_vars(data.get('action_value', ''), event, content, context)
        
        try:
            if action_type == 'reply_text':
                if '|||' in action_value:
                    replies = [r.strip() for r in action_value.split('|||') if r.strip()]
                    if replies:
                        action_value = random.choice(replies)
                event.reply(action_value)
            
            elif action_type == 'reply_image':
                event.reply_image(action_value)
            
            elif action_type == 'reply_voice':
                event.reply_voice(action_value)
            
            elif action_type == 'reply_video':
                event.reply_video(action_value)
            
            elif action_type == 'reply_markdown':
                template_id = data.get('template_id', '')
                if template_id:
                    params = {}
                    param_str = data.get('template_params', '')
                    if param_str:
                        for line in param_str.split('\n'):
                            line = line.strip()
                            if '=' in line:
                                k, v = line.split('=', 1)
                                params[k.strip()] = WorkflowExecutor._replace_vars(v.strip(), event, content, context)
                    event.reply_markdown(template_id, params)
                else:
                    event.reply(action_value)
            
            elif action_type == 'reply_markdown_aj':
                keyboard_id = data.get('keyboard_id', '')
                event.reply_markdown_aj(action_value, keyboard_id if keyboard_id else None)
            
            elif action_type == 'custom_api':
                WorkflowExecutor._execute_custom_api(data, event, content, context)
            
            elif action_type == 'math':
                WorkflowExecutor._execute_math(data, event, content, context)
            
            elif action_type == 'string_op':
                WorkflowExecutor._execute_string_op(data, event, content, context)
                    
        except Exception as e:
            log.error(f"工作流动作执行失败: {e}")
    
    @staticmethod
    def _execute_custom_api(data, event, content, context):
        """执行自定义API调用"""
        api_url = WorkflowExecutor._replace_vars(data.get('api_url', ''), event, content, context)
        api_method = data.get('api_method', 'GET').upper()
        timeout = int(data.get('api_timeout', 10))
        response_type = data.get('response_type', 'json')
        
        # 解析请求头
        headers = dict(DEFAULT_HEADERS)
        headers_str = data.get('api_headers', '')
        if headers_str:
            try:
                import json
                custom_headers = json.loads(headers_str)
                headers.update(custom_headers)
            except:
                for line in headers_str.split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        headers[k.strip()] = WorkflowExecutor._replace_vars(v.strip(), event, content, context)
        
        # 解析请求体
        body = None
        body_str = data.get('api_body', '')
        if body_str and api_method in ['POST', 'PUT', 'PATCH']:
            try:
                import json
                body = json.loads(WorkflowExecutor._replace_vars(body_str, event, content, context))
            except:
                body = WorkflowExecutor._replace_vars(body_str, event, content, context)
        
        # 解析URL参数
        params = {}
        params_str = data.get('api_params', '')
        if params_str:
            try:
                import json
                params = json.loads(WorkflowExecutor._replace_vars(params_str, event, content, context))
            except:
                pass
        
        try:
            # 发送请求
            if api_method == 'GET':
                resp = requests.get(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
            elif api_method == 'POST':
                if isinstance(body, dict):
                    resp = requests.post(api_url, headers=headers, params=params, json=body, timeout=timeout, allow_redirects=True)
                else:
                    resp = requests.post(api_url, headers=headers, params=params, data=body, timeout=timeout, allow_redirects=True)
            elif api_method == 'PUT':
                resp = requests.put(api_url, headers=headers, params=params, json=body, timeout=timeout, allow_redirects=True)
            elif api_method == 'DELETE':
                resp = requests.delete(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
            else:
                resp = requests.get(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
            
            # 处理响应
            context['api_status'] = resp.status_code
            context['api_response'] = resp.text
            
            if response_type == 'json':
                try:
                    context['api_json'] = resp.json()
                except:
                    context['api_json'] = {}
            elif response_type == 'binary':
                context['api_binary'] = resp.content
            
            # 发送回复
            reply_type = data.get('reply_type', 'text')
            reply_template = data.get('api_reply', '')
            message_template = data.get('message_template', '')
            
            template = reply_template or message_template
            
            if reply_type == 'text' or reply_type == '':
                if template:
                    reply_text = WorkflowExecutor._process_template(template, event, content, context)
                    event.reply(reply_text)
                else:
                    event.reply(context.get('api_response', ''))
            
            elif reply_type == 'image':
                if response_type == 'binary':
                    event.reply_image(context.get('api_binary'))
                else:
                    url = WorkflowExecutor._process_template(template, event, content, context) if template else context.get('api_response', '')
                    image_text = data.get('image_text', '')
                    if image_text:
                        image_text = WorkflowExecutor._replace_vars(image_text, event, content, context)
                    event.reply_image(url, image_text if image_text else None)
            
            elif reply_type == 'voice':
                if response_type == 'binary':
                    event.reply_voice(context.get('api_binary'))
                else:
                    url = WorkflowExecutor._process_template(template, event, content, context) if template else context.get('api_response', '')
                    event.reply_voice(url)
            
            elif reply_type == 'video':
                if response_type == 'binary':
                    event.reply_video(context.get('api_binary'))
                else:
                    url = WorkflowExecutor._process_template(template, event, content, context) if template else context.get('api_response', '')
                    event.reply_video(url)
            
            elif reply_type == 'markdown':
                text = WorkflowExecutor._process_template(template, event, content, context) if template else context.get('api_response', '')
                event.reply(text, use_markdown=True)
            
            elif reply_type == 'template_markdown':
                md_template = data.get('markdown_template', '1')
                keyboard_id = data.get('keyboard_id', '')
                text = WorkflowExecutor._process_template(template, event, content, context)
                params = WorkflowExecutor._parse_template_params(text)
                event.reply_markdown(md_template, tuple(params), keyboard_id if keyboard_id else None)
            
            elif reply_type == 'ark':
                ark_type = data.get('ark_type', '23')
                text = WorkflowExecutor._process_template(template, event, content, context)
                params = WorkflowExecutor._parse_ark_params(text)
                event.reply_ark(ark_type, tuple(params))
                
        except requests.Timeout:
            event.reply("API请求超时")
        except Exception as e:
            log.error(f"API调用失败: {e}")
            event.reply(f"API调用失败: {str(e)}")
    
    @staticmethod
    def _process_template(template, event, content, context):
        """处理消息模板"""
        if not template:
            return ''
        
        result = template
        
        # 先替换正则捕获组
        regex_groups = context.get('regex_groups', ())
        for i, group in enumerate(regex_groups, 1):
            result = result.replace(f'{{${i}}}', str(group) if group else '')
        
        # 替换基本变量
        result = WorkflowExecutor._replace_vars(result, event, content, context)
        
        # 如果是JSON响应，处理JSON路径
        api_json = context.get('api_json')
        if api_json and isinstance(api_json, dict):
            # 查找所有 {path} 模式
            pattern = r'\{(?!\$)([^}]+)\}'
            matches = re.findall(pattern, result)
            for path in matches:
                if path not in ['user_id', 'group_id', 'content', 'date', 'time', 'random', 'at_user', 'api_response', 'api_status', 'message', 'timestamp']:
                    value = WorkflowExecutor._extract_json_path(api_json, path.strip())
                    result = result.replace(f'{{{path}}}', str(value))
        
        return result
    
    @staticmethod
    def _extract_json_path(data, path):
        """从JSON中提取指定路径的数据"""
        try:
            parts = path.split('.')
            result = data
            
            for part in parts:
                if '[' in part and ']' in part:
                    key = part[:part.index('[')]
                    index = int(part[part.index('[') + 1:part.index(']')])
                    if key:
                        result = result[key][index]
                    else:
                        result = result[index]
                else:
                    result = result[part]
            
            return result
        except Exception as e:
            return f'[提取失败:{path}]'
    
    @staticmethod
    def _parse_template_params(template_str):
        """解析模板参数"""
        if not template_str:
            return []
        
        params = []
        current = ""
        depth = 0
        array_items = []
        
        for char in template_str:
            if char == '(' and depth == 0:
                if current.strip():
                    params.append(current.strip())
                    current = ""
                depth = 1
                array_items = []
            elif char == ')' and depth == 1:
                if current.strip():
                    array_items.append(current.strip())
                    current = ""
                params.append(array_items)
                depth = 0
                array_items = []
            elif char == ',' and depth == 0:
                if current.strip():
                    params.append(current.strip())
                current = ""
            elif char == ',' and depth == 1:
                if current.strip():
                    array_items.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            params.append(current.strip())
        
        return params
    
    @staticmethod
    def _parse_ark_params(template_str):
        """解析ARK参数"""
        all_params = WorkflowExecutor._parse_template_params(template_str)
        
        normal_params = []
        list_items = []
        
        for param in all_params:
            if isinstance(param, list):
                list_items.append(param)
            else:
                normal_params.append(param)
        
        if list_items:
            return normal_params + [list_items]
        return normal_params
    
    @staticmethod
    def _replace_vars(text, event, content, context):
        """替换变量"""
        if not text or '{' not in text:
            return text
        
        now = datetime.now()
        variables = {
            '{user_id}': str(event.user_id),
            '{group_id}': str(event.group_id) if event.is_group else '',
            '{content}': content,
            '{message}': content,
            '{date}': now.strftime('%Y-%m-%d'),
            '{today}': now.strftime('%Y-%m-%d'),
            '{time}': now.strftime('%H:%M:%S'),
            '{datetime}': now.strftime('%Y-%m-%d %H:%M:%S'),
            '{timestamp}': str(int(time.time())),
            '{year}': str(now.year),
            '{month}': str(now.month),
            '{day}': str(now.day),
            '{hour}': str(now.hour),
            '{minute}': str(now.minute),
            '{weekday}': str(now.weekday()),
            '{weekday_cn}': ['周一','周二','周三','周四','周五','周六','周日'][now.weekday()],
            '{random}': str(random.randint(1, 100)),
            '{random100}': str(random.randint(1, 100)),
            '{random10}': str(random.randint(1, 10)),
            '{random6}': str(random.randint(1, 6)),
            '{at_user}': f'<@{event.user_id}>',
        }
        
        for var, value in variables.items():
            text = text.replace(var, value)
        
        # 替换正则捕获组
        regex_groups = context.get('regex_groups', ())
        for i, group in enumerate(regex_groups, 1):
            text = text.replace(f'{{${i}}}', str(group) if group else '')
        
        # 替换上下文变量
        for var_name, var_value in context.items():
            if var_name == 'api_json' and isinstance(var_value, dict):
                for key, val in var_value.items():
                    text = text.replace(f'{{api_json.{key}}}', str(val))
            elif var_name not in ['regex_groups', 'api_binary']:
                text = text.replace(f'{{{var_name}}}', str(var_value))
        
        # 支持读取用户存储数据 {storage.key}
        import re as regex_module
        storage_pattern = r'\{storage\.([^}]+)\}'
        storage_matches = regex_module.findall(storage_pattern, text)
        if storage_matches:
            from .storage import get_user_value
            for key in storage_matches:
                value = get_user_value(event.user_id, key, '')
                text = text.replace(f'{{storage.{key}}}', str(value))
        
        return text


def test_api(api_config):
    """测试API调用（用于Web面板）"""
    try:
        api_url = api_config.get('url', api_config.get('api_url', ''))
        api_method = api_config.get('method', api_config.get('api_method', 'GET')).upper()
        timeout = int(api_config.get('timeout', api_config.get('api_timeout', 10)))
        response_type = api_config.get('response_type', 'json')
        
        headers = dict(DEFAULT_HEADERS)
        headers_data = api_config.get('headers', api_config.get('api_headers', {}))
        if isinstance(headers_data, str):
            try:
                import json
                headers_data = json.loads(headers_data)
            except:
                headers_data = {}
        if headers_data:
            headers.update(headers_data)
        
        params = api_config.get('params', {})
        if isinstance(params, str):
            try:
                import json
                params = json.loads(params)
            except:
                params = {}
        
        body = api_config.get('body', api_config.get('api_body', None))
        if isinstance(body, str) and body:
            try:
                import json
                body = json.loads(body)
            except:
                pass
        
        # 发送请求
        if api_method == 'GET':
            resp = requests.get(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
        elif api_method == 'POST':
            resp = requests.post(api_url, headers=headers, params=params, json=body, timeout=timeout, allow_redirects=True)
        elif api_method == 'PUT':
            resp = requests.put(api_url, headers=headers, params=params, json=body, timeout=timeout, allow_redirects=True)
        elif api_method == 'DELETE':
            resp = requests.delete(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
        else:
            resp = requests.get(api_url, headers=headers, params=params, timeout=timeout, allow_redirects=True)
        
        if not (200 <= resp.status_code < 300):
            return {'success': False, 'error': f'HTTP {resp.status_code}'}
        
        if response_type == 'json':
            try:
                return {'success': True, 'data': resp.json()}
            except:
                return {'success': True, 'data': resp.text}
        elif response_type == 'binary':
            return {'success': True, 'data': resp.content, 'is_binary': True}
        else:
            return {'success': True, 'data': resp.text}
            
    except requests.Timeout:
        return {'success': False, 'error': 'API请求超时'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
