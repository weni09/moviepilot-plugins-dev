<template>
  <v-card flat>
    <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
      
      <v-chip class="ml-2" size="x-small" color="error" variant="flat">
        数量：{{ state.cleanupList.length }}, 总大小：{{ totalSize }}
      </v-chip>
      <v-spacer/>
            <v-btn color="primary"
             @click="deleteAllRecord"
             class="mr-4"
             icon
             size="small">
             <v-icon icon="mdi-broom" size="small"/>
             <v-tooltip activator="parent" location="top">清空记录</v-tooltip>
      </v-btn>
    </v-card-title>
    <v-card-text class="pa-0">
      <v-table fixed-header height="300px" hover>
        <thead>
          <tr>
            <th class="text-left name-column">名称</th>
            <th class="text-left">删除选项</th>
            <th class="text-left">大小</th>
            <th class="text-right size-column">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in state.cleanupList" :key="item.hash">
             <td class="name-column">
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
                  <v-btn icon="mdi-content-copy" size="x-small" @click.stop="_copyPath(item.path)" style="margin-left: 8px;"></v-btn>
                 </div>
                </template>
             <span>{{ item.path }}</span> <!-- 提示显示完整路径 -->
           </v-tooltip>
            </td>
            <template v-if="item.type=='torrent'"> 
             <td>
               <v-chip
                  :color="deleteOptionText(item).color"
                  size="small"
                  text-color="white"
                >
                {{ deleteOptionText(item).text }}
              </v-chip>
            </td>
            <td>
              {{ itemSizeText(item) }}
            </td>
            </template>
            <template v-else-if="item.type=='file'">
              <td>
              <v-chip
                  :color="deleteOptionText(item).color"
                  size="small"
                  text-color="white"
                >
                {{ deleteOptionText(item).text }}
              </v-chip></td>
              <td class="size-column">{{ formatBytes(item.size) }}</td>
            </template>  
            <td class="text-right">
              <v-btn icon size="small" @click="removeFromCleanup(item)" color="error">
                <v-icon>mdi-delete</v-icon>
                <v-tooltip activator="parent" location="top">从待清理中移除</v-tooltip>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
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
import { computed ,reactive} from 'vue';
import {CombinedItem,ONLY_TORRENT,formatBytes,
  SnackbarModel,ALL,copyPath} from './definedFunctions.ts';

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

// 一个函数：删除来添加项目到待清理列表
const removeFromCleanup = (item: CombinedItem) => {
   state.cleanupList = state.cleanupList.filter(
      i => i.hash !== item.hash
    );
};


// 
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
  // 这里可以添加其他清理逻辑
  // console.log('已清空待清理记录');
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
  showNotification("路径已复制到剪贴板");
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
<style lang="scss" scoped>
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