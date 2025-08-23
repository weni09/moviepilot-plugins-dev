<template>
      <div>
    <!-- 卡片网格布局 -->
        <v-row v-if="!props.loading && props.scanRes.combinedList.length > 0" :class="pa-2" no-gutters>
          <v-col 
            v-for="(item,index) in props.scanRes.combinedList" 
            :key="item.hash"
            cols="12" 
            sm="6" 
            md="4" 
            lg="4"
            class="pa-1 d-flex"
          >
            <v-card 
              :class="[
                'seed-card-horizontal', 
                { 'selected': isItemSelected(item) },
                { 'qb-card': item.hasOwnProperty('client') && item.client !== 'transmission' },
                { 'tr-card': item.hasOwnProperty('client') && item.client === 'transmission' }
              ]"
              :elevation="props.selectedScans.includes(item) ? 4 : 1"
              hover
              @click="toggleSelection(item)"
              class="flex-grow-1"
            >
              <!-- 卡片头部 - 横向布局 -->
              <div class="card-header-horizontal pa-2">
                 <div class="d-flex align-center justify-space-between mb-2">
                   <v-row class="d-flex align-center" gutters="no-gutters">
                    <v-col :cols="1" class="px-0 py-0">
                     <v-checkbox 
                       :model-value="props.selectedScans"
                       @update:model-value="selectedScansChange($event)"
                       :value="item" 
                       hide-details
                       @click.stop
                       size="x-small"
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
              <div class="card-content-horizontal pa-1 pt-0">
                <!-- 状态标签行 -->
                <div class="d-flex align-center flex-wrap mb-1 font-weight-bold status-labels">
                <v-chip
                    :color="item.hasOwnProperty('client') && item.client === 'transmission' ? '#E91E63' : 'info'"
                    size="x-small"
                    text-color="white"
                    v-if="item.hasOwnProperty('client') && item.client"
                    >
                    {{ item.client === 'transmission' ? 'TR' : 'QB' }}
                </v-chip>
                  <v-chip
                    :color="getRandomColor(index)"
                    size="x-small"
                    text-color="white"
                    class="ml-1"
                  >
                    {{ item.hash.toUpperCase() }}
                  </v-chip>
                </div>

                <!-- 详细信息 - 横向网格布局 -->
                <div class="info-grid-horizontal">
                  <div class="info-item">
                    <v-icon size="14" color="info" class="mr-1">mdi-database</v-icon>
                    <span class="text-caption">{{ item.size ? formatBytes(item.size) : '未知' }}</span>
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
      </div>
    </template>
    <script lang="ts" setup> 
import type {PropType} from 'vue';
import {formatBytes,CombinedItem, ScanResult,copyPath,
    mapTrackers,SortItem,formatTimeSince,getStatusColor,getColorByString,getRandomColor
} from "./definedFunctions";

const props = defineProps({
   selectedScans: {
    type: Array as PropType<CombinedItem[]>,
    default: () => []
  },
  scanRes: {
    type: Object as PropType<ScanResult>,
    default: () => ({
      combinedList: [],
      total: 0,
      totalSize:0,
      tTotal:0,
      tTotalSize:0,
      mTotal:0,
      mTotalSize:0,
      page: 1,
      pageSize: 50
    })
  },
  loading: {
    type: Boolean,
    default: false
  },
});

const emit = defineEmits(["copyPath","update:selectedScans","update:scanParams"])

// 检查项目是否被选中（基于hash比较，而不是对象引用）
const isItemSelected = (item: CombinedItem): boolean => {
  return props.selectedScans.some(scan => {
      return scan.hash === item.hash;
  });
};

// 选中状态改变
const toggleSelection = (item: CombinedItem) => {
  // 根据项目类型使用不同的比较逻辑
  const index = props.selectedScans.findIndex(scan => {
    return scan.hash === item.hash;
  });
  if (index > -1) {
    // 取消选择
    props.selectedScans.splice(index, 1);
  } else {
    // 选择项目
    props.selectedScans.push(item);
  }
};
//格式化种子生存时间
const formatCreatedTime = (time: string)=>{
  if (time == "1970-01-01 08:00:00"){
return "未知"
  }
  else{
    return formatTimeSince(time)
  }
}

// 复制路径
const _copyPath = async (path: string) => {
  if (await copyPath(path)){
    emit('copyPath', true);
  }else{
    emit('copyPath', false);
  }
};

// 切换展开状态
const toggleExpand = (item: CombinedItem) => {
  if (!(item as any).expanded) {
    (item as any).expanded = true;
  } else {
    (item as any).expanded = false;
  }
};
// 已选择项变更
const selectedScansChange = (values:Array<CombinedItem>|null|undefined)=>{
    emit('update:selectedScans', values);
}

defineExpose({
  isItemSelected,
});
</script>

<style lang="scss" scoped>

/* 横向卡片样式 */
.seed-card-horizontal {
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-border-color), 0.1);
  cursor: pointer;
  min-height: 120px;
  max-width: 400px;
  background-color: rgba(var(--v-theme-surface), 0.95);
  border-radius: 0;
}

/* QB卡片样式 - 淡蓝色背景 */
.seed-card-horizontal.qb-card {
  background-color: rgba(59, 130, 246, 0.03);
  border-color: rgba(59, 130, 246, 0.1);
}

.seed-card-horizontal.qb-card:hover {
  background-color: rgba(59, 130, 246, 0.05);
  border-color: rgba(59, 130, 246, 0.2);
}

/* TR卡片样式 - 淡红色背景 */
.seed-card-horizontal.tr-card {
  background-color: rgba(239, 68, 68, 0.03);
  border-color: rgba(239, 68, 68, 0.1);
}

.seed-card-horizontal.tr-card:hover {
  background-color: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.2);
}

.seed-card-horizontal:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(var(--v-border-color), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.seed-card-horizontal.selected {
  border-color: rgba(var(--v-theme-primary), 0.5);
  background-color: rgba(var(--v-theme-primary), 0.02);
  box-shadow: 0 2px 12px rgba(var(--v-theme-primary), 0.15);
}

 .card-header-horizontal {
   border-bottom: 1px solid rgba(var(--v-border-color), 0.1);
   background-color: rgba(var(--v-theme-surface), 0.3);
   border-radius: 0;
   padding: 8px 12px;
 }

 .card-content-horizontal {
  background-color: rgba(var(--v-theme-surface), 0.2);
  padding: 8px 12px;
  .status-labels{
    :deep(.v-chip.v-chip--size-x-small){
          padding: 0px 2px !important;
    }
  }
}

.file-name-horizontal {
    font-weight: 500;
    color: rgba(var(--v-theme-on-surface), 0.87);
    line-height: 1.2;
    max-width: 20rem;
    font-size: 0.8rem;
    word-wrap: break-word;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* 限制最多显示2行 */
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
}

/* 响应式网格调整 */
@media (max-width: 600px) {
  .seed-card-horizontal {
    min-height: 100px;
    max-width: 100%;
  }
  .info-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .info-grid-horizontal {
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
  }
  
  .card-header-horizontal,
  .card-content-horizontal,
  .card-actions-horizontal {
    padding: 8px;
  }
  
  .file-name-horizontal {
    // max-width: 200px;
  }
}

@media (min-width: 1920px) {
  .seed-card-horizontal {
    min-height: 140px;
    max-width: 450px;
  }
  .info-grid-horizontal {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }
  .file-name-horizontal {
    // max-width: 320px;
  }
}




/* 信息网格布局 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

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
  margin-left: 1px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: rgba(var(--v-theme-on-surface), 0.7);
  max-width: 7.5rem;
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
.card-actions {
  background-color: rgba(var(--v-theme-surface), 0.3);
  border-top: 1px solid rgba(var(--v-border-color), 0.1);
  border-radius: 0 0 4px 4px;
}

 .card-actions-horizontal {
   background-color: rgba(var(--v-theme-surface), 0.3);
   border-top: 1px solid rgba(var(--v-border-color), 0.1);
   border-radius: 0;
   padding: 6px 12px;
 }


</style>