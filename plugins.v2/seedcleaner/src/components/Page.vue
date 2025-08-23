<template>
    <div class="plugin-common plugin-page">
    <v-card flat class="rounded border">
      <v-card-title class="text-subtitle text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
        <v-icon icon="mdi-tools" class="mr-2" color="primary" size="small"/>
        <span>种子清理工</span>
        <v-spacer/>
        <div class="header-actions">
          <v-btn color="success"
                 @click="switch_tab('config')"
                 variant="text"
                 :disabled="state.scaning || state.clearing"
                 size="small"
                 density="compact"
                 class="header-action-btn">
            <template v-if="smAndDown">
              <v-icon icon="mdi-cog" size="18" />
            </template>
            <template v-else>
              <v-icon icon="mdi-cog" size="18" class="mr-1" />
              <span>配置页</span>
            </template>
          </v-btn>
          <v-btn color="primary"
                 @click="close"
                 variant="text"
                 :disabled="state.scaning || state.clearing"
                 size="small"
                 density="compact"
                 class="header-action-btn">
            <template v-if="smAndDown">
              <v-icon icon="mdi-close" size="18" />
            </template>
            <template v-else>
              <v-icon icon="mdi-close" size="18" class="mr-1" />
              <span>关闭</span>
            </template>
          </v-btn>
        </div>
      </v-card-title>

      <!-- 内容区域统一左右内边距 -->
      <v-card-text class="px-3 py-2">
      <!-- 工具条区域 - 卡片式 -->
      <v-card flat class="rounded mb-3 border config-card">
        <v-card-title
          class="text-subtitle-2 d-flex align-center px-3 py-2 bg-primary-lighten-5 cursor-pointer"
          @click.stop.prevent="toolbarRef?.toggleCollapse && toolbarRef.toggleCollapse()"
        >
          <v-icon icon="mdi-magnify" class="mr-2" color="primary" size="small" />
          <span>扫描选项</span>
          <v-spacer />
          <v-btn
            color="primary"
            icon="mdi-chevron-left"
            size="small"
            density="compact"
            variant="text"
            class="ml-auto mr-2 transition-button"
            :class="{ 'rotate-180': toolbarRef?.isCollapsed }"
            @click.stop.prevent="toolbarRef?.toggleCollapse && toolbarRef.toggleCollapse()"
          />
        </v-card-title>
        <v-card-text class="px-3 py-2">
          <ToolBar ref="toolbarRef"/>
          
          <!-- 第三行：操作按钮 - 独立于ToolBar，折叠时仍显示 -->
          <v-row class="mb-0 mt-n1 px-2">
            <v-col :cols="smAndDown ? 6 : 3">
              <v-btn 
                color="primary"
                @click="startScan(false)"
                variant="outlined"
                :size="smAndDown ? 'x-small' : 'small'"
                :density="smAndDown ? 'compact' : 'comfortable'"
                class="w-100 modern-action-btn"
                :class="smAndDown ? 'mobile-action-btn' : ''"
                :disabled="state.clearing"
                :loading="state.scaning"
                elevation="2"
              >
                <v-icon icon="mdi-magnify" :size="smAndDown ? '16' : 'small'" :class="smAndDown ? 'mr-1' : 'mr-2'"/>
                <span v-if="!smAndDown">开始扫描</span>
                <span v-else class="mobile-btn-text">开始扫描</span>
              </v-btn>
            </v-col>
            <v-col :cols="smAndDown ? 6 : 3">
              <v-btn 
                color="secondary"
                @click="downloadTracker"
                variant="outlined"
                :size="smAndDown ? 'x-small' : 'small'"
                :density="smAndDown ? 'compact' : 'comfortable'"
                class="w-100 modern-action-btn"
                :class="smAndDown ? 'mobile-action-btn' : ''"
                :disabled="state.scaning || state.clearing"
                elevation="2"
              >
                <v-icon :icon="smAndDown ? 'mdi-tray-arrow-down' : 'mdi-tray-arrow-down'" :size="smAndDown ? '16' : 'small'" :class="smAndDown ? 'mr-1' : 'mr-2'"/>
                <span v-if="!smAndDown">导出Tracker</span>
                <span v-else class="mobile-btn-text">导出Tracker</span>
              </v-btn>
            </v-col>
            <v-col :cols="smAndDown ? 6 : 3">
              <v-btn 
                color="warning"
                @click="resetParams"
                variant="outlined"
                :size="smAndDown ? 'x-small' : 'small'"
                :density="smAndDown ? 'compact' : 'comfortable'"
                class="w-100 modern-action-btn"
                :class="smAndDown ? 'mobile-action-btn' : ''"
                :disabled="state.scaning || state.clearing"
                elevation="2"
              >
                <v-icon icon="mdi-refresh" :size="smAndDown ? '16' : 'small'" :class="smAndDown ? 'mr-1' : 'mr-2'"/>
                <span v-if="!smAndDown">重置选项</span>
                <span v-else class="mobile-btn-text">重置选项</span>
              </v-btn>
            </v-col>
            <v-col :cols="smAndDown ? 6 : 3">
              <v-btn 
                color="error"
                @click="startCleanup"
                variant="outlined"
                :size="smAndDown ? 'x-small' : 'small'"
                :density="smAndDown ? 'compact' : 'comfortable'"
                class="w-100 modern-action-btn"
                :class="smAndDown ? 'mobile-action-btn' : ''"
                :disabled="state.scaning"
                :loading="state.clearing"
                elevation="2"
              >
                <v-icon :icon="smAndDown ? 'mdi-trash-can-outline' : 'mdi-trash-can-outline'" :size="smAndDown ? '16' : 'small'" :class="smAndDown ? 'mr-1' : 'mr-2'"/>
                <span v-if="!smAndDown">开始清理</span>
                <span v-else class="mobile-btn-text">开始清理</span>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <!-- 动态组件区域 -->
      <!-- 列表区域 - 卡片式，与上方卡片一致 -->
      <v-card flat class="rounded mb-3 border config-card">
        <v-card-title class="text-subtitle-2 d-flex align-center px-3 py-2 bg-primary-lighten-5">
          <v-icon icon="mdi-list-box" class="mr-2" color="primary" size="small"/>
          <span>列表区域</span>
          <v-spacer />
          <!-- 列表操作按钮 -->
          <div class="list-actions d-flex align-center">
            <v-btn color="primary"
                   @click="deleteAllRecord"            
                   :variant="'outlined'"
                   :size="smAndDown ? 'x-small' : 'small'"
                   :icon="smAndDown"
                   :class="'mr-2'"
                   :disabled="state.scaning || state.clearing">
                   <v-icon icon="mdi-broom" :size="smAndDown ? 18:'small'" />
                   <span class="ml-1" v-if="!smAndDown">清空记录</span>
            </v-btn>
            <v-btn color="success"
                   @click="addSelectedToCleanup"
                    :variant="'outlined'"
                   :size="smAndDown ? 'x-small' : 'small'"
                   :icon="smAndDown"
                   :class="'mr-2'"
                   :disabled="state.scaning || state.clearing">
              <v-icon icon="mdi-plus-box" :size="smAndDown ? 18:'small'"/>
              <span class="ml-1" v-if="!smAndDown">添加到待清理</span>
            </v-btn>
            <v-btn color="warning"
                   :variant="'outlined'"
                   :size="smAndDown ? 'x-small' : 'small'"
                   :icon="smAndDown"
                   :class="'mr-2'"
                   @click="toggleFilter"
                   :disabled="state.scaning || state.clearing">
              <v-icon icon="mdi-filter-variant" :size="smAndDown ? 18:'small'" />
               <span class="ml-1" v-if="!smAndDown">筛选条件</span>
            </v-btn>
               <v-btn color="#E91E63"
                   :variant="'outlined'"
                   :size="smAndDown ? 'x-small' : 'small'"
                   :icon="smAndDown"
                   :class="'mr-2'"
                   @click="toggleSort"
                   :disabled="state.scaning || state.clearing">
              <v-icon icon="mdi-sort" :size="smAndDown ? 18:'small'" />
               <span class="ml-1" v-if="!smAndDown">排序规则</span>
            </v-btn>
          </div>
        </v-card-title>
        <v-card-text class="px-3 py-2">
            <v-tabs v-model="state.listTab" bg-color="deep-purple-lighten-5" fixed-tabs>
            <v-tab value="scan" @click="setTab('scan')">
              <v-icon icon="mdi-magnify" class="mr-1" size="18" />
              扫描结果
            </v-tab>
            <v-tab value="cleanup" @click="setTab('cleanup')">
              <v-icon icon="mdi-trash-can-outline" class="mr-1" size="18" />
              等待清理
            </v-tab>
            </v-tabs>
        </v-card-text>
        
        <!-- 扫描结果选项卡内容 -->
        <div v-show="state.listTab == 'scan'" class="tab-content">
          <ScanResults :scan-res="state.scanRes"
                       :scan-params="state.scanParams"
                       :loading="state.scaning"
                       :initialConfig="state.initConfig"
                       @update:scanParams="handleScanParamsUpdate"
                       ref="scanResultsRef"
                       @applyFilter="applyFilter"
                       @applySort = "applySort"
          />
        </div>
        
        <!-- 等待清理选项卡内容 -->
        <div v-show="state.listTab == 'cleanup'" class="tab-content">
          <CleanupList ref="cleanupRef"/>
        </div>
      </v-card>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="state.snackbar.show"
                :timeout="3000"
                :color="state.snackbar.color"
                :location="state.snackbar.location"
    >
      {{ state.snackbar.message }}
    </v-snackbar>

  </div>
</template>

<script setup lang="ts">
import {onMounted, reactive, ref, Ref} from 'vue';
import ToolBar from './ToolBar.vue';
import ScanResults from './ScanResults.vue';
import CleanupList from './CleanupList.vue';
import {PLUGIN_ID, SnackbarModel, CombinedItem, ScanResult,ApiRequest,SortItem,FilterModel} from './definedFunctions.ts';

// 响应式断点：小屏幕（含）仅显示图标
import { useDisplay } from 'vuetify';
const { smAndDown } = useDisplay();

const emit = defineEmits(['close', 'switch']);

const props = defineProps({
  api: {
    type: Object,
    default: () => ({} as ApiRequest),
    required: true,
  },
});


interface PageState {
  listTab: string; // 'scan' | 'cleanup'
  scaning: boolean;
  clearing: boolean;
  scanRes: ScanResult
  scanParams: {
    page: number;
    pageSize: number;
    sortBy: SortItem[];
    filter:FilterModel;
  },
  snackbar: SnackbarModel,
  initConfig: Object // 初始配置
}

const toolbarRef = ref();
const cleanupRef = ref();
const scanResultsRef = ref();

// 当前激活的选项卡（'scan' 或 'cleanup'）
const state = reactive<PageState>({
  listTab: "scan",
  scaning: false,
  clearing: false,
  scanRes: {
    combinedList: [],
    total: 0,
    totalSize:0,
    tTotal: 0,
    tTotalSize:0,
    mTotal: 0,
    mTotalSize:0,
    page: 1,
    pageSize: 50
  },
  scanParams: {
    page: 1,
    pageSize: 50,
    sortBy: [{key: 'name', order: 'asc'}],
    filter:{
      path:"",
      client_name:"",
      client:"",
      seeds_limit_down:null,
      seeds_limit_up:null,
      seeds_limit: [null,null],
      size_limit_down:null,
      size_limit_up:null,
      size_limit: [null,null],
      live_time: 0,
    }
  },
  snackbar: {
    location: 'top',
    show: false,
    message: '',
    color: 'success'
  },
  initConfig:{}
});


// 设置当前 tab 并切换组件
const setTab = (name) => {
  state.listTab = name;
};

const switch_tab = (name) => {
  emit('switch', name);
};

const close = () => {
  emit('close');
};

const initData = ()=>{
  state.scanRes.combinedList = []
  // state.scanRes.total = 0;
  state.scanRes.tTotal = 0;
  state.scanRes.mTotal = 0;
  scanResultsRef.value.clearSelectedScans(); // 清除选中的扫描结果
}
const startScan = (isPageChange:boolean=false,isPageSizeChange:boolean=false,
     isSortChanged:boolean=false,filterChanged:boolean=false) => {
  // 触发开始扫描逻辑
  // console.log('开始扫描', `扫描参数: ${toolbarRef.value.state},isPageChange: ${isPageChange}`);
  state.scaning = true;
  initData()
  if (!isPageChange){
    state.scanParams.page = 1; // 如果不是分页变更，重置页码
  }


  // 这里可以调用 API 或其他逻辑来执行扫描
  let url = `plugin/${PLUGIN_ID}/scan?pageChange=${isPageChange}&pageSizeChange=${isPageSizeChange}&sortChange=${isSortChanged}&filterChange=${filterChanged}`
  const params = {...toolbarRef.value.state}
  params["page"] = state.scanParams.page
  params["limit"] = state.scanParams.pageSize
  params["sortBy"] = state.scanParams.sortBy
  params["filter"] = state.scanParams.filter
  console.log("startScan",params);
  props.api.post(url, params).then(res => {
    state.scanRes.combinedList = res.data.combined_list || [];
    state.scanRes.total = res.data.total || 0; 
    state.scanRes.tTotal = res.data.t_total || 0;
    state.scanRes.mTotal = res.data.m_total || 0;
    state.scanRes.totalSize = res.data.total_size||0;
    state.scanRes.tTotalSize = res.data.t_total_size||0;
    state.scanRes.mTotalSize = res.data.m_total_size||0;
    state.scanRes.page = res.data.page || 1;
    state.scanRes.pageSize = res.data.page_size || 50;
    // console.log('扫描结果:', state.scanRes);
    // 切换到扫描结果 tab
    setTab('scan');
  }).catch(error => {
    console.error('扫描失败:', error);
  }).finally(() => {
    state.scaning = false;
  });
};

const resetParams = () => {
  if (toolbarRef.value && toolbarRef.value.initParams) {
    toolbarRef.value.initParams(); // 调用 ToolBar 的 initParams 方法
    // console.log('参数已重置');
  } else {
    console.warn('ToolBar 或 initParams 方法未定义');
  }
};

const deleteAllRecord = () => {
  // 删除所有扫描结果
  // console.log('删除所有扫描结果');
  if (state.listTab == 'scan'){
    initData();
    state.scanRes.page = 1;
  }else if (state.listTab == 'cleanup'){
    cleanupRef.value && cleanupRef.value.deleteAllRecord()
  }
};
// 添加选中的扫描结果到待清理列表
// cleanupList 是一个包含选中项 hash 的数组
const addToCleanup = (cleanupList: Array<CombinedItem>) => {
  // 将选中的扫描结果添加到待清理列表
  console.log('添加到待清理', cleanupList.length);
  if (!cleanupList || cleanupList.length == 0) {
    showNotification("添加失败，未选择需要清理的项", 'error');
    return
  }
  let willCleanupList: CombinedItem[] = cleanupList
  cleanupRef.value.setCleanupList(willCleanupList)
};


// 添加当前选中的扫描结果到待清理列表
const addSelectedToCleanup = () => {
  if (scanResultsRef.value) {
    const selectedScans = scanResultsRef.value.getSelectedScans();
    addToCleanup(selectedScans);
  }
};

// 切换筛选对话框
const toggleFilter = () => {
  if (scanResultsRef.value) {
    scanResultsRef.value.toggleFilter();
  }
};

//切换排序对话框
const toggleSort = ()=>{
  if (scanResultsRef.value) {
    scanResultsRef.value.toggleSort();
  }
}
const startCleanup = () => {
  state.clearing = true
  // 开始执行清理任务
  let willCleanupList = cleanupRef.value.getCleanupList()
  props.api.post(`plugin/${PLUGIN_ID}/clear`, willCleanupList).then((res) => {
    if (res["code"]!='ok'){
       showNotification(`清理失败:${res["message"]}`, 'error');
    }else{
       showNotification('清理成功', 'success');
      cleanupRef.value.deleteAllRecord()
    }
    // console.info("清理完成", res)
    state.snackbar.show = true;
  }).catch((e) => {
    console.error("清理出错", e)
    showNotification('清理失败: ' + (e.message || '未知错误'), 'error');
  }).finally(() => {
    state.clearing = false
  })

};
const handleScanParamsUpdate = (newScanParams: { page: number; pageSize: number,
                              sort: SortItem[], changed:string }) => {
  let isPageChanged = false
  let isPageSizeChanged = false
  let isSortChanged = false;
  if (newScanParams.changed === 'page') {
    isPageChanged = true;
  } else if (newScanParams.changed === 'pageSize') {
    isPageSizeChanged = true;
  } else if (newScanParams.changed === 'sort') {
    isSortChanged = true;
  }
  if (isPageChanged) {
    // 如果是页码变更，更新页码
    state.scanParams.page = Number(newScanParams.page);
  } else if (isPageSizeChanged) {
    // 如果是页大小变更，更新页大小
      state.scanParams.pageSize = Number(newScanParams.pageSize);
  }
  // 修复类型不匹配问题，创建符合SortItem接口定义的对象数组
  if (isSortChanged){
    const sortItem: SortItem = {
          key: newScanParams.sort[0].key,
          order: newScanParams.sort[0].order as any,
        };
    state.scanParams.sortBy = [sortItem];
  }
   
  // 调用 API 或方法加载新页面的数据
  startScan(isPageChanged,isPageSizeChanged, isSortChanged);
};

// 过滤扫描
const applyFilter = (filter: FilterModel) => {
  // 更新过滤条件
  state.scanParams.filter.path = filter.path || "";
  state.scanParams.filter.client_name = filter.client_name||"";
  state.scanParams.filter.client = filter.client||"";
  state.scanParams.filter.seeds_limit = filter.seeds_limit||[];
  state.scanParams.filter.size_limit = filter.size_limit||[];
  state.scanParams.filter.size_limit = filter.size_limit||[];
  state.scanParams.filter.live_time = filter.live_time||0;
  // 重新开始扫描
  startScan(false, false, false, true);
};

//
const applySort = (sortOptionList: SortItem[]) => {
  // console.log("applySort", sortOptionList);
   state.scanParams.sortBy = sortOptionList;
   startScan(false, false, true, false);
};

// 下载Tracker
const downloadTracker = async () => { 
  let url = `/plugin/${PLUGIN_ID}/tracker-list`;
  try {
    const res = await props.api.get(url);
    // console.log("downloadTracker=>>", res);
    const tracker_list: Array<string> = res.data;
    if (tracker_list && tracker_list.length > 0) {
      // 1. 将数组项通过换行符连接成一个字符串
      const fileContent = tracker_list.join('\n');
      // 2. 创建一个 Blob 对象
      const blob = new Blob([fileContent], { type: 'text/plain;charset=utf-8' });
      // 3. 创建一个 URL 指向 Blob
      const blobUrl = URL.createObjectURL(blob);
      // 4. 创建一个临时的 a 标签来触发下载
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = 'trackers.txt'; // 设置下载的文件名
      // 5. 模拟点击链接并移除
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(blobUrl); // 释放 Blob URL 资源
      showNotification("下载成功！", "success");
    } else {
      showNotification("空数据，无法下载", "error");
    }
  } catch (err) {
    showNotification("下载失败！", "error");
    console.log("downloadTracker error=>>", err);
  }
};

// 消息通知
const showNotification = (text, color = 'success')=> {
  state.snackbar.message = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}

// 获取配置
const getConfig = ()=>{
  let url = `/plugin/${PLUGIN_ID}/config`;
  props.api.get(url).then(res=>{
    state.initConfig = res;
  })
}

onMounted(()=>{
  getConfig();
})
</script>
<style lang="scss" scoped>
.plugin-page {
  margin: 0 auto;
  padding: 0.5rem;
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.07);
}

.border {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.text-subtitle {
  font-weight: 500;
  margin-bottom: 2px;
}

.text-subtitle-1 {
  font-size: 1.1rem !important;
}

.text-subtitle-2 {
  font-size: 0.9rem !important;
  font-weight: 500;
  margin-bottom: 2px;
}

/* 卡片式外观与间距优化，与logsclean风格保持一致 */
.config-card {
  background-image: linear-gradient(to right, rgba(var(--v-theme-surface), 0.98), rgba(var(--v-theme-surface), 0.95)),
                   repeating-linear-gradient(45deg, rgba(var(--v-theme-primary), 0.03), rgba(var(--v-theme-primary), 0.03) 10px, transparent 10px, transparent 20px);
  background-attachment: fixed;
  box-shadow: 0 1px 2px rgba(var(--v-border-color), 0.05) !important;
  transition: all 0.3s ease;
}

.config-card:hover {
  box-shadow: 0 3px 6px rgba(var(--v-border-color), 0.1) !important;
}

/* 顶部标题按钮组间距更紧凑 */
.header-actions {
  display: inline-flex;
  gap: 4px; /* 更小的按钮间距 */
  align-items: center;
}

.header-action-btn {
  min-width: 0;
  padding-left: 4px;
  padding-right: 4px;
}

/* 列表区域按钮间距更紧凑 */
.list-actions > .v-btn {
  min-width: 0;
  padding-left: 4px !important;
  padding-right: 4px !important;
}
/* 折叠按钮动画（与 ToolBar 保持一致） */
.transition-button {
  transition: transform 0.3s ease;
}
.rotate-180 {
  transform: rotate(180deg);
}

// 按钮样式
.w-100 {
  width: 100% !important;
}

// 现代化操作按钮样式
.modern-action-btn {
  border-radius: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  text-transform: none !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  position: relative !important;
  overflow: hidden !important;
  min-height: 36px !important;
  
  // 默认状态
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
  }
  
  // 悬浮效果
  &:hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    
    &::before {
      left: 100%;
    }
  }
  
  // 点击效果
  &:active:not(:disabled) {
    transform: translateY(0) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
  }
  
  // 禁用状态
  &:disabled {
    opacity: 0.6 !important;
    transform: none !important;
    box-shadow: none !important;
  }
  
  // 加载状态
  &.v-btn--loading {
    transform: none !important;
  }
}

// 为不同颜色的按钮添加特殊效果
.modern-action-btn.v-btn--color-primary {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-primary), 0.8)) !important;
  border: none !important;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, rgb(var(--v-theme-primary), 0.9), rgb(var(--v-theme-primary), 0.7)) !important;
  }
}

.modern-action-btn.v-btn--color-secondary {
  background: linear-gradient(135deg, rgb(var(--v-theme-secondary)), rgb(var(--v-theme-secondary), 0.8)) !important;
  border: none !important;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, rgb(var(--v-theme-secondary), 0.9), rgb(var(--v-theme-secondary), 0.7)) !important;
  }
}

.modern-action-btn.v-btn--color-warning {
  background: linear-gradient(135deg, rgb(var(--v-theme-warning)), rgb(var(--v-theme-warning), 0.8)) !important;
  border: none !important;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, rgb(var(--v-theme-warning), 0.9), rgb(var(--v-theme-warning), 0.7)) !important;
  }
}

.modern-action-btn.v-btn--color-error {
  background: linear-gradient(135deg, rgb(var(--v-theme-error)), rgb(var(--v-theme-error), 0.8)) !important;
  border: none !important;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, rgb(var(--v-theme-error), 0.9), rgb(var(--v-theme-error), 0.7)) !important;
  }
}

// 移动端按钮优化样式
.mobile-action-btn {
  min-height: 32px !important;
  max-height: 32px !important;
  padding: 0 8px !important;
  font-size: 0.75rem !important;
  border-radius: 8px !important;
  
  // 移动端按钮文字样式
  .mobile-btn-text {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
  
  // 移动端图标样式
  .v-icon {
    font-size: 16px !important;
  }
  
  // 移动端悬浮效果简化
  &:hover:not(:disabled) {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
  }
  
  // 移动端点击效果简化
  &:active:not(:disabled) {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
  }
}

// 移动端响应式布局优化
@media (max-width: 960px) {
  // 移动端按钮行间距调整
  .v-row {
    margin-bottom: 12px !important;
  }
  
  // 移动端按钮列间距调整
  .v-col {
    padding: 4px !important;
  }
  
  // 移动端按钮容器内边距调整
  .px-2 {
    padding-left: 8px !important;
    padding-right: 8px !important;
  }
  
  // 移动端按钮组上边距调整
  .mt-n1 {
    margin-top: 8px !important;
  }
}

/* 选项卡内容样式 */
.tab-content {
  margin: 0;
  padding: 0;
}

.tab-content .v-card {
  margin: 0;
  border-radius: 0;
  box-shadow: none;
}
</style>