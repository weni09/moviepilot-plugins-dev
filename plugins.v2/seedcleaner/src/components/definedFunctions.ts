
import {trackerMapping} from "./trackerMapping";

// Define Anchor type locally if needed
type Anchor = 'top' | 'bottom' | 'left' | 'right' | 'center';

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
}

interface SourceFileItem extends BaseItem {
  type: 'file';
}

export type CombinedItem = TorrentItem | SourceFileItem;

export interface ScanResult {
  combinedList: CombinedItem[];
  total: number;
  tTotal: number; // 种子总数
  mTotal: number; // 缺失种子的文件总数
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