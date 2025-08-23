
import {trackerMapping} from "./trackerMapping";

export const PLUGIN_ID = "SeedCleaner"
export const ONLY_TORRENT = "only_torrent" //仅种子
export const ONLY_DATA = "only_data" //仅数据
export const ALL = "all" //全部
/**
 * 字节格式化,转化字节为B，KB,MB...字符串
 * @param {*} a 字节数
 * @param {*} b 保留几位小数
 */
export function formatBytes(a: number, b: number = 2) {
    if (0 == a) return "0 B";
    var c = 1024, d = b || 2, e = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
        f = Math.floor(Math.log(a) / Math.log(c));
    return parseFloat((a / Math.pow(c, f)).toFixed(d)) + " " + e[f];
}


export const copyPath = async (path: string) => {
  if (window.isSecureContext && navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(path);
      return true;
    } catch (err) {
      console.error("现代剪贴板API复制失败", err);
      return false
    }
  }
  // 使用兼容方案并防止滚动跳动
  const textArea = document.createElement("textarea");
  textArea.value = path;
  Object.assign(textArea.style, {
    position: "absolute",
    left: "-9999px",
    top: "-9999px",
    opacity: "0"
  });
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand("copy");
    return true;
  } catch (err) {
    console.error("兼容方案复制失败", err);
    return false
  } finally {
    document.body.removeChild(textArea);
  }
}

export const mapTrackers = (trackers: string[]): string[] => {
  if (!Array.isArray(trackers)) return [];
  return trackers.map((tracker) => {

    if (trackerMapping[tracker]){
      return trackerMapping[tracker];
    }
    // 去除协议部分（如果存在）
    let hostname = tracker.replace(/^[a-zA-Z0-9+.-]+:\/{2}/, '');
    // 去除路径、端口等，只保留主机名
    hostname = hostname.split('/')[0].split(':')[0];
    // 分割域名
    const parts = hostname.split('.');
    // 用各部分匹配
    for (let part of parts){
      if (trackerMapping[part]){
        return trackerMapping[part];
     }
    }
    // 无法匹配时返回原值
    return tracker;
  });
};

// 字符串格式化:value为0返回空
const getStrUnit = (value:number,unit:string)=>{
  if (value!=0){
    return value.toFixed(0)+unit
  }else{
    return ""
  }
}
// 时长计算及格式化
export function formatTimeSince(_targetTime: string|Date): string {
  // 解析目标时间
    let targetTime: Date;
    if (typeof _targetTime === 'string'){
      targetTime = new Date(_targetTime);
    }else{
      targetTime = _targetTime
    }
  
    const now = new Date();
    // 计算时间差（毫秒）
    const diffMs = now.getTime() - targetTime.getTime();
    // 如果目标时间在未来，返回空字符串或适当处理
    if (diffMs < 0) {
        return "目标时间在未来";
    }
    // 计算各个时间单位
    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const weeks = Math.floor(days / 7);
    // 计算月和年（近似值）
    const targetYear = targetTime.getFullYear();
    const targetMonth = targetTime.getMonth();
    const currentYear = now.getFullYear();
    const currentMonth = now.getMonth();
    let months = (currentYear - targetYear) * 12 + (currentMonth - targetMonth);
    // 如果当前日期小于目标日期，减少一个月
    if (now.getDate() < targetTime.getDate()) {
        months--;
    }
    const years = Math.floor(months / 12);
    // 根据规则格式化输出
    if (seconds < 60) {
        return `${seconds}秒`;
    } else if (minutes < 60) {
        return `${minutes}分钟`;
    } else if (hours < 24) {
        const remainingMinutes = minutes % 60;
        return `${getStrUnit(hours,'小时')}${getStrUnit(remainingMinutes,'分钟')}`;
    } else if (days < 7) {
        const remainingHours = hours % 24;
        return `${getStrUnit(days,'天')}${getStrUnit(remainingHours,'小时')}`;
    } else if (months < 1) {
        const remainingDays = days % 7;
        return `${getStrUnit(weeks,'周')}${getStrUnit(remainingDays,'天')}`;
    } else if (years < 1) {
        const remainingWeeks = Math.floor((days % 30) / 7); // 近似计算
        const remainingDays = days % 7;
        return `${getStrUnit(months,'月')}${getStrUnit(remainingWeeks,'周')}${getStrUnit(remainingDays,'天')}`;
    } else {
        const remainingMonths = months % 12;
        const remainingWeeks = Math.floor((days % 365) / 30 / 7); // 近似计算
        const remainingDays = days % 7;
        return `${getStrUnit(years,'年')}${getStrUnit(remainingMonths,'月')}${getStrUnit(remainingWeeks,'周')}${getStrUnit(remainingDays,'天')}`;
    }
}


// 获取状态颜色
export const getStatusColor = (status: string) => {
  let error_status = ['缺失源文件' , '错误' , '已停止' , '未知']
  if (error_status.includes(status)) {
    return 'error';
  } else {
    return 'success';
  }
};


const availableColors = ['primary','#E91E63','#FFC107','#03A9F4','success','#3F51B5', 'info', 'warning', '#F44336', '#009688'];
// 根据字符串生成颜色索引
export const getColorByString = (strs: string[]): string => {
  let strsArray = strs.sort()
  let _strs = strsArray.join("");
  let hash = 0;
  for (let i = 0; i < _strs.length; i++) {
    hash = _strs.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash % availableColors.length);
  return availableColors[index];
};
// 获取随机颜色
export const getRandomColor = (num: number) => {
  const index = Math.floor(num % availableColors.length);
  return availableColors[index];
};



// Define Anchor type locally if needed
type Anchor = 'top' | 'bottom' | 'left' | 'right' | 'center';

export interface ApiRequest {
  get: <T>(url: string, config?: any) => Promise<T>;
  post: <T>(url: string, data?: any, config?: any) => Promise<T>;
  put: <T>(url: string, data?: any, config?: any) => Promise<T>;
  delete: <T>(url: string, config?: any) => Promise<T>;
  patch: <T>(url: string, data?: any, config?: any) => Promise<T>;
}
// definedFunctions.ts


interface BaseItem {
  name: string;
  hash: string;
  size: number;
  path: string;
  client?: string;
}

interface TorrentItem extends BaseItem {
  type: 'torrent';
  client_name:string;
  trackers: string[];
  data_missing: boolean;
  removeOption: string;
  seeds: number;
  status: string;
  error: string;
  created_at:string;
}

interface SourceFileItem extends BaseItem {
  type: 'file';
}

export type CombinedItem = TorrentItem | SourceFileItem;

export interface ScanResult {
  combinedList: CombinedItem[];
  total: number;
  totalSize:number;
  tTotal: number; // 种子总数
  tTotalSize: number;
  mTotal: number; // 缺失种子的文件总数
  mTotalSize:number;
  page: number;
  pageSize: number;
}


export interface SnackbarModel {
  show: boolean;
  message: string;
  color: string;
  location:Anchor;
}

export interface DownloaderInfoModel {
  name: string;
  type: string; // 下载器类型: qbittorrent,transmission
  host: string;
  port: number;
  username: string;
  password: string;
}

export interface DownloaderModel {
  system: DownloaderInfoModel[];
  custom: DownloaderInfoModel[];
}

export type SortItem = { key: string, order: null| boolean | 'asc' | 'desc' }


export interface FilterModel{
  path: string
  client_name:string
  client:string
  seeds_limit_down:number|null
  seeds_limit_up:number|null
  seeds_limit:Array<number|null>
  size_limit_down:number|null
  size_limit_up:number|null
  size_limit:Array<number|null>
  live_time:number
}