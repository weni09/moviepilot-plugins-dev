<template>
  <v-card flat class="mb-4">
    <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
      <span>扫描记录</span>
      <v-btn color="primary"
             @click="deleteAllRecord"
             class="ml-2"
             prepend-icon="mdi-magnify"
             size="small">清空记录
      </v-btn>
      <v-btn color="success"
             @click="addToCleanup"
             class="ml-2"
             prepend-icon="mdi-plus-box"
             size="small">添加到待清理
      </v-btn>
       <v-chip class="ml-2" size="x-small" color="info" variant="flat" v-if="totalComputed!=''">
        {{ totalComputed }}
      </v-chip>
      <v-chip class="ml-2" size="x-small" color="error" variant="flat">
        {{ `已选择 ${state.selectedScans.length}项` }}
      </v-chip>
      <v-spacer/>
      <v-select
          v-model="scanParams.pageSize"
          :items="[50, 100, 200, 300, 500]"
          label="每页数量"
          variant="outlined"
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
          :total-visible="5"
      ></v-pagination>
    </v-card-title>
    <v-card-text class="pa-0">
      <v-table fixed-header height="320px" density="compact" hover>
        <thead>
        <tr>
          <th class="text-left">
            <v-checkbox v-model="selectAllScans" hide-details/>
          </th>
          <th class="text-left name-column">名称</th>
          <th class="text-left">Tracker</th>
          <th class="text-left">状态</th>
          <th class="text-left size-column">大小</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in props.scanRes.combinedList" :key="item.hash">
          <td>
            <v-checkbox v-model="state.selectedScans" :value="item.hash" hide-details/>
          </td>
          <td class="name-column" >
            <v-tooltip location="bottom">
              <template #activator="{ props }">
               <div v-bind="props" style="display: flex; align-items: center;">
                 <v-chip 
                  :color="item.hasOwnProperty('client') && item.client === 'transmission' ? 'primary' : 'error'"
                  size="small" 
                  text-color="white"
                  v-if="item.hasOwnProperty('client') && item.client">
                  {{ (item.client || '').slice(0, 2) }}
                  </v-chip>
              <span style="margin-left: 8px;">{{ item.name }}</span>
             </div>
            </template>
             <span>{{ item.path }}</span> <!-- 提示显示完整路径 -->
           </v-tooltip>
        </td>
          <template v-if="item.type === 'torrent'">
            <td>
              {{item.trackers.length > 0
                ? item.trackers.join(', ')
                : '无 Tracker'}}
            </td>
            <td>
              <v-chip
                  :color="item.data_missing ? 'error' : 'success'"
                  size="small"
                  text-color="white"
              >
                {{ item.data_missing ? '缺失源文件' : '包含源文件' }}
              </v-chip>
            </td>
          </template>
          <template v-else-if="item.type === 'file'">
            <td>无 Tracker</td>
            <td>
              <v-chip color="warning" size="small" text-color="white">缺失种子</v-chip>
            </td>
          </template>
          <td class="size-column">{{ item.size ? `${formatBytes(item.size)}` : '未知大小' }}</td>
        </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import {ref, computed, reactive} from 'vue';
import type {PropType} from 'vue';
import {formatBytes, CombinedItem, ScanResult} from "./definedFunctions";

interface StateModel {
  selectedScans: string[]
}

const props = defineProps({
  scanRes: {
    type: Object as PropType<ScanResult>,
    default: () => ({
      combinedList: [],
      total: 0,
      t_total:0,
      m_total:0,
      page: 1,
      pageSize: 50
    })
  },
  scanParams: {
    type: Object as PropType<{
      page: number;
      pageSize: number;
    }>,
    required: true,
    default: () => ({
      page: 1,
      pageSize: 50
    })
  }
});


const emit = defineEmits(['deleteAllRecord', 'addToCleanup', 'update:scanParams']);

const state = reactive<StateModel>({
  selectedScans: [],

})
// 计算总数和缺失文件数量
const totalComputed = computed(() => {
  let res :string[]= []
  if (props.scanRes.tTotal>0){
    let torrentFIleText = `种子：${props.scanRes.tTotal}`;
    res.push(torrentFIleText);
  }
  if (props.scanRes.mTotal>0){
    let missingFileText = `缺失种子的文件：${props.scanRes.mTotal}`;
    res.push(missingFileText);
  }
  if (props.scanRes.tTotal>0 && props.scanRes.mTotal>0){
    let totalText=`总计：${props.scanRes.total}`;
    res.push(totalText);
  }
  return  res.join(' | ');
});
// 获取所有可选的唯一标识符（info_hash + hash）
const allScanKeys = computed(() => {
  const Keys = props.scanRes.combinedList.map(item => item.hash);
  return [...Keys];
});

// 全选状态绑定
const selectAllScans = computed({
  get: () => allScanKeys.value.length > 0 && state.selectedScans.length === allScanKeys.value.length,
  set: (value) => {
    if (value) {
      state.selectedScans = [...allScanKeys.value];
    } else {
      state.selectedScans = [];
    }
  }
});


const deleteAllRecord = () => {
  state.selectedScans = []
  emit('deleteAllRecord')
};
const addToCleanup = () => {
  // console.log("添加到待清理列表", state.selectedScans);
  emit('addToCleanup', state.selectedScans);
};

const totalPages = computed(() => {
     return Math.ceil(props.scanRes.total / props.scanParams.pageSize);
});

const handlePageChange = (newPage: number) => {
  emit('update:scanParams', {
    pageSize: props.scanParams.pageSize,
    page: newPage,
    changed:"page"
  });
};
 const handlePageSizeChange = (newPageSize: number) => {
     emit('update:scanParams', {
       pageSize: newPageSize,
       page: 1, // 切换每页数量后跳转到第一页
       changed:"pageSize"
     });
   };
const clearSelectedScans = ()=>{
  state.selectedScans = [];
}
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
}
</style>