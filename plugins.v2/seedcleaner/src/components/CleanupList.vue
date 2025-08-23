<template>
  <v-card flat class="cleanup-list-card">
    <v-card-title class="cleanup-list-title d-flex align-center px-4 py-3">
      <div class="title-left d-flex align-center">
        <div class="title-content">
          <div class="title-stats d-flex align-center">
            <v-chip class="mr-2" size="small" color="error" variant="flat" v-if="state.cleanupList.length > 0">
              <v-icon size="14" class="mr-1">mdi-delete</v-icon>
              数量：{{ state.cleanupList.length }}, 总大小：{{ totalSize }}
            </v-chip>
          </div>
        </div>
      </div>
      <v-spacer />
      <div class="title-actions d-flex align-center">
        <!-- <v-btn color="error"
               @click="deleteAllRecord"
               icon
               size="small"
               :disabled="state.cleanupList.length === 0">
          <v-icon icon="mdi-broom" size="small"/>
          <v-tooltip activator="parent" location="top">清空记录</v-tooltip>
        </v-btn> -->
      </div>
    </v-card-title>
    
    <v-card-text class="pa-0">
      <div style="min-height: 260px; max-height: 420px; overflow-y: auto;">
        <!-- 卡片网格布局 -->
        <v-row v-if="state.cleanupList.length > 0" class="pa-2" no-gutters>
          <v-col 
            v-for="(item,index) in state.cleanupList" 
            :key="item.hash || item.path"
            cols="12" 
            sm="6" 
            md="4" 
            lg="4"
            class="pa-1 d-flex"
          >
            <v-card 
              :class="[
                'cleanup-card-horizontal', 
                { 'qb-card': item.hasOwnProperty('client') && item.client !== 'transmission' },
                { 'tr-card': item.hasOwnProperty('client') && item.client === 'transmission' }
              ]"
              elevation="1"
              hover
              class="flex-grow-1"
            >
              <!-- 卡片头部 - 横向布局 -->
               <div class="card-header-horizontal pa-2">
                 <div class="d-flex align-center justify-space-between mb-2">
                    <v-row class="d-flex align-center" no-gutters>
                    <v-col :cols="1" class="px-0 py-0">
                      <!-- 移除按钮 -->
                      <v-btn
                        size="x-small"
                        variant="text"
                        color="error"
                        @click.stop="removeFromCleanup(item)"
                        icon="mdi-delete"
                      />
                     </v-col>
                     <v-col :cols="10" class="px-1 py-0">
                     <span class="file-name-horizontal text-body-2">
                       {{ item.name }}
                     </span></v-col>
                     <v-col :cols="1" class="px-0 py-0">
                      <v-btn
                        size="x-small"
                        variant="text"
                        color="primary"
                        @click.stop="_copyPath(item.path)"
                        icon="mdi-content-copy"/>
                        </v-col>
                   </v-row>
                  </div>
                </div>

              <!-- 卡片内容 - 横向信息展示 -->
              <div class="card-content-horizontal pa-2 pt-0">
                <!-- 删除选项标签行 -->
                <div class="d-flex align-center flex-wrap gap-1 mb-1">
                  <v-chip
                    :color="deleteOptionText(item).color"
                    size="x-small"
                    text-color="white"
                    class="delete-option-chip"
                  >
                    {{ deleteOptionText(item).text }}
                  </v-chip>
                  
                  <!-- 类型标签 -->
                  <v-chip
                    :color="item.type === 'torrent' ? 'warning' : 'error'"
                    text-color="white"
                    size="x-small"
                    class="type-chip ml-2"
                  >
                    {{ item.type === 'torrent' ? '种子' : '文件' }}
                  </v-chip>
                </div>

                <!-- 详细信息 - 横向网格布局 -->
                <div class="info-grid-horizontal">
                  <div class="info-item">
                    <v-icon size="14" color="info" class="mr-1">mdi-database</v-icon>
                    <span class="text-caption">{{ itemSizeText(item) }}</span>
                  </div>
                   <div class="info-item">
                    <v-icon size="14" :color="item.type == 'torrent'?getStatusColor(item.status):'error'" class="mr-1">mdi-chart-timeline-variant</v-icon>
                    <span class="text-caption text-truncate">{{ `${item.type == 'torrent'?item.status:'缺失种子' }` }}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" :color="item.type == 'torrent'?getColorByString(item?.trackers):'primary'" class="mr-1">mdi-tag</v-icon>
                    <span class="text-caption">{{ item.type === 'torrent' && item?.trackers.length > 0 ? mapTrackers(item.trackers)[0] : '无' }}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" color="warning" class="mr-1">mdi-clock-outline</v-icon>
                    <span class="text-caption">{{ item.type === 'torrent' && item.created_at ? formatCreatedTime(item.created_at) : '-' }}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" color="success" class="mr-1">mdi-seed</v-icon>
                    <span class="text-caption">{{ item.type === 'torrent' ? `${item.seeds || 0}`:'无'}}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" color="cyan" class="mr-1">mdi-folder</v-icon>
                    <span class="text-caption text-truncate" :title="item.path">{{ item.path }}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" color="teal" class="mr-1">mdi-download</v-icon>
                    <span class="text-caption text-truncate">{{ `${item.type == 'torrent'?item.client_name:'-' }` }}</span>
                  </div>
                  <div class="info-item">
                    <v-icon size="14" color="error" class="mr-1">mdi-close-octagon</v-icon>
                    <span class="text-caption text-truncate">{{ `${item.type == 'torrent' && item.error?item.error:'无'}` }}</span>
                  </div>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>

        <!-- 空状态显示 -->
        <div v-else class="empty-state">
          <v-icon icon="mdi-delete-off" />
          <div class="text-h6 mb-2">暂无待清理项目</div>
          <div class="text-body-2">请先在扫描结果中选择需要清理的项目</div>
        </div>
      </div>
    </v-card-text>
    
    <v-snackbar v-model="state.snackbar.show"
                :timeout="3000"
                :color="state.snackbar.color"
                :location="state.snackbar.location"
    >
      {{ state.snackbar.message }}
    </v-snackbar>
  </v-card>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue';
import {CombinedItem, ONLY_TORRENT, formatBytes, SnackbarModel, ALL, copyPath, mapTrackers,
getStatusColor,getColorByString,getRandomColor

} from './definedFunctions.ts';

interface StateModel{
  cleanupList: CombinedItem[]
  clearing:boolean
  snackbar:SnackbarModel
}

const state = reactive<StateModel>({
  cleanupList:[],
  clearing:false,
  snackbar: {
    location:'top',
    show: false,
    message: '',
    color: 'success'
 }
})

// 移除项目从待清理列表
const removeFromCleanup = (item: CombinedItem) => {
   state.cleanupList = state.cleanupList.filter(
      i => i.hash !== item.hash
    );
  showNotification(`已从待清理列表中移除: ${item.name}`);
};

// 切换展开状态
const toggleExpand = (item: CombinedItem) => {
  if (!(item as any).expanded) {
    (item as any).expanded = true;
  } else {
    (item as any).expanded = false;
  }
};

// 格式化时间差
const formatTimeSince = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffInMs = now.getTime() - date.getTime();
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  
  if (diffInDays === 0) return '今天';
  if (diffInDays === 1) return '昨天';
  if (diffInDays < 7) return `${diffInDays}天前`;
  if (diffInDays < 30) return `${Math.floor(diffInDays / 7)}周前`;
  if (diffInDays < 365) return `${Math.floor(diffInDays / 30)}个月前`;
  return `${Math.floor(diffInDays / 365)}年前`;
};

// 格式化种子生存时间
const formatCreatedTime = (time: string): string => {
  if (time === "1970-01-01 08:00:00" || !time) {
    return "";
  } else {
    return formatTimeSince(time);
  }
};

// 删除选项文本
const deleteOptionText = (item: CombinedItem | undefined) => {
  // 根据 removeOption 返回对应的文本
  if (item?.type == 'torrent' && (item.removeOption === ONLY_TORRENT || (item?.removeOption === ALL && item.data_missing))) {
    return {
      text:"仅种子",
      color:"error"
    }
  } else {
    return {
      text:"全部",
      color:"success"
    }
  }
}

// 计算总大小
const totalSize = computed(() => {
  // 计算总大小逻辑（假设每个项目有 size 字段）
  let totalSize = 0
  for (const item of state.cleanupList) {
    if (item.type == 'torrent'){
          if (item.removeOption === ONLY_TORRENT || item.data_missing) {
            continue; // 如果只删除种子，跳过
          }else{
            totalSize += item.size || 0; // 累加种子大小
          }
    }else if (item.type == 'file') {
      totalSize += item.size || 0; // 累加源文件大小
    }
  }
  return formatBytes(totalSize);
});

// 计算每行的大小 文本
const itemSizeText = (item: CombinedItem | undefined) => {
  if (item?.type == 'torrent' && item?.data_missing){
    return "不计算"
  }else if (item && item.size){
    return formatBytes(item.size)
  }
  return "未知大小"
}

const deleteAllRecord = () => {
  state.cleanupList = [];
  showNotification('已清空所有待清理记录');
};

// 去重添加到待清理
const setCleanupList = (info: CombinedItem[]) => {
  const existingHashes = new Set(
    state.cleanupList.map(item => item.hash)
  );
  const newList = info.filter(item => !existingHashes.has(item.hash));

  state.cleanupList.push(...newList);
  if (newList.length > 0) {
    showNotification(`成功添加 ${newList.length} 条记录到待清理`)
  } else {
    showNotification("没有新项目可添加，全部已存在","info")
  }
};

const showNotification = (text, color = 'success')=> {
  state.snackbar.message = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}

const _copyPath = async (path: string) => {
  if (await copyPath(path)){
    showNotification("路径已复制到剪贴板");
  }else{
    showNotification("复制路径失败","error");
  }
};

const getCleanupList = ()=>{
  return state.cleanupList
}

defineExpose({
  setCleanupList,
  getCleanupList,
  deleteAllRecord,
})
</script>

<style scoped>
/* 清理列表卡片样式 */
.cleanup-list-card {
  border: none;
  border-radius: 0;
  box-shadow: none;
  margin: 0;
}

/* 清理列表标题栏样式 */
.cleanup-list-title {
  background: rgba(var(--v-theme-surface), 0.95);
  color: rgba(var(--v-theme-on-surface), 0.87);
  border-bottom: 1px solid rgba(var(--v-border-color), 0.1);
  padding: 8px 16px;
  margin: 0;
}

.title-left {
  display: flex;
  align-items: center;
  flex: 1; /* 让左侧区域占据剩余空间 */
  min-width: 0; /* 允许内容收缩 */
}

.title-content {
  display: flex;
  flex-direction: column;
  width: 100%; /* 确保内容占满可用宽度 */
}

.title-stats {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  max-width: calc(100vw - 150px); /* 增加标签可用空间 */
  min-width: 0; /* 允许内容收缩 */
}

.title-stats .v-chip {
  font-size: 0.75rem;
  height: 24px; /* 固定高度 */
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0; /* 防止标签被压缩 */
  white-space: nowrap; /* 不换行 */
  min-width: fit-content; /* 根据内容调整最小宽度 */
  padding: 4px 8px; /* 调整内边距 */
}

.title-stats .v-chip:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(var(--v-theme-error), 0.15);
}

.title-stats .v-chip .v-icon {
  opacity: 0.9;
}

.title-actions {
  display: flex;
  align-items: center;
  flex-shrink: 0; /* 防止操作按钮被压缩 */
  margin-left: auto; /* 确保操作按钮始终在右侧 */
}

/* 清理卡片样式 */
.cleanup-card-horizontal {
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-border-color), 0.1);
  cursor: pointer;
  min-height: 120px;
  max-width: 400px;
  background-color: rgba(var(--v-theme-surface), 0.95);
  border-radius: 0;
}

/* QB卡片样式 - 淡蓝色背景 */
.cleanup-card-horizontal.qb-card {
  background-color: rgba(59, 130, 246, 0.03);
  border-color: rgba(59, 130, 246, 0.1);
}

.cleanup-card-horizontal.qb-card:hover {
  background-color: rgba(59, 130, 246, 0.05);
  border-color: rgba(59, 130, 246, 0.2);
}

/* TR卡片样式 - 淡红色背景 */
.cleanup-card-horizontal.tr-card {
  background-color: rgba(239, 68, 68, 0.03);
  border-color: rgba(239, 68, 68, 0.1);
}

.cleanup-card-horizontal.tr-card:hover {
  background-color: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.2);
}

.cleanup-card-horizontal:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(var(--v-border-color), 0.1);
  border-color: rgba(var(--v-theme-error), 0.2);
}

/* 卡片头部样式 */
.card-header-horizontal {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.1);
  background-color: rgba(var(--v-theme-surface), 0.3);
  border-radius: 0;
  padding: 8px 12px;
}

.file-name-horizontal {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.87);
  line-height: 1.4;
  max-width: 280px;
  font-size: 0.8rem;
  word-wrap: break-word;
  white-space: normal;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 卡片内容样式 */
.card-content-horizontal {
  background-color: rgba(var(--v-theme-surface), 0.2);
  padding: 8px 12px;
}

/* 信息网格布局 */
.info-grid-horizontal {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 6px;
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 0.7rem;
  line-height: 1.1;
  padding: 0;
}

.info-item .v-icon {
  flex-shrink: 0;
  opacity: 0.8;
}

.info-item .text-caption {
  margin-left: 3px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

/* 详细信息表格样式 */
.detail-table {
  background-color: rgba(var(--v-theme-surface-variant), 0.3);
  border-radius: 4px;
  padding: 8px;
}

.detail-row {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  font-size: 0.75rem;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.7);
  min-width: 60px;
  margin-right: 8px;
}

.detail-value {
  color: rgba(var(--v-theme-on-surface), 0.87);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-value.text-error {
  color: rgb(var(--v-theme-error));
}

/* 卡片底部操作样式 */
.card-actions-horizontal {
  background-color: rgba(var(--v-theme-surface), 0.3);
  border-top: 1px solid rgba(var(--v-border-color), 0.1);
  border-radius: 0;
  padding: 6px 12px;
}

/* 删除选项和类型标签样式 */
.delete-option-chip,
.type-chip {
  border-radius: 0 0 8px 8px !important;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.empty-state .v-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* 响应式网格调整 */
@media (max-width: 600px) {
  .cleanup-card-horizontal {
    min-height: 100px;
    max-width: 100%;
  }
  
  .info-grid-horizontal {
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
  }
  
  .card-header,
  .card-content,
  .card-actions,
  .card-header-horizontal,
  .card-content-horizontal,
  .card-actions-horizontal {
    padding: 8px;
  }
  
  .file-name-horizontal {
    max-width: 200px;
  }
  
  .title-stats {
    max-width: calc(100vw - 100px); /* 移动端增加标签可用空间 */
  }
  
  .title-stats .v-chip {
    font-size: 0.7rem;
    height: 20px;
    padding: 3px 6px;
  }
}

@media (min-width: 1920px) {
  .cleanup-card-horizontal {
    min-height: 140px;
    max-width: 450px;
  }
  
  .info-grid-horizontal {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }
  
  .file-name-horizontal {
    max-width: 320px;
  }
}

/* 图标颜色主题 */
.info-item .v-icon[color="success"] {
  color: rgb(var(--v-theme-success)) !important;
}

.info-item .v-icon[color="info"] {
  color: rgb(var(--v-theme-info)) !important;
}

.info-item .v-icon[color="warning"] {
  color: rgb(var(--v-theme-warning)) !important;
}

.info-item .v-icon[color="primary"] {
  color: rgb(var(--v-theme-primary)) !important;
}

.info-item .v-icon[color="secondary"] {
  color: rgb(var(--v-theme-secondary)) !important;
}

.info-item .v-icon[color="accent"] {
  color: rgb(var(--v-theme-accent)) !important;
}
</style>