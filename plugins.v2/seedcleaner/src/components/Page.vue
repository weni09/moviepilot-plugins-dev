<template>
  <div class="plugin-common plugin-page">
    <v-card flat class="rounded border">
      <v-card-title class="text-subtitle text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
        <v-icon icon="mdi-tools" class="mr-2" color="primary" size="small"/>
        <span>种子清理工</span>
        <v-card-subtitle class="ml-2">详情页</v-card-subtitle>
        <v-spacer/>
        <v-btn color="success"
               icon
               @click="switch_tab('config')"
               variant="tonal"
               :disabled="state.scaning || state.clearing"
               size="small"
               class="mr-4">
               <v-icon icon="mdi-cog" size="small"/>
               <v-tooltip activator="parent" location="top">配置页</v-tooltip>
        </v-btn>
        <v-btn color="primary"
               @click="close"
               icon
               :disabled="state.scaning || state.clearing"
               variant="tonal"
               size="small"
               class="mr-4"
               >
                <v-icon icon="mdi-close" size="small"/>
               <v-tooltip activator="parent" location="top">关闭</v-tooltip>
        </v-btn>
      </v-card-title>

      <!-- 工具条区域 -->
      <ToolBar ref="toolbarRef"/>
      <v-divider/>
      <!-- 动态组件区域 -->
      <!-- 选项卡标题 -->
      <v-card flat class="px-2 py-1">
        <v-card-title class="text-subtitle-2 d-flex align-center px-3 py-2 bg-primary-lighten-5">
          <v-icon icon="mdi-list-box" class="mr-2" color="primary" size="small"/>
          <span>列表区域</span>
          <v-spacer/>
          <div class="d-flex">
            <v-btn color="primary"
               @click="startScan(false)"
               icon
               variant="tonal"
               :disabled="state.clearing"
               :loading="state.scaning"
               size="small"
               class="ml-4 mr-4">
               <v-icon icon="mdi-magnify" size="small"/>
               <v-tooltip activator="parent" location="top">开始扫描</v-tooltip>
            </v-btn>
            <v-btn
                color="warning"
                @click="resetParams"
                icon
                variant="tonal"
                :disabled="state.scaning || state.clearing"
                size="small"
                class="mr-4">
              <v-icon icon="mdi-refresh" size="small"/>
              <v-tooltip activator="parent" location="top">重置选项</v-tooltip>
            </v-btn>
            <v-btn color="error"
               @click="startCleanup"
               icon
               variant="tonal"
               :disabled="state.scaning"
               :loading="state.clearing"
               class="mr-4" size="small">
               <v-icon icon="mdi-trash-can-outline" size="small"/>
               <v-tooltip activator="parent" location="top">开始清理</v-tooltip>
            </v-btn>
          </div>
          <div>

          </div>
        </v-card-title>
        <v-tabs v-model="state.listTab" grow>
          <v-tab value="scan" @click="setTab('scan')">扫描结果</v-tab>
          <v-tab value="cleanup" @click="setTab('cleanup')">待清理</v-tab>
        </v-tabs>
        <!-- <component :is="currentTabComponent"/> -->
        <ScanResults v-show="state.listTab == 'scan'"
                     :scan-res="state.scanRes"
                     @delete-all-record="deleteAllRecord"
                     @add-to-cleanup="addToCleanup"
                     :scan-params="state.scanParams"
                     :loading="state.scaning"
                     @update:scanParams="handleScanParamsUpdate"
                     ref="scanResultsRef"
                     @applyFilter="applyFilter"
        />
        <CleanupList v-show="state.listTab == 'cleanup'" ref="cleanupRef"/>
      </v-card>
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
import {reactive, ref, Ref} from 'vue';
import ToolBar from './ToolBar.vue';
import ScanResults from './ScanResults.vue';
import CleanupList from './CleanupList.vue';
import {PLUGIN_ID, SnackbarModel, CombinedItem, ScanResult,ApiRequest,SortItem} from './definedFunctions.ts';


const emit = defineEmits(['close', 'switch']);

const props = defineProps({
  api: {
    type: Object,
    default: () => ({} as ApiRequest),
    required: true,
  },
  initialConfig: {
    type: Object,
    default: () => ({}),
  }
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
    filter:{
      path:string;
    }
  },
  snackbar: SnackbarModel
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
    }
  },
  snackbar: {
    location: 'top',
    show: false,
    message: '',
    color: 'success'
  }
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
  console.log('开始扫描', `扫描参数: ${toolbarRef.value.state},isPageChange: ${isPageChange}`);
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
  params["sortBy"] = [state.scanParams.sortBy[0].key,state.scanParams.sortBy[0].order]
  params["filter"] = state.scanParams.filter
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
    console.log('参数已重置');
  } else {
    console.warn('ToolBar 或 initParams 方法未定义');
  }
};

const deleteAllRecord = () => {
  // 删除所有扫描结果
  // console.log('删除所有扫描结果');
  initData();
  state.scanRes.page = 1;
};
// 添加选中的扫描结果到待清理列表
// cleanupList 是一个包含选中项 hash 的数组
const addToCleanup = (cleanupList: Array<CombinedItem>) => {
  // 将选中的扫描结果添加到待清理列表
  console.log('添加到待清理', cleanupList.length);
  if (!cleanupList || cleanupList.length == 0) {
    state.snackbar.message = "添加失败，未选择需要清理的项"
    state.snackbar.color = 'error';
    state.snackbar.show = true;
    return
  }
  let willCleanupList: CombinedItem[] = cleanupList
  cleanupRef.value.setCleanupList(willCleanupList)
};

const startCleanup = () => {
  state.clearing = true
  // 开始执行清理任务
  let willCleanupList = cleanupRef.value.getCleanupList()
  props.api.post(`plugin/${PLUGIN_ID}/clear`, willCleanupList).then((res) => {
    if (res["code"]!='ok'){
       state.snackbar.message = `清理失败:${res["message"]}`;
       state.snackbar.color = 'error';
    }else{
      state.snackbar.message = '清理成功';
      state.snackbar.color = 'success';
      cleanupRef.value.deleteAllRecord()
    }
    // console.info("清理完成", res)
    state.snackbar.show = true;
  }).catch((e) => {
    console.error("清理出错", e)
    state.snackbar.message = '清理失败: ' + (e.message || '未知错误');
    state.snackbar.color = 'error';
    state.snackbar.show = true;
  }).finally(() => {
    state.clearing = false
  })

};
const handleScanParamsUpdate = (newScanParams: { page: number; pageSize: number,
                              sort: [{key:string,order: boolean | "desc" | "asc" | undefined}], changed:string }) => {
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
          order: newScanParams.sort[0].order as ("desc" | "asc" | undefined)
        };
    state.scanParams.sortBy = [sortItem];
  }
   
  // 调用 API 或方法加载新页面的数据
  startScan(isPageChanged,isPageSizeChanged, isSortChanged);
};

// 过滤扫描
const applyFilter = (filter: { path: string }) => {
  // 更新过滤条件
  state.scanParams.filter.path = filter.path;
  // 重新开始扫描
  startScan(false, false, false, true);
};

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
</style>