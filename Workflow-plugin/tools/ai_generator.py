# -*- coding: utf-8 -*-
"""工作流AI生成模块"""

import re
import json
import logging

log = logging.getLogger(__name__)

AI_SERVICE_URL = 'https://i.elaina.vin/api/elainabot/ai.php'


class AIGenerator:
    """AI工作流生成器"""
    
    @classmethod
    def get_models(cls):
        """获取可用的AI模型列表"""
        try:
            import httpx
            with httpx.Client(timeout=30, verify=False) as client:
                response = client.post(AI_SERVICE_URL, json={'action': 'status'})
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        return {
                            'success': True,
                            'models': result.get('models', []),
                            'default_model': result.get('default_model', 'gpt-4o-mini')
                        }
            return {'success': False, 'message': 'AI服务不可用'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    @classmethod
    def generate(cls, description, model='gpt-4o-mini'):
        """AI生成工作流"""
        try:
            import httpx
            
            if not description:
                return {'success': False, 'message': '请输入工作流描述'}
            
            workflow_desc = f'''你是QQ机器人工作流生成器。根据用户需求生成完整的工作流JSON。

用户需求: {description}

## 全部节点类型及参数

### 1. trigger - 触发器（必须有且只有一个，工作流起点）
data: {{"trigger_type":"类型","trigger_content":"触发内容"}}
trigger_type可选: exact(完全匹配), startswith(前缀匹配), contains(包含匹配), regex(正则匹配)
示例: {{"trigger_type":"exact","trigger_content":"签到"}}

### 2. condition - 条件判断（2个输出：满足走output-1，不满足走output-2）
data: {{"condition_type":"类型","condition_value":"值"}}
condition_type可选:
- contains: 内容包含
- equals: 内容等于  
- regex: 正则匹配
- random: 随机概率(0-100)
- user_id: 用户ID等于
- group_id: 群ID等于
- var_equals: 变量等于(格式: 变量名:值)
- var_gt: 变量大于(格式: 变量名:数值)
- var_lt: 变量小于
- data_equals: 用户存储等于(格式: 键名:值)
- data_gt: 用户存储大于
- data_lt: 用户存储小于
- data_is_today: 今日已操作(值=存储键名)
- cooldown: 冷却时间(值=秒数)
- time_range: 时间范围(格式: 08:00-18:00)
- weekday_in: 星期几(格式: 1,2,3,4,5)
- global_equals: 全局存储等于
- global_gt: 全局存储大于
- rank_top: 排行前N
- content_regex: 内容正则
- content_length: 内容长度(格式: >=5)
- is_number: 是否数字
- expression: 表达式(如: {{score}}>100)
示例: {{"condition_type":"data_is_today","condition_value":"sign_date"}}

### 3. action - 动作节点
回复类型:
- reply_text: 回复文字 {{"action_type":"reply_text","action_value":"内容"}}
- reply_image: 发送图片 {{"action_type":"reply_image","action_value":"图片URL"}}
- reply_voice: 发送语音 {{"action_type":"reply_voice","action_value":"语音URL"}}
- reply_video: 发送视频 {{"action_type":"reply_video","action_value":"视频URL"}}
- reply_markdown: Markdown {{"action_type":"reply_markdown","action_value":"**加粗**"}}
- reply_markdown_aj: AJ Markdown {{"action_type":"reply_markdown_aj","action_value":"内容"}}

数据操作:
- math: 数学运算 {{"action_type":"math","math_type":"类型","operand1":"值1","operand2":"值2","result_var":"结果变量"}}
  math_type: add(加), sub(减), mul(乘), div(除), mod(取余), random(随机), abs(绝对值), round(四舍五入), floor(向下取整), ceil(向上取整), pow(幂), max(最大), min(最小)
- string_op: 字符串操作 {{"action_type":"string_op","string_type":"类型","input1":"字符串1","input2":"字符串2","result_var":"结果变量"}}
  string_type: concat(拼接), replace(替换), substring(截取), length(长度), upper(大写), lower(小写), trim(去空格), split(分割), join(连接), format(格式化), regex_extract(正则提取), regex_replace(正则替换)
- custom_api: 调用API {{"action_type":"custom_api","api_url":"URL","api_method":"GET/POST","api_headers":"{{}}","api_body":"","api_reply":"回复模板"}}

### 4. storage - 用户存储（每个用户独立数据）
data: {{"storage_type":"操作","storage_key":"键名","storage_value":"值","default_value":"默认值","result_var":"结果变量"}}
storage_type: get(读取), set(写入), incr(增加), decr(减少), delete(删除)
示例: {{"storage_type":"incr","storage_key":"score","storage_value":"10"}}

### 5. global_storage - 全局存储（所有用户共享）
data: {{"storage_type":"操作","storage_key":"键名","storage_value":"值","default_value":"默认值","result_var":"结果变量"}}
storage_type: get(读取), set(写入), incr(增加), decr(减少)

### 6. list_random - 随机抽取
data: {{"list_items":"选项1|选项2|选项3","weights":"权重1|权重2|权重3","result_var":"list_result","index_var":"list_index"}}
示例: {{"list_items":"金币x10|金币x50|钻石x1","weights":"70|20|10","result_var":"reward"}}

### 7. leaderboard - 排行榜
data: {{"leaderboard_type":"操作","leaderboard_key":"排序键","limit":10,"ascending":"false"}}
leaderboard_type: top(获取排行榜), my_rank(我的排名), count(统计人数)

### 8. delay - 延时
data: {{"seconds":秒数}}
示例: {{"seconds":3}}

### 9. set_var - 设置变量
data: {{"var_name":"变量名","var_value":"值"}}
示例: {{"var_name":"greeting","var_value":"你好{{user_id}}"}}

### 10. comment - 注释（不影响流程）
data: {{"comment_text":"备注内容"}}

## 可用变量
- {{user_id}} 用户QQ号
- {{group_id}} 群号
- {{content}} 消息内容
- {{$1}} {{$2}} 正则捕获组
- {{today}} 今日日期(YYYY-MM-DD)
- {{time}} 当前时间(HH:MM:SS)
- {{timestamp}} 时间戳
- {{random}} 随机数0-99
- {{random_100}} 随机数0-100
- {{storage.键名}} 读取用户存储
- {{global.键名}} 读取全局存储
- {{变量名}} 自定义变量
- {{math_result}} 数学运算默认结果
- {{api_response}} API原始响应
- {{api_json.字段}} API JSON字段

## 连接规则
- 普通节点输出: from_output="output_1"
- condition满足: from_output="output-1"
- condition不满足: from_output="output-2"

## 输出格式
{{"name":"工作流名","nodes":{{"node_1":{{...}}}},"connections":[{{"from_node":"node_1","from_output":"output_1","to_node":"node_2"}}]}}

## 完整示例：签到系统
用户需求: "触发签到，判断今日是否签到，未签到则随机5-10分，保存积分和日期，回复成功"
{{"name":"每日签到","nodes":{{"node_1":{{"id":"node_1","type":"trigger","x":100,"y":150,"data":{{"trigger_type":"exact","trigger_content":"签到"}}}},"node_2":{{"id":"node_2","type":"condition","x":280,"y":150,"data":{{"condition_type":"data_is_today","condition_value":"sign_date"}}}},"node_3":{{"id":"node_3","type":"action","x":460,"y":50,"data":{{"action_type":"reply_text","action_value":"今日已签到，请明天再来~"}}}},"node_4":{{"id":"node_4","type":"action","x":460,"y":250,"data":{{"action_type":"math","math_type":"random","operand1":"5","operand2":"10","result_var":"score"}}}},"node_5":{{"id":"node_5","type":"storage","x":640,"y":250,"data":{{"storage_type":"incr","storage_key":"total_score","storage_value":"{{score}}"}}}},"node_6":{{"id":"node_6","type":"storage","x":820,"y":250,"data":{{"storage_type":"set","storage_key":"sign_date","storage_value":"{{today}}"}}}},"node_7":{{"id":"node_7","type":"action","x":1000,"y":250,"data":{{"action_type":"reply_text","action_value":"签到成功！获得{{score}}积分，总积分{{storage.total_score}}"}}}}}},"connections":[{{"from_node":"node_1","from_output":"output_1","to_node":"node_2"}},{{"from_node":"node_2","from_output":"output-1","to_node":"node_3"}},{{"from_node":"node_2","from_output":"output-2","to_node":"node_4"}},{{"from_node":"node_4","from_output":"output_1","to_node":"node_5"}},{{"from_node":"node_5","from_output":"output_1","to_node":"node_6"}},{{"from_node":"node_6","from_output":"output_1","to_node":"node_7"}}]}}

只返回JSON，不要任何解释文字。'''
            
            log.info(f"[AI工作流] 发送请求到 {AI_SERVICE_URL}, 模型: {model}, prompt长度: {len(workflow_desc)}")
            
            with httpx.Client(timeout=120, verify=False) as client:
                response = client.post(AI_SERVICE_URL, json={
                    'action': 'workflow',
                    'description': description,  # 直接发送用户描述，AI服务会添加上下文
                    'model': model
                })
                
                if response.status_code != 200:
                    return {'success': False, 'message': f'AI服务请求失败: {response.status_code}'}
                
                result = response.json()
                log.info(f"[AI工作流] 响应字段: {list(result.keys())}")
                
                # 检查错误
                if not result.get('success'):
                    error_msg = result.get('message', 'AI服务错误')
                    raw = result.get('raw', '')
                    if raw:
                        error_msg += f" 原始: {raw[:200]}"
                    return {'success': False, 'message': error_msg}
                
                # PHP已经返回解析好的workflow对象
                workflow_data = result.get('workflow')
                if workflow_data and isinstance(workflow_data, dict):
                    log.info(f"[AI工作流] 成功获取工作流，节点数: {len(workflow_data.get('nodes', {}))}")
                    return {
                        'success': True,
                        'workflow': workflow_data,
                        'model': result.get('model', model)
                    }
                else:
                    return {'success': False, 'message': 'AI返回的工作流格式无效'}
                    
        except Exception as e:
            log.error(f"AI生成工作流失败: {e}")
            return {'success': False, 'message': str(e)}
    
    @classmethod
    def _parse_response(cls, ai_response, description):
        """解析AI响应"""
        log.info(f"[AI工作流] 开始解析响应，长度: {len(ai_response)}, 前500字符: {ai_response[:500]}")
        
        # 1. 尝试提取 ```json ... ``` 代码块
        code_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', ai_response)
        if code_block_match:
            json_str = code_block_match.group(1)
            log.info("[AI工作流] 从代码块提取JSON")
        else:
            # 2. 尝试匹配最外层的 { ... }
            json_match = re.search(r'\{[\s\S]*\}', ai_response)
            if json_match:
                json_str = json_match.group()
                log.info("[AI工作流] 从响应提取JSON对象")
            else:
                ai_response_stripped = ai_response.strip()
                if ai_response_stripped.startswith('{') and ai_response_stripped.endswith('}'):
                    json_str = ai_response_stripped
                    log.info("[AI工作流] 直接使用响应作为JSON")
                else:
                    log.error(f"[AI工作流] 响应中未找到JSON: {ai_response}")
                    return None
        
        # 清理JSON
        json_str_cleaned = cls._clean_json(json_str)
        
        try:
            workflow_data = json.loads(json_str_cleaned)
            log.info(f"[AI工作流] JSON解析成功，节点数: {len(workflow_data.get('nodes', {}))}")
        except json.JSONDecodeError as e:
            log.warning(f"[AI工作流] JSON解析失败: {e}")
            try:
                import ast
                workflow_data = ast.literal_eval(json_str)
                workflow_data = json.loads(json.dumps(workflow_data))
                log.info("[AI工作流] AST解析成功")
            except Exception as e2:
                log.error(f"[AI工作流] 解析失败: {e2}, 原始JSON: {json_str[:500]}")
                return None
        
        # 验证必要字段
        if 'nodes' not in workflow_data:
            workflow_data['nodes'] = {}
        if 'connections' not in workflow_data:
            workflow_data['connections'] = []
        if 'name' not in workflow_data:
            workflow_data['name'] = '新工作流'
        
        return workflow_data
    
    @classmethod
    def _clean_json(cls, s):
        """清理JSON字符串"""
        s = re.sub(r'//.*?$', '', s, flags=re.MULTILINE)
        s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
        s = re.sub(r"'(\w+)'(\s*:)", r'"\1"\2', s)
        s = re.sub(r":\s*'([^']*)'", r': "\1"', s)
        s = re.sub(r',(\s*[}\]])', r'\1', s)
        return s.strip()
    
    @classmethod
    def generate_node(cls, node_type, description, model='gpt-4o-mini', current_data=None):
        """AI生成单个节点配置"""
        try:
            import httpx
            
            if not description:
                return {'success': False, 'error': '请输入描述'}
            
            # 根据节点类型构建prompt - 更明确的指令
            node_prompts = {
                'trigger': f'''你是一个JSON生成器。根据用户需求生成QQ机器人触发器配置。

用户需求: {description}

你必须返回一个JSON对象，包含以下字段:
- trigger_type: 触发类型，可选值: exact(完全匹配), startswith(前缀匹配), contains(包含匹配), regex(正则匹配)
- trigger_content: 触发内容/关键词

示例1: 用户说"当发送签到时触发" -> {{"trigger_type":"exact","trigger_content":"签到"}}
示例2: 用户说"触发 测试" -> {{"trigger_type":"exact","trigger_content":"测试"}}
示例3: 用户说"匹配天气加城市名" -> {{"trigger_type":"regex","trigger_content":"天气 (.+)"}}

只返回JSON，不要任何解释文字。''',
                
                'condition': f'''你是一个JSON生成器。根据用户需求生成条件判断配置。

用户需求: {description}

你必须返回一个JSON对象，包含以下字段:
- condition_type: 条件类型
- condition_value: 条件值
- var_name: 变量名(可选)

condition_type可选值:
- contains: 内容包含某文字
- equals: 内容完全等于
- regex: 正则匹配
- random: 随机概率(填0-100的数字)
- data_is_today: 今日已操作(值填存储键名)
- data_equals/data_gt/data_lt: 存储数据比较
- var_equals/var_gt/var_lt: 变量比较

示例1: "判断今天是否签到" -> {{"condition_type":"data_is_today","condition_value":"sign_date"}}
示例2: "50%概率" -> {{"condition_type":"random","condition_value":"50"}}

只返回JSON。''',
                
                'action': f'''你是一个JSON生成器。根据用户需求生成动作节点配置。

用户需求: {description}

action_type可选:
- reply_text: 回复文字，设置action_value为回复内容
- reply_image: 回复图片，action_value填图片URL
- custom_api: 调用API，需要api_url, api_method(GET/POST), api_reply(回复模板)
- math: 数学运算，需要math_type(add/sub/mul/div), operand1, operand2, result_var

变量: {{user_id}}用户ID {{$1}}正则捕获组 {{data.xxx}}API返回字段 {{storage.xxx}}用户存储

示例1: "回复你好" -> {{"action_type":"reply_text","action_value":"你好"}}
示例2: "积分加10" -> {{"action_type":"math","math_type":"add","operand1":"{{storage.score}}","operand2":"10","result_var":"new_score"}}
示例3: "调用天气API" -> {{"action_type":"custom_api","api_url":"https://api.example.com/weather","api_method":"GET","api_reply":"天气: {{data.weather}}"}}

只返回JSON。''',
                
                'storage': f'''你是一个JSON生成器。根据用户需求生成用户存储配置。

用户需求: {description}

字段:
- storage_type: get(读取)/set(写入)/incr(增加)/decr(减少)/delete(删除)
- storage_key: 存储键名
- storage_value: 值(写入/增减时用)
- result_var: 结果变量名

示例1: "积分加10" -> {{"storage_type":"incr","storage_key":"score","storage_value":"10","result_var":"new_score"}}
示例2: "读取等级" -> {{"storage_type":"get","storage_key":"level","default_value":"1","result_var":"user_level"}}

只返回JSON。''',
                
                'global_storage': f'''你是一个JSON生成器。生成全局存储配置。

用户需求: {description}

字段: storage_type(get/set/incr/decr), storage_key, storage_value, result_var

示例: "全局计数加1" -> {{"storage_type":"incr","storage_key":"total_count","storage_value":"1","result_var":"total"}}

只返回JSON。''',
                
                'leaderboard': f'''你是一个JSON生成器。生成排行榜配置。

用户需求: {description}

字段:
- leaderboard_type: top(获取排行榜)/my_rank(我的排名)/count(统计人数)
- leaderboard_key: 排行的键名(如score, level等)
- limit: 显示数量
- ascending: true升序/false降序

示例: "积分榜前10" -> {{"leaderboard_type":"top","leaderboard_key":"score","limit":"10","ascending":"false"}}

只返回JSON。''',
                
                'list_random': f'''你是一个JSON生成器。生成随机抽取配置。

用户需求: {description}

字段:
- list_items: 用|分隔的选项列表
- weights: 对应权重(可选)
- result_var: 结果变量
- index_var: 索引变量

示例: "抽奖: 金币、钻石、SSR" -> {{"list_items":"金币x10|钻石x1|SSR卡","weights":"70|25|5","result_var":"prize"}}

只返回JSON。''',
                
                'delay': f'''你是一个JSON生成器。生成延时配置。

用户需求: {description}

字段: seconds(等待秒数)

示例: "等待3秒" -> {{"seconds":"3"}}

只返回JSON。''',
                
                'set_var': f'''你是一个JSON生成器。生成变量设置配置。

用户需求: {description}

字段:
- var_name: 变量名
- var_value: 变量值，支持{{$1}}等捕获组

示例: "保存城市名" -> {{"var_name":"city","var_value":"{{$1}}"}}

只返回JSON。''',
                
                'comment': f'''你是一个JSON生成器。生成注释配置。

用户需求: {description}

字段: comment_text(备注内容)

示例: "这是签到流程" -> {{"comment_text":"签到主流程"}}

只返回JSON。'''
            }
            
            prompt = node_prompts.get(node_type, f'生成{node_type}节点配置JSON。需求: {description}\n只返回JSON。')
            
            log.info(f"[AI节点] 类型={node_type}, 描述={description}, 模型={model}")
            
            with httpx.Client(timeout=60, verify=False) as client:
                response = client.post(AI_SERVICE_URL, json={
                    'action': 'create',
                    'filename': 'node_config.json',
                    'description': prompt,
                    'model': model
                })
                
                if response.status_code != 200:
                    log.error(f"[AI节点] HTTP错误: {response.status_code}")
                    # 失败时使用模板生成
                    return cls._generate_node_fallback(node_type, description)
                
                result = response.json()
                log.info(f"[AI节点] 原始响应: {str(result)[:500]}")
                
                if result.get('error'):
                    log.error(f"[AI节点] 服务错误: {result.get('message')}")
                    return cls._generate_node_fallback(node_type, description)
                
                # 尝试多个字段获取AI响应
                ai_response = (result.get('response') or result.get('content') or 
                              result.get('message') or result.get('code') or 
                              result.get('reply') or result.get('text') or '')
                
                if not ai_response:
                    log.error(f"[AI节点] 响应为空，使用备用方案")
                    return cls._generate_node_fallback(node_type, description)
                
                log.info(f"[AI节点] AI响应: {ai_response[:300]}")
                
                # 解析JSON
                node_data = cls._parse_node_response(ai_response)
                if node_data and cls._validate_node_data(node_type, node_data):
                    return {'success': True, 'node_data': node_data}
                else:
                    log.warning(f"[AI节点] 解析失败或数据无效，使用备用方案")
                    return cls._generate_node_fallback(node_type, description)
                    
        except Exception as e:
            log.error(f"AI生成节点失败: {e}")
            return cls._generate_node_fallback(node_type, description)
    
    @classmethod
    def _validate_node_data(cls, node_type, data):
        """验证节点数据是否有效"""
        if not isinstance(data, dict):
            return False
        # 检查是否包含无关字段（如handler, owner_only）
        if 'handler' in data or 'owner_only' in data:
            return False
        # 根据节点类型检查必要字段
        required_fields = {
            'trigger': ['trigger_type', 'trigger_content'],
            'condition': ['condition_type'],
            'action': ['action_type'],
            'storage': ['storage_type', 'storage_key'],
            'global_storage': ['storage_type', 'storage_key'],
            'leaderboard': ['leaderboard_type', 'leaderboard_key'],
            'list_random': ['list_items'],
            'delay': ['seconds'],
            'set_var': ['var_name'],
            'comment': ['comment_text']
        }
        fields = required_fields.get(node_type, [])
        # 至少有一个有效字段
        return any(f in data for f in fields) if fields else True
    
    @classmethod
    def _generate_node_fallback(cls, node_type, description):
        """备用方案：基于规则生成节点配置"""
        import re as regex
        
        log.info(f"[AI节点] 使用备用方案: {node_type}, {description}")
        
        # 从描述中提取关键信息
        desc = description.strip()
        
        if node_type == 'trigger':
            # 提取触发词
            # 尝试匹配 "触发 xxx" 或直接使用描述
            match = regex.search(r'触发\s*[：:]*\s*(.+)', desc)
            if match:
                trigger_content = match.group(1).strip()
            else:
                # 移除常见前缀词
                trigger_content = regex.sub(r'^(当|用户|发送|输入|说)\s*', '', desc)
                trigger_content = regex.sub(r'\s*(时|的时候|触发)$', '', trigger_content)
            
            # 判断是否需要正则
            if '(' in trigger_content or ')' in trigger_content or '.*' in trigger_content:
                trigger_type = 'regex'
            elif '+' in desc or '加' in desc:
                # 如 "天气+城市" -> 正则
                parts = regex.split(r'[+＋加]', trigger_content)
                if len(parts) > 1:
                    trigger_type = 'regex'
                    trigger_content = parts[0].strip() + ' (.+)'
                else:
                    trigger_type = 'exact'
            else:
                trigger_type = 'exact'
            
            return {'success': True, 'node_data': {
                'trigger_type': trigger_type,
                'trigger_content': trigger_content or desc
            }}
        
        elif node_type == 'condition':
            # 条件判断
            if '今天' in desc or '今日' in desc:
                # 今日已操作类
                key = 'last_action_date'
                if '签到' in desc:
                    key = 'sign_date'
                return {'success': True, 'node_data': {
                    'condition_type': 'data_is_today',
                    'condition_value': key
                }}
            elif '%' in desc or '概率' in desc or '随机' in desc:
                # 随机概率
                match = regex.search(r'(\d+)\s*%?', desc)
                prob = match.group(1) if match else '50'
                return {'success': True, 'node_data': {
                    'condition_type': 'random',
                    'condition_value': prob
                }}
            else:
                return {'success': True, 'node_data': {
                    'condition_type': 'contains',
                    'condition_value': desc
                }}
        
        elif node_type == 'action':
            # 动作
            if 'api' in desc.lower() or 'http' in desc.lower() or '接口' in desc:
                return {'success': True, 'node_data': {
                    'action_type': 'custom_api',
                    'api_url': '',
                    'api_method': 'GET',
                    'api_reply': '{api_response}'
                }}
            elif '加' in desc or '增' in desc or '减' in desc:
                # 数学运算
                op = 'add' if ('加' in desc or '增' in desc) else 'sub'
                match = regex.search(r'(\d+)', desc)
                amount = match.group(1) if match else '10'
                return {'success': True, 'node_data': {
                    'action_type': 'math',
                    'math_type': op,
                    'operand1': '{storage.score}',
                    'operand2': amount,
                    'result_var': 'new_value'
                }}
            else:
                # 默认回复
                return {'success': True, 'node_data': {
                    'action_type': 'reply_text',
                    'action_value': desc if len(desc) < 50 else '收到'
                }}
        
        elif node_type == 'storage':
            if '加' in desc or '增' in desc:
                op = 'incr'
            elif '减' in desc:
                op = 'decr'
            elif '读' in desc or '获取' in desc:
                op = 'get'
            elif '删' in desc:
                op = 'delete'
            else:
                op = 'set'
            
            # 提取数值
            match = regex.search(r'(\d+)', desc)
            value = match.group(1) if match else '1'
            
            # 提取键名
            key = 'score'
            if '积分' in desc:
                key = 'score'
            elif '等级' in desc:
                key = 'level'
            elif '金币' in desc:
                key = 'coins'
            
            return {'success': True, 'node_data': {
                'storage_type': op,
                'storage_key': key,
                'storage_value': value if op in ['set', 'incr', 'decr'] else '',
                'result_var': 'data_result'
            }}
        
        elif node_type == 'delay':
            match = regex.search(r'(\d+)', desc)
            seconds = match.group(1) if match else '1'
            return {'success': True, 'node_data': {'seconds': seconds}}
        
        elif node_type == 'set_var':
            return {'success': True, 'node_data': {
                'var_name': 'temp',
                'var_value': '{$1}'
            }}
        
        elif node_type == 'list_random':
            return {'success': True, 'node_data': {
                'list_items': '选项1|选项2|选项3',
                'result_var': 'list_result'
            }}
        
        elif node_type == 'leaderboard':
            return {'success': True, 'node_data': {
                'leaderboard_type': 'top',
                'leaderboard_key': 'score',
                'limit': '10',
                'ascending': 'false'
            }}
        
        elif node_type == 'comment':
            return {'success': True, 'node_data': {
                'comment_text': desc
            }}
        
        else:
            return {'success': True, 'node_data': {}}
    
    @classmethod
    def _parse_node_response(cls, ai_response):
        """解析AI节点响应"""
        # 1. 尝试提取 ```json ... ``` 代码块
        code_block_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', ai_response)
        if code_block_match:
            json_str = code_block_match.group(1)
        else:
            # 2. 尝试匹配 { ... }
            json_match = re.search(r'\{[^{}]*\}', ai_response)
            if json_match:
                json_str = json_match.group()
            else:
                ai_response_stripped = ai_response.strip()
                if ai_response_stripped.startswith('{') and ai_response_stripped.endswith('}'):
                    json_str = ai_response_stripped
                else:
                    return None
        
        # 清理JSON
        json_str = cls._clean_json(json_str)
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            try:
                import ast
                data = ast.literal_eval(json_str)
                return json.loads(json.dumps(data))
            except:
                return None
