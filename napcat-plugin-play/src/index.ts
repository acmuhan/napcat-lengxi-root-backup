// NapCat Play 娱乐插件 @author 冷曦 @version 1.1.0
import type { PluginModule, NapCatPluginContext, PluginConfigSchema, PluginConfigUIController } from 'napcat-types/napcat-onebot/network/plugin-manger';
import type { OB11Message } from 'napcat-types/napcat-onebot/types/index';
import fs from 'fs';
import path, { dirname } from 'path';
import type { PluginConfig } from './types';
import { DEFAULT_PLUGIN_CONFIG } from './config';
import { pluginState } from './core/state';
import { handleMemeCommand } from './handlers/meme-handler';
import { handleMusicCommand } from './handlers/music-handler';
import { handleMenuCommand } from './handlers/menu-handler';
import { handleDrawCommand } from './handlers/draw-handler';
import { initMemeData } from './services/meme-service';
import { initAutoSign, stopAutoSign } from './services/auto-sign';
import { sendRecord, sendReply } from './utils/message';

export let plugin_config_ui: PluginConfigSchema = [];

// 插件初始化
const plugin_init: PluginModule['plugin_init'] = async (ctx: NapCatPluginContext) => {
  Object.assign(pluginState, {
    logger: ctx.logger,
    actions: ctx.actions,
    adapterName: ctx.adapterName,
    networkConfig: ctx.pluginManager.config,
  });
  pluginState.log('info', 'Play 娱乐插件正在初始化...');

  // 配置 UI
  plugin_config_ui = ctx.NapCatConfig.combine(
    ctx.NapCatConfig.html('<div style="padding:10px;background:#f5f5f5;border-radius:8px;margin-bottom:10px"><b>🎮 Play 娱乐插件</b><br/><span style="color:#666;font-size:13px">发送 <code>娱乐菜单</code> 查看指令 | 交流群：<a href="https://qm.qq.com/q/oB5hdOZcuQ" target="_blank">1085402468</a></span></div>'),
    // 功能开关
    ctx.NapCatConfig.html('<b>📌 功能开关</b>'),
    ctx.NapCatConfig.boolean('enableMeme', '表情包功能', true, '启用 meme 表情包制作'),
    ctx.NapCatConfig.boolean('enableMusic', '点歌功能', true, '启用 QQ 音乐点歌'),
    ctx.NapCatConfig.boolean('enableDraw', 'AI绘画功能', true, '启用 AI 绘画'),
    ctx.NapCatConfig.text('prefix', 'Meme前缀', '', '仅表情包功能需要前缀'),
    // API 配置
    ctx.NapCatConfig.html('<b>🔧 API 配置</b>'),
    ctx.NapCatConfig.text('memeApiUrl', 'Meme API', 'http://datukuai.top:2233', 'meme 服务地址'),
    ctx.NapCatConfig.text('musicApiUrl', '音乐 API', 'https://a.aa.cab', '点歌服务地址'),
    ctx.NapCatConfig.text('drawApiUrl', '绘画 API', 'https://i.elaina.vin/api/openai', 'AI 绘画服务地址'),
    // 其他设置
    ctx.NapCatConfig.html('<b>⚙️ 其他设置</b>'),
    ctx.NapCatConfig.select('maxFileSize', '图片大小限制', [5, 10, 20].map(n => ({ label: `${n}MB`, value: n })), 10),
    ctx.NapCatConfig.boolean('enableMasterProtect', '主人保护', true, '所有 meme 对主人反向操作'),
    ctx.NapCatConfig.text('ownerQQs', '主人QQ', '', '多个用逗号分隔'),
    ctx.NapCatConfig.boolean('debug', '调试模式', false, '显示详细日志')
  );

  // 加载配置
  if (fs.existsSync(ctx.configPath)) {
    pluginState.config = { ...DEFAULT_PLUGIN_CONFIG, ...JSON.parse(fs.readFileSync(ctx.configPath, 'utf-8')) };
  }

  // 初始化数据
  pluginState.dataPath = ctx.configPath ? dirname(ctx.configPath) : path.join(process.cwd(), 'data', 'napcat-plugin-play');
  if (pluginState.config.enableMeme) initMemeData().catch(() => { });

  initAutoSign(pluginState.dataPath).catch(() => { });

  pluginState.log('info', 'Play 娱乐插件初始化完成');
};

// 获取配置
export const plugin_get_config = async (): Promise<PluginConfig> => pluginState.config;

// 保存配置
export const plugin_set_config = async (ctx: NapCatPluginContext, config: PluginConfig): Promise<void> => {
  const old = { ...pluginState.config };
  pluginState.config = config;

  // 启用 meme 时初始化数据
  if (config.enableMeme && !old.enableMeme && !pluginState.initialized) {
    initMemeData().catch(() => { });
  }

  // 保存到文件
  if (ctx?.configPath) {
    const resolved = path.resolve(ctx.configPath);
    if (!resolved.includes('napcat')) return;
    const dir = path.dirname(resolved);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(resolved, JSON.stringify(config, null, 2), 'utf-8');
  }
};

// 响应式配置控制器
const plugin_config_controller = (_ctx: NapCatPluginContext, ui: PluginConfigUIController, config: Record<string, unknown>): (() => void) | void => {
  const toggle = (fields: string[], show: boolean) => fields.forEach(f => show ? ui.showField(f) : ui.hideField(f));
  toggle(['memeApiUrl', 'maxFileSize', 'enableMasterProtect', 'ownerQQs'], config.enableMeme !== false);
  toggle(['musicApiUrl'], config.enableMusic !== false);
  toggle(['drawApiUrl'], config.enableDraw !== false);
  return () => { };
};

// 响应式配置变更
const plugin_on_config_change = (_ctx: NapCatPluginContext, ui: PluginConfigUIController, key: string, _value: unknown, config: Record<string, unknown>): void => {
  const toggle = (fields: string[], show: boolean) => fields.forEach(f => show ? ui.showField(f) : ui.hideField(f));

  if (key === 'enableMeme') toggle(['memeApiUrl', 'maxFileSize', 'enableMasterProtect', 'ownerQQs'], config.enableMeme !== false);
  if (key === 'enableMusic') toggle(['musicApiUrl'], config.enableMusic !== false);
  if (key === 'enableDraw') toggle(['drawApiUrl'], config.enableDraw !== false);
};

// 插件清理
const plugin_cleanup: PluginModule['plugin_cleanup'] = async () => {
  stopAutoSign();
  pluginState.log('info', 'Play 娱乐插件已卸载');
};

// 消息处理
const plugin_onmessage: PluginModule['plugin_onmessage'] = async (ctx: NapCatPluginContext, event: OB11Message) => {
  if (event.post_type !== 'message') return;

  const raw = event.raw_message || '';

  const text = raw.replace(/\[CQ:[^\]]+\]/g, '').trim();

  // 哈基米：随机语音
  if (text === '哈基米') {
    await sendRecord(event, 'https://i.elaina.vin/api/%E5%93%88%E5%9F%BA%E7%B1%B3/', ctx);
    return;
  }

  // 自闭：自我禁言（仅群聊）
  const selfMuteMatch = text.match(/^自闭\s*(\d+)$/);
  if (selfMuteMatch && event.message_type === 'group') {
    const minutes = Math.min(Math.max(parseInt(selfMuteMatch[1], 10) || 1, 1), 43200);
    await ctx.actions.call('set_group_ban', {
      group_id: String(event.group_id), user_id: String(event.user_id), duration: minutes * 60,
    } as never, ctx.adapterName, ctx.pluginManager.config).catch(() => { });
    await sendReply(event, `好的，已帮你自闭 ${minutes} 分钟 🤐`, ctx);
    return;
  }

  // 按优先级处理命令
  if (await handleMenuCommand(event, raw, ctx)) return;
  if (pluginState.config.enableMusic && await handleMusicCommand(event, raw, ctx)) return;
  if (pluginState.config.enableDraw && await handleDrawCommand(event, raw, ctx)) return;
  if (pluginState.config.enableMeme) await handleMemeCommand(event, raw, ctx);
};

export { plugin_init, plugin_onmessage, plugin_cleanup, plugin_config_controller, plugin_on_config_change };
