<template>
  <v-card flat class="mb-4">
    <v-card-title class="text-subtitle-1 d-flex align-center px-2 py-1 bg-primary-lighten-5 flex-wrap">
      <div class="d-flex title-stats align-center ml-1" :class="[smAndDown ? 'w-100 mb-2' : 'mr-1']">
         <!-- 全选复选框 -->
        <v-checkbox
          :model-value="isSelectAll"
          :indeterminate="isIndeterminate"
          hide-details
          @change="toggleSelectAll"
          :size="smAndDown?'x-small':'small'"
          :label="smAndDown ? '' : '全选'"
          :density="smAndDown?'compact':'comfortable'"
          class="select-all-checkbox"
        />
        <v-chip :size="smAndDown?'x-small':'small'" color="info" variant="flat" v-if="totalComputed!=''">
          <v-icon size="14" class="mr-1">mdi-database</v-icon>
          {{ totalComputed }} 
        </v-chip>
        <v-chip  :size="smAndDown?'x-small':'small'" color="error" variant="flat" v-if="state.selectedScans.length > 0">
          <v-icon size="14" class="mr-1">mdi-checkbox-multiple-marked</v-icon>
          {{ `已选择 ${state.selectedScans.length}项: ${selectedScansSize}` }}
        </v-chip>
      </div>
      <v-spacer v-if="!smAndDown" />
      <div class="d-flex align-center ml-1 flex-wrap" v-if="totalPages >= 1">
      <v-select
          v-model="scanParams.pageSize"
          :items="[50, 100, 200, 300, 500]"
          variant="underlined"
          density="compact"
          :size="smAndDown?'x-small':'small'"
          :style="smAndDown?'max-width: 63px;':'max-width: 120px;'"
          @update:modelValue="handlePageSizeChange"
      ></v-select>
      <v-pagination
          v-model="scanParams.page"
          :length="totalPages"
          @update:modelValue="handlePageChange"
          rounded="circle"
          variant="elevated"
          :size="'small'"
          prev-icon="mdi-arrow-left-circle"
          next-icon="mdi-arrow-right-circle"
          :density="smAndDown?'compact':'comfortable'"
          :total-visible="smAndDown?1:7"
          :class="[smAndDown?'ml-1':'ml-2']"
          :elevation="5"
      ></v-pagination>
      <div class="d-flex align-center ml-1">
       <v-text-field
          :class="smAndDown?'ml-1':'ml-3'"
          variant="underlined"
          density="compact"
          hide-details
          :size="smAndDown?'x-small':'small'"
          :label="`共 ${ totalPages } 页`"
          :max-width="smAndDown?100:130"
          v-model="state.currentPage"
          >
          <template #prepend-inner>
          <!-- <v-chip color="grey-darken-3" :size="18" variant="elevated" class="go-page-prepend" @click="goToPage">去</v-chip> -->
          <!-- <v-icon size="18" class="mr-1">mdi-close-circle</v-icon> -->
           <v-icon size="20" class="mr-1 cursor-pointer go-page-append" 
            @click="goToPage"
           color="primary"
           title="跳转到"
           >mdi-arrow-right-bold-circle</v-icon>
        </template>
        <template #append-inner>
          <v-icon size="20" class="mr-1 cursor-pointer go-page-append" 
          @click.stop="state.currentPage=undefined"
           color="#009688"
           title="清除"
           >mdi-close-circle</v-icon>
          <!-- <v-chip color="grey-darken-3 cursor-pointer" :size="'x-small'" variant="elevated" class="go-page-append" @click="goToPage">页</v-chip> -->
        </template>
        </v-text-field>
        </div>
    </div>
    </v-card-title>
    <v-card-text class="pa-0">
        <!-- 筛选标签区域 - 紧凑彩色设计 -->
       <div class="filter-section-compact pa-3 pb-2" v-if="activeFilterCount > 0">
         <!-- 筛选标签紧凑布局 -->
         <div class="filter-chips-compact">
           <template v-for="(value,key) in state.filter">
             <v-chip
               v-if="isShowFilterTag(value,key)"
               :key="key"
               class="filter-chip-compact"
               :class="`filter-${key}`"
               closable
               variant="elevated"
               size="small"
               @click:close="deleteFilter(key)"
               elevation="2"
             >
               <template v-slot:prepend>
                <v-tooltip location="top">
                   <template #activator="{ props }">
                     <v-icon v-bind="props" v-if="getfilterAttrByKey('type',key)=='icon'" size="14">{{ getfilterAttrByKey('label',key) }}</v-icon>
                     <span v-else-if="getfilterAttrByKey('type',key)=='text'" size="14">{{ getfilterAttrByKey('label',key) }}</span>
                   </template>
                   {{ getfilterAttrByKey("title",key) }}
                 </v-tooltip>
               </template>
               {{ formatFilterTag(value,key) }}
             </v-chip>
           </template>
         </div>
      </div>
      <div style="min-height: 260px; max-height: 450px; overflow-y: auto;">
        <!-- <data-list-table 
          v-if="!props.loading && props.scanRes.combinedList.length > 0"
          v-model:selectedScans="state.selectedScans"
          :headers="state.headers"
          :scanRes="props.scanRes"
          :scanParams="props.scanParams"
          @update:scanParams="handleScanParamsChange"
          :loading="props.loading"
          @copyPath="_copyPath"
        /> -->
        <data-list-card
        v-if="!props.loading && props.scanRes.combinedList.length > 0"
         v-model:selectedScans="state.selectedScans"
        :scanRes="props.scanRes"
        :loading="props.loading"
          @copyPath="_copyPath"
          ref="dataListCardRef"
        />
        <!-- 空状态显示 -->
        <div v-else-if="!props.loading && props.scanRes.combinedList.length === 0" class="empty-state">
          <v-icon icon="mdi-database-off" />
          <div class="text-h6 mb-2">暂无数据</div>
          <div class="text-body-2">当前筛选条件下没有找到匹配的种子或文件</div>
        </div>

        <!-- 加载状态 -->
        <div v-else class="pa-4">
          <v-skeleton-loader type="card@8" />
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
    <filter-dialog
    v-model:dialogShow="state.filterDialog" 
    :filter="state.filter" 
    :initialConfig="props.initialConfig"
    @filterChange="filterChange"
    @applyFilter="applyFilter"
    />
    <sort-dialog
    v-model:dialogShow="state.sortDialog" 
    @applySort="applySort"
    />
  </v-card>
</template>

<script setup lang="ts">
import {ref, computed, reactive, watch} from 'vue';
import type {PropType} from 'vue';
import {formatBytes, SnackbarModel,CombinedItem, ScanResult,copyPath,mapTrackers,SortItem,formatTimeSince, FilterModel} from "./definedFunctions";
import FilterDialog from './FilterDialog.vue';
import SortDialog from './SortDialog.vue';
import DataListTable from './DataListTable.vue';
import DataListCard from './DataListCard.vue';
// 响应式断点：小屏幕（含）仅显示图标
import { useDisplay } from 'vuetify';
const { smAndDown } = useDisplay();


interface StateModel {
  selectedScans: Array<CombinedItem>; // 包含 data_missing 可选属性
  snackbar: SnackbarModel;
  headers: any[];
  currentPage: string|undefined;
  filterDialog: boolean;
  filter:FilterModel
  currentFilterValues: Array<string>;
  sortDialog: boolean;
  
}

const props = defineProps({
  initialConfig: {
    type: Object,
    default: () => ({}),
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
  // 将sortBy改为字符串类型，避免直接传递SortItem数组
  scanParams: {
    type: Object as PropType<{
      page: number;
      pageSize: number;
      sortBy: SortItem[];
    }>,
    required: true,
    default: () => ({
      page: 1,
      pageSize: 50,
      sortBy: [{key: 'name', order: 'asc'}]
    })
  },
  loading: {
    type: Boolean,
    default: false
  },
});

const emit = defineEmits(['deleteAllRecord', 'addToCleanup', 'update:scanParams','applyFilter','applySort']);

const filterItems = [{
  title:"路径",
  value:"path",
  type:"icon",
  label:"mdi-folder-arrow-left"
  },  { title:"下载器名称",
    value:"client_name",
    type:"icon",
    label:"mdi-download"
  },{ title:"下载器类型",
    value:"client",
    type:"icon",
    label:"mdi-download-circle"
  },{ title:"做种数",
    value:"seeds_limit",
    type:"icon",
    label:"mdi-seed"
  },{ title:"大小(MB)",
    value:"size_limit",
    type:"icon",
    label:"mdi-harddisk"
  },{ title:"存活(小于)",
    value:"live_time",
    type:"icon",
    label:"mdi-clock-outline"
  },
]

const state = reactive<StateModel>({
  selectedScans: [],
  snackbar: {
    location:'top',
    show: false,
    message: '',
    color: 'success'
 }, 
 headers: [
      { value: 'expand', title: '',key:"data-table-expand"},
      { value: 'name', title: '名称',align:"left", sortable: true,maxWidth:"20rem", },
      { value: 'path', title: '路径',align:"left", sortable: true,maxWidth:"14rem", },
      { value: 'tracker', title: 'Tracker',align:"center", },
      { value: 'status', title: '状态' ,align:"center",},
      { value: 'seeds', title: '做种数' ,align:"center",sortable: true},
      { value: 'size', title: '大小', sortable: true,align:"center", },
      { value: 'select', title: '',key:"data-table-select"}],
  currentPage: undefined,
  filterDialog: false,
  filter:{
    path: '',
    client_name: '',
    client: '',
    seeds_limit_down:null,
    seeds_limit_up:null,
    seeds_limit: [null,null],
    size_limit_down:null,
    size_limit_up:null,
    size_limit: [null,null],
    live_time:0,
  },
  currentFilterValues:["path"],
  sortDialog: false,
})

const dataListCardRef = ref();
// 获取过滤项的属性通过key(value)
const getfilterAttrByKey = (attr:string,key: string) => { 
  for (let i of filterItems) {
    if (i.value === key) {
      return i[attr];
    }
  }
  return key;
}


// 计算总数和缺失文件数量
const totalComputed = computed(() => {
  let res :string[]= []
  if (props.scanRes.tTotal>0){
    let torrentFIleText = `种子：${props.scanRes.tTotal}/${formatBytes(props.scanRes.tTotalSize)}`;
    res.push(torrentFIleText);
  }
  if (props.scanRes.mTotal>0){
    let missingFileText = `缺种的文件：${props.scanRes.mTotal}/${formatBytes(props.scanRes.mTotalSize)}`;
    res.push(missingFileText);
  }
  if (props.scanRes.tTotal>0 && props.scanRes.mTotal>0){
    let totalText=`总计：${props.scanRes.total}/${formatBytes(props.scanRes.totalSize)}`;
    res.push(totalText);
  }
  return  res.join(' | ');
});

// 是否被选中
const isItemSelected = (item: CombinedItem): boolean => {
  return state.selectedScans.some(scan => {
      return scan.hash === item.hash;
  });
};

// 计算全选状态
const isSelectAll = computed(() => {
  const visibleCount = props.scanRes.combinedList.length;
  if (!dataListCardRef.value) return false;
  // 只有当可见项目数量大于0且所有可见项目都被选中时，才是全选状态
  const isAllSelected = visibleCount > 0 && props.scanRes.combinedList.every(item => isItemSelected(item));
  return isAllSelected;
});

// 计算部分选择状态
const isIndeterminate = computed(() => {
  const selectedCount = state.selectedScans.length;
  // 当有项目被选中但不是所有项目都被选中时，是部分选择状态
  const isIndeterminate = selectedCount > 0 && !props.scanRes.combinedList.every(item => isItemSelected(item));
  return isIndeterminate;
});

// 计算活跃筛选条件数量
const activeFilterCount = computed(() => {
  let count = 0;
  Object.entries(state.filter).forEach(([key, value]) => {
    if (isShowFilterTag(value,key)) {
      count++;
    }
  });
  return count;
});

// 消息通知
const showNotification = (text, color = 'success')=> {
  state.snackbar.message = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}

// 计算总页数
const totalPages = computed(() => {
     return Math.ceil(props.scanRes.total / props.scanParams.pageSize);
});

// 页码改变
const handlePageChange = (newPage: number) => {
  emit('update:scanParams', {
    pageSize: props.scanParams.pageSize,
    page: newPage,
    sort: props.scanParams.sortBy,
    changed:"page"
  });
};
// 分页数改变
 const handlePageSizeChange = (newPageSize: number) => {
     emit('update:scanParams', {
       pageSize: newPageSize,
       page: 1, // 切换每页数量后跳转到第一页
       sort: props.scanParams.sortBy,
       changed:"pageSize"
     });
};
// 扫描参数改变
const handleScanParamsChange = (newScanParams:any)=>{
  emit('update:scanParams', newScanParams);
}
// 去跳转页码
const goToPage = () =>{
  
  if (state.currentPage === undefined || state.currentPage === null) {
    return;
  }
  let currentPageNum = parseInt(state.currentPage);
  if (!currentPageNum) {
    showNotification("请输入有效的页码", "error");
    return;
  }
  if (currentPageNum < 1 || currentPageNum > totalPages.value) {
    showNotification("页码超出范围", "error");
    return;
  }
  handlePageChange(currentPageNum);
}
// 切换全选状态
const toggleSelectAll = () => {
  // 检查当前是否已经全选（基于实际选中状态，而不是数量比较）
  const currentlyAllSelected = props.scanRes.combinedList.every(item => isItemSelected(item));
  if (currentlyAllSelected) {
    // 如果当前是全选状态，则取消全选
    state.selectedScans = [];
  } else {
    // 如果当前不是全选状态，则全选
    // 清空当前选中状态，然后添加所有可见项目
    state.selectedScans = [];
    props.scanRes.combinedList.forEach(item => {
      state.selectedScans.push(item);
    });
  }
  // 不需要手动更新selectAll状态，计算属性会自动处理
};

const clearSelectedScans = ()=>{
  state.selectedScans = [];
}

// 路径复制结果
const _copyPath = (isSuccess: boolean) => {
  if (isSuccess){
    showNotification("完整路径已复制到剪贴板");
  }else{
    showNotification("复制路径失败","error");
  }
};


// 计算所选项目大小的总和，排除 data_missing 为 true 的项
const selectedScansSize = computed(() => {
  return formatBytes(state.selectedScans.reduce((sum, scan) => {
    // 添加类型守卫检查
    if ('data_missing' in scan && scan.data_missing) {
      sum = sum + 0;
    }else{
      sum = sum + scan.size;
    }
    return sum
  }, 0))
});

// 切换筛选对话框的显示状态
const toggleFilter = () => {
  state.filterDialog = !state.filterDialog;
};

//应用筛选
const applyFilter = () => {
  // console.log(state.filter);
 state.filterDialog = false;
  emit('applyFilter', state.filter)
};

//应用排序
const applySort = (sortOptionList: SortItem[])=>{
  console.log("applySort",sortOptionList);
  emit('applySort', sortOptionList)
}
// 删除筛选条件
const deleteFilter = (name:string)=>{
  if (state.filter[name] instanceof Array){
    state.filter[name] = [null,null]
  }else {
    state.filter[name] = ''
  }
  state.filterDialog = false;
  emit('applyFilter', state.filter)
};

// filterChange 
const filterChange = (filter:Object)=>{
  if (filter instanceof Object){
    for (let key in filter){
      if (key in state.filter){
         state.filter[key] = filter[key];
          if (key.indexOf("_up") > -1){
            let _key = key.replace("_up","")
            state.filter[_key][1] = filter[key]
          }
          if (key.indexOf("_down") > -1){
            let _key = key.replace("_down","")
            state.filter[_key][0] = filter[key]
          }
        }
      }
  }
}
// 切换对话框的显示状态
const toggleSort = () => {
  state.sortDialog = !state.sortDialog;
};

// 是否显示筛选标签
const isShowFilterTag=(value:any,key:string)=>{
  if (!filterItems.some(item=>item.value === key)) return false;
  if (value instanceof Array && value.length === 2){
    return value[0] !==null && value[1] !== null && value[0] !== '' && value[1] !== '';
  }else if (typeof value === 'number'){
    return value !== 0
  }else if (value !== null && value !== ''){
    return true
  }
  return false;
}
// 格式化筛选标签
const formatFilterTag=(value:any,key:string="")=>{ 
  let unit=""
  if (value instanceof Array && value.length === 2){
    if (key=='size_limit'){unit = 'MB'};
    return `${value[0]} ~ ${value[1]} ${unit}`
  }else{
    return value
  }
}

defineExpose({
  clearSelectedScans,
  toggleFilter,
  toggleSort,
  getSelectedScans: () => state.selectedScans,

})
</script>
<style scoped> 
.size-column {
  width: 7.5rem !important;
  max-width: 7.5rem !important;
}
.name-column {
  width: 40rem !important;
  max-width: 40rem !important;
  & .name-text{
    margin-left: 8px;
    max-width: 35rem;
  }
}
.w-100 {
  width: 100% !important;
}

.title-stats {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  min-width: 0; /* 允许内容收缩 */
}

.title-stats .v-chip {
  font-size: 0.65rem;
  height: 24px; /* 固定高度 */
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0; /* 防止标签被压缩 */
  white-space: nowrap; /* 不换行 */
  min-width: fit-content; /* 根据内容调整最小宽度 */
  padding: 2px 4px; /* 调整内边距 */
}

.title-stats .v-chip:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.15);
}

.title-stats .v-chip .v-icon {
  opacity: 0.9;
}
/* 加载状态样式 */
.v-skeleton-loader {
  margin-bottom: 16px;
}

/* 分页控件样式 */
.border-top {
  border-top: 1px solid rgba(var(--v-border-color), 0.1);
}
.v-pagination {
  background-color: rgba(var(--v-theme-surface), 0.5);
  border-radius: 4px;
  padding: 2px;
  min-height: auto;
}
.v-pagination .v-btn {
  margin: 0 1px;
  height: 28px;
  min-width: 28px;
}
/* 筛选标签区域 - 紧凑彩色设计 */
.filter-section-compact {
  background-color: rgba(var(--v-theme-surface), 0.95);
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(var(--v-border-color), 0.05);
  margin-bottom: 12px;
}

.filter-chips-compact {
  padding: 8px 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip-compact {
   display: flex;
   align-items: center;
   font-size: 0.75rem;
   font-weight: 500;
   color: rgba(var(--v-theme-on-surface), 0.87);
   background-color: rgba(var(--v-theme-surface), 0.1);
   border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
   border-radius: 8px;
   padding: 6px 12px;
   min-height: 32px;
   transition: all 0.2s ease;
}

 .filter-chip-compact:hover {
   transform: translateY(-1px);
   box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.15);
   border-color: rgba(var(--v-theme-primary), 0.3);
 }

 .filter-chip-compact.filter-path {
   background-color: rgba(99, 102, 241, 0.1);
   border-color: rgba(99, 102, 241, 0.3);
   color: rgba(99, 102, 241, 0.9);
 }
 
 .filter-chip-compact.filter-client_name {
   background-color: rgba(168, 85, 247, 0.1);
   border-color: rgba(168, 85, 247, 0.3);
   color: rgba(168, 85, 247, 0.9);
 }
 
 .filter-chip-compact.filter-client {
   background-color: rgba(236, 72, 153, 0.1);
   border-color: rgba(236, 72, 153, 0.3);
   color: rgba(236, 72, 153, 0.9);
 }
 
 .filter-chip-compact.filter-seeds_limit {
   background-color: rgba(34, 197, 94, 0.1);
   border-color: rgba(34, 197, 94, 0.3);
   color: rgba(34, 197, 94, 0.9);
 }
 
 .filter-chip-compact.filter-size_limit {
   background-color: rgba(59, 130, 246, 0.1);
   border-color: rgba(59, 130, 246, 0.3);
   color: rgba(59, 130, 246, 0.9);
 }
 
 .filter-chip-compact.filter-live_time {
   background-color: rgba(245, 158, 11, 0.1);
   border-color: rgba(245, 158, 11, 0.3);
   color: rgba(245, 158, 11, 0.9);
 }

.filter-chip-compact .v-icon {
  margin-right: 4px;
  opacity: 0.8;
}

 .filter-chip-compact.filter-path .v-icon {
   color: rgba(99, 102, 241, 0.9) !important;
 }
 
 .filter-chip-compact.filter-client_name .v-icon {
   color: rgba(168, 85, 247, 0.9) !important;
 }
 
 .filter-chip-compact.filter-client .v-icon {
   color: rgba(236, 72, 153, 0.9) !important;
 }
 
 .filter-chip-compact.filter-seeds_limit .v-icon {
   color: rgba(34, 197, 94, 0.9) !important;
 }
 
 .filter-chip-compact.filter-size_limit .v-icon {
   color: rgba(59, 130, 246, 0.9) !important;
 }
 
 .filter-chip-compact.filter-live_time .v-icon {
   color: rgba(245, 158, 11, 0.9) !important;
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

.go-page-append,.go-page-prepend{
  /* font-size: 10px; */
  opacity:1;
  &:hover{
    cursor: pointer;
    opacity: 0.6;
    transform: translateY(-2px) !important;
    /* box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important; */
    &::before {
      left: 100%;
    }
  }
}
</style>