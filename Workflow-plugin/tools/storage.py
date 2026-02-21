# -*- coding: utf-8 -*-
"""工作流数据存储模块 - 包含工作流配置和用户游戏数据存储"""

import os
import json
import logging
import threading

log = logging.getLogger(__name__)

# 数据目录放在工作流插件文件夹内
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
WORKFLOW_FILE = os.path.join(DATA_DIR, 'visual_workflows.json')
USER_DATA_FILE = os.path.join(DATA_DIR, 'workflow_user_data.json')
os.makedirs(DATA_DIR, exist_ok=True)

_user_data_cache = None
_user_data_lock = threading.Lock()


def load_workflows():
    """加载工作流配置"""
    try:
        log.debug(f"[工作流存储] 加载文件: {WORKFLOW_FILE}, 存在: {os.path.exists(WORKFLOW_FILE)}")
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                log.debug(f"[工作流存储] 加载成功, 数量: {len(data)}")
                return data
    except Exception as e:
        log.error(f"[工作流存储] 加载失败: {e}")
    return []


def save_workflows(workflows):
    """保存工作流配置"""
    try:
        log.info(f"[工作流存储] 保存到: {WORKFLOW_FILE}, 数量: {len(workflows)}")
        # 确保目录存在
        os.makedirs(os.path.dirname(WORKFLOW_FILE), exist_ok=True)
        with open(WORKFLOW_FILE, 'w', encoding='utf-8') as f:
            json.dump(workflows, f, ensure_ascii=False, indent=2)
        log.info(f"[工作流存储] 保存成功")
        return True
    except Exception as e:
        log.error(f"[工作流存储] 保存失败: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False


# ========== 用户数据存储 (用于游戏等场景) ==========

def _load_user_data():
    """加载用户数据缓存"""
    global _user_data_cache
    if _user_data_cache is None:
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    _user_data_cache = json.load(f)
            else:
                _user_data_cache = {}
        except Exception as e:
            log.error(f"加载用户数据失败: {e}")
            _user_data_cache = {}
    return _user_data_cache


def _save_user_data():
    """保存用户数据到文件"""
    global _user_data_cache
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(_user_data_cache or {}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log.error(f"保存用户数据失败: {e}")
        return False


def get_user_value(user_id, key, default=None):
    """获取用户数据
    Args:
        user_id: 用户ID
        key: 数据键名 (如 'score', 'level', 'inventory')
        default: 默认值
    Returns:
        存储的值，不存在则返回default
    """
    with _user_data_lock:
        data = _load_user_data()
        user_data = data.get(str(user_id), {})
        return user_data.get(key, default)


def set_user_value(user_id, key, value):
    """设置用户数据
    Args:
        user_id: 用户ID
        key: 数据键名
        value: 要存储的值
    Returns:
        是否成功
    """
    with _user_data_lock:
        data = _load_user_data()
        user_id = str(user_id)
        if user_id not in data:
            data[user_id] = {}
        data[user_id][key] = value
        return _save_user_data()


def incr_user_value(user_id, key, amount=1, default=0):
    """增加用户数值 (原子操作)
    Args:
        user_id: 用户ID
        key: 数据键名
        amount: 增加的数量 (可为负数)
        default: 初始默认值
    Returns:
        增加后的新值
    """
    with _user_data_lock:
        data = _load_user_data()
        user_id = str(user_id)
        if user_id not in data:
            data[user_id] = {}
        current = data[user_id].get(key, default)
        try:
            new_value = float(current) + float(amount)
            if new_value == int(new_value):
                new_value = int(new_value)
            data[user_id][key] = new_value
            _save_user_data()
            return new_value
        except (ValueError, TypeError):
            return current


def delete_user_value(user_id, key):
    """删除用户数据"""
    with _user_data_lock:
        data = _load_user_data()
        user_id = str(user_id)
        if user_id in data and key in data[user_id]:
            del data[user_id][key]
            _save_user_data()
            return True
        return False


def get_all_user_data(user_id):
    """获取用户的所有数据"""
    with _user_data_lock:
        data = _load_user_data()
        return data.get(str(user_id), {}).copy()


def clear_user_data(user_id):
    """清空用户的所有数据"""
    with _user_data_lock:
        data = _load_user_data()
        user_id = str(user_id)
        if user_id in data:
            del data[user_id]
            _save_user_data()
            return True
        return False


# ========== 全局存储 (跨用户共享) ==========

GLOBAL_DATA_FILE = os.path.join(DATA_DIR, 'workflow_global_data.json')
_global_data_cache = None
_global_data_lock = threading.Lock()


def _load_global_data():
    """加载全局数据"""
    global _global_data_cache
    if _global_data_cache is None:
        try:
            if os.path.exists(GLOBAL_DATA_FILE):
                with open(GLOBAL_DATA_FILE, 'r', encoding='utf-8') as f:
                    _global_data_cache = json.load(f)
            else:
                _global_data_cache = {}
        except Exception as e:
            log.error(f"加载全局数据失败: {e}")
            _global_data_cache = {}
    return _global_data_cache


def _save_global_data():
    """保存全局数据"""
    global _global_data_cache
    try:
        with open(GLOBAL_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(_global_data_cache or {}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log.error(f"保存全局数据失败: {e}")
        return False


def get_global_value(key, default=None):
    """获取全局数据"""
    with _global_data_lock:
        data = _load_global_data()
        return data.get(key, default)


def set_global_value(key, value):
    """设置全局数据"""
    with _global_data_lock:
        data = _load_global_data()
        data[key] = value
        return _save_global_data()


def incr_global_value(key, amount=1, default=0):
    """增加全局数值"""
    with _global_data_lock:
        data = _load_global_data()
        current = data.get(key, default)
        try:
            new_value = float(current) + float(amount)
            if new_value == int(new_value):
                new_value = int(new_value)
            data[key] = new_value
            _save_global_data()
            return new_value
        except (ValueError, TypeError):
            return current


# ========== 排行榜功能 ==========

def get_leaderboard(key, limit=10, ascending=False):
    """获取排行榜
    Args:
        key: 排行的数据键名 (如 'score', 'coins')
        limit: 返回数量
        ascending: True为升序(最小在前)，False为降序(最大在前)
    Returns:
        [(user_id, value), ...] 排序后的列表
    """
    with _user_data_lock:
        data = _load_user_data()
        results = []
        for user_id, user_data in data.items():
            if key in user_data:
                try:
                    value = float(user_data[key])
                    results.append((user_id, value))
                except (ValueError, TypeError):
                    pass
        
        results.sort(key=lambda x: x[1], reverse=not ascending)
        return results[:limit]


def get_user_rank(user_id, key, ascending=False):
    """获取用户排名
    Args:
        user_id: 用户ID
        key: 排行的数据键名
        ascending: 排序方式
    Returns:
        (rank, value, total) 排名从1开始，未上榜返回(0, 0, total)
    """
    with _user_data_lock:
        data = _load_user_data()
        results = []
        for uid, user_data in data.items():
            if key in user_data:
                try:
                    value = float(user_data[key])
                    results.append((uid, value))
                except (ValueError, TypeError):
                    pass
        
        results.sort(key=lambda x: x[1], reverse=not ascending)
        total = len(results)
        
        user_id = str(user_id)
        for i, (uid, value) in enumerate(results):
            if uid == user_id:
                return (i + 1, value, total)
        
        return (0, 0, total)


def count_users_with_key(key):
    """统计拥有某个键的用户数量"""
    with _user_data_lock:
        data = _load_user_data()
        count = 0
        for user_data in data.values():
            if key in user_data:
                count += 1
        return count
