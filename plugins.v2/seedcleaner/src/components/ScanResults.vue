<template>
  <v-card flat class="mb-4">
    <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
      <div class="d-flex align-center mr-4">
        <v-chip class="ml-2" size="x-small" color="info" variant="flat" v-if="totalComputed!=''">
          {{ totalComputed }}
        </v-chip>
        <v-chip class="ml-2" size="x-small" color="error" variant="flat">
          {{ `已选择 ${state.selectedScans.length}项: ${selectedScansSize}` }}
        </v-chip>
        </div>
         <v-spacer />
      <v-select
          v-model="scanParams.pageSize"
          :items="[50, 100, 200, 300, 500]"
          label="每页数量"
          variant="underlined"
          density="compact"
          size="small"
          style="max-width: 120px;"
          @update:modelValue="handlePageSizeChange"
      ></v-select>
      <v-pagination
          v-model="scanParams.page"
          :length="totalPages"
          @update:modelValue="handlePageChange"
          rounded="circle"
          size="small"
          class="mr-8"
          :total-visible="5"
      ></v-pagination>
     
      <v-btn color="primary"
             @click="deleteAllRecord"
             class="mr-4"
             icon
             size="small">
             <v-icon icon="mdi-broom" size="small"/>
             <v-tooltip activator="parent" location="top">清空记录</v-tooltip>
      </v-btn>
      <v-btn color="success"
             @click="addToCleanup"
             icon
             size="small"
             class="mr-4"
             >
              <v-icon icon="mdi-plus-box" size="small"/>
             <v-tooltip activator="parent" location="top">添加到待清理</v-tooltip>
      </v-btn>
       <v-btn color="warning"
          icon
          size="small"
          class="mr-4"
          @click="toggleFilter">
          <v-icon icon="mdi-filter-variant" size="small" />
        <v-tooltip activator="parent" location="top">筛选条件</v-tooltip>
       </v-btn>
        <v-dialog v-model="filterDialog" max-width="400px">
          <v-card>
            <v-card-title>条件筛选</v-card-title>
            <v-card-text>
              <v-row align="center" :gutters="1" class="d-flex align-center align-content-center">
                <v-col cols="4"> 
                <v-select
                    v-model="state.filterName"
                    :items="filterItems"
                    variant="outlined"
                    density="compact"
                    class="mb-3 text-caption"
                    hint="筛选字段名称"
                 />
                </v-col>
               <v-col cols="8">
                <v-text-field
                  v-model="state.filter[state.filterName]"
                  :label="`输入筛选${getfilterTitleByKey(state.filterName)}`"
                  @keyup.enter="applyFilter"
                  density="compact"
                  autofocus
                ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="deleteFilter(state.filterName)">取消</v-btn>
              <v-btn color="primary" @click="applyFilter">确定</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-card-title>
    <v-card-text class="pa-0">
      <div class="filter-chips d-flex ">
      <v-chip
        closable
        prepend-icon="mdi-folder-arrow-left"
        variant="outlined"
        @click:close="deleteFilter(state.filterName)"
        v-if="state.filter[state.filterName]"
      >{{ state.filter[state.filterName] }}</v-chip>
      </div>
      <v-data-table-server
        :headers="state.headers"
        :hide-default-header="false"
        :items="props.scanRes.combinedList"
        :items-per-page="scanParams.pageSize"
        :page="scanParams.page"
        :item-count="props.scanRes.total"
        :items-length="props.scanRes.total"
        :sort-by.sync="props.scanParams.sortBy"
        :item-value="item => item"
        :loading="props.loading"
        v-model="state.selectedScans"
        must-sort
        fixed-header
        height="420px"
        density="default"
        hover
        hide-default-footer
        show-expand
        show-select
        expand-on-click
        @update:sortBy="handleSortChange"
        @update:page="handlePageChange"
        @update:items-per-page="handlePageSizeChange">
  <template #loading>
        <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
  </template>
  <template #item.name="{ item }">
     <v-chip
            :color="item.hasOwnProperty('client') && item.client === 'transmission' ? 'primary' : 'error'"
            size="small"
            text-color="white"
            v-if="item.hasOwnProperty('client') && item.client">
            {{ (item.client || '').slice(0, 2) }}
          </v-chip>
          <span class="name-text">{{ item.name }}</span>
  </template>
  <template #item.path="{ item }">
    <span>{{ item.path.replace(item.name,"") }}</span>
    <v-btn icon="mdi-content-copy" size="x-small" @click.stop="_copyPath(item.path)" style="margin-left: 8px;"></v-btn>
  </template>
  <template #item.tracker="{ item }">
    <div v-if="item.type === 'torrent' && item?.trackers.length > 0">
      <v-chip
        :color="getColorByString(item.trackers)"
        text-color="white"
        size="small"
        class="mr-1 mb-1"
      >
        {{ mapTrackers(item.trackers)[0] }}
      </v-chip>
    </div>
    <div v-else>
      <v-chip color="info" text-color="white" size="small">
        无 Tracker
      </v-chip>
    </div>
  </template>
  <template #item.status="{ item }">
    <v-chip
      :color="item.data_missing ? 'error' : 'success'"
      size="small"
      text-color="white"
      v-if="item.type === 'torrent'"
    >
      {{ item.data_missing ? '缺失源文件' : '包含源文件' }}
    </v-chip>
     <v-chip color="warning" 
     size="small" 
     text-color="white" 
     v-else-if="item.type === 'file'"> 缺失种子
    </v-chip>
  </template>

  <template #item.size="{ item }">
    {{ item.size ? `${formatBytes(item.size)}` : '未知大小' }}  
  </template>
  <template #expanded-row="{ item }">
    <tr>
      <td colspan="100%">
        <v-table density="compact">
          <thead>
            <tr>
              <th class="text-left">
                Hash
              </th>
              <th class="text-left">
                客户端名称
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-left">
                  {{ item.hash }}
              </td>
              <td class="text-left">
                  {{ `${item.type == 'torrent'?item.client_name:'-' }`}}
              </td>
            </tr>
          </tbody>
        </v-table>
      </td>
    </tr>
  </template>
  <template #item.select="{ item }">
    <v-checkbox v-model="state.selectedScans" :value="item" hide-details/>
  </template>

</v-data-table-server>
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
import {ref, computed, reactive, watch} from 'vue';
import type {PropType} from 'vue';
import {formatBytes, SnackbarModel,CombinedItem, ScanResult,copyPath,mapTrackers,SortItem} from "./definedFunctions";


interface StateModel {
  selectedScans: Array<CombinedItem>; // 包含 data_missing 可选属性
  snackbar: SnackbarModel;
  headers: any[];
  filterName: string;
  filter:Record<string,any>
}

const props = defineProps({
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
      sortBy: []
    })
  },
  loading: {
    type: Boolean,
    default: false
  },
});

const emit = defineEmits(['deleteAllRecord', 'addToCleanup', 'update:scanParams','applyFilter']);
const filterItems = [{
  title:"路径",
  value:"path"
}]
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
      { value: 'path', title: '路径',align:"left", sortable: true,maxWidth:"12rem", },
      { value: 'tracker', title: 'Tracker',align:"center", },
      { value: 'status', title: '状态' ,align:"center",},
      { value: 'size', title: '大小', sortable: true,align:"center", },
      { value: 'select', title: '',key:"data-table-select"}],
  filterName:"path",
  filter:{}
})
const getfilterTitleByKey = (key: string) => { 
  for (let i of filterItems) {
    if (i.value === key) {
      return i.title;
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
// 获取所有可选的唯一标识符（info_hash + hash），包含 data_missing
// const allScanKeys = computed(() => {
//   const Keys = props.scanRes.combinedList.map(item => ({
//     hash: item.hash,
//     size: item.size,
//     data_missing: item.data_missing // 确保包含 data_missing 属性
//   }));
//   return [...Keys];
// });

// 全选状态绑定
// const selectAllScans = computed({
//   get: () => allScanKeys.value.length > 0 && state.selectedScans.length === allScanKeys.value.length,
//   set: (value) => {
//     if (value) {
//       state.selectedScans = [...allScanKeys.value];
//     } else {
//       state.selectedScans = [];
//     }
//   }
// });

// 消息通知
const showNotification = (text, color = 'success')=> {
  state.snackbar.message = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}

const deleteAllRecord = () => {
  state.selectedScans = [];
  emit('deleteAllRecord');
};
const addToCleanup = () => {
  // console.log("添加到待清理列表", state.selectedScans);
  emit('addToCleanup', state.selectedScans);
};

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
// 排序改变
const handleSortChange = (items:any)=>{
  console.log("handleSortChange",items)
  emit('update:scanParams', {
    pageSize: props.scanParams.pageSize,
    page: props.scanParams.page, // 切换每页数量后跳转到第一页
    sort: items,
    changed:"sort"
  });
}
const clearSelectedScans = ()=>{
  state.selectedScans = [];
}

const _copyPath = async (path: string) => {
  showNotification("完整路径已复制到剪贴板");
  if (await copyPath(path)){
    showNotification("完整路径已复制到剪贴板");
  }else{
    showNotification("复制路径失败","error");
  }
};

const availableColors = ['primary', 'secondary', 'success', 'info', 'warning', 'error', 'accent'];

// 根据字符串生成颜色索引
const getColorByString = (strs: string[]): string => {
  let strsArray = strs.sort()
  let _strs = strsArray.join("");
  let hash = 0;
  for (let i = 0; i < _strs.length; i++) {
    hash = _strs.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash % availableColors.length);
  return availableColors[index];
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

const filterDialog = ref(false);
const toggleFilter = () => {
  filterDialog.value = true;
};

//应用筛选
const applyFilter = () => {
  console.log('应用筛选，路径包含：',state.filterName, state.filter[state.filterName]);
  filterDialog.value = false;
  if (!state.filter[state.filterName]){
    return
  }
  emit('applyFilter', state.filter)
};

// 删除筛选条件
const deleteFilter = (name:string)=>{
  state.filter[name] = ''
  filterDialog.value = false;
  emit('applyFilter', state.filter)
};

defineExpose({
  clearSelectedScans,
  
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
</style>