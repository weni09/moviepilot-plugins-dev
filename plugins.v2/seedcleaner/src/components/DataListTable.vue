<template>
 <div>
 <v-data-table-server
        v-if="!props.loading && props.scanRes.combinedList.length > 0"
        :headers="props.headers"
        :hide-default-header="false"
        :items="props.scanRes.combinedList"
        :items-per-page="scanParams.pageSize"
        :page="scanParams.page"
        :item-count="props.scanRes.total"
        :items-length="props.scanRes.total"
        :sort-by.sync="props.scanParams.sortBy"
        :item-value="item => item"
        :loading="props.loading"
        :model-value="props.selectedScans"
        @update:model-value="selectedScansChange"
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
    <span>{{ item.path.replace(`/${item.name}`,"").replace(`\\${item.name}`,"") }}</span>
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
      :color="getStatusColor(item.status)"
      size="small"
      text-color="white"
      v-if="item.type === 'torrent'"
    >
      {{ item.status }}
    </v-chip>
     <v-chip color="warning" 
     size="small" 
     text-color="white" 
     v-else-if="item.type === 'file'"> 缺失种子
    </v-chip>
  </template>
  <template #item.seeds="{ item }">
    {{ item.type === 'torrent' ? item.seeds : '-' }}
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
              <th class="text-center">
                Hash
              </th>
              <th class="text-left">
                下载器名称
              </th>
              <th class="text-center">
                错误信息
              </th>
              <th class="text-center">
                存活时间
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-center">
                  {{ item.hash }}
              </td>
              <td class="text-left">
                  {{ `${item.type == 'torrent'?item.client_name:'-' }`}}
              </td>
                <td class="text-center text-error">
                  {{ `${item.type == 'torrent' && item.error?item.error:'-' }` }}
              </td>
                  <td class="text-center text-success">
                  {{ `${item.type == 'torrent' && formatCreatedTime(item.created_at) != ""? formatCreatedTime(item.created_at) :"-" }` }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </td>
    </tr>
  </template>
  <template #item.select="{ item }">
    <v-checkbox :model-value="props.selectedScans" @update:model-value="selectedScansChange($event)"  
    :value="item" hide-details/>
  </template>
   </v-data-table-server>
</div>
</template>

<script lang="ts" setup> 
import type {PropType} from 'vue';
import {formatBytes,CombinedItem, ScanResult,copyPath,mapTrackers,SortItem,formatTimeSince,
getStatusColor,getColorByString,
} from "./definedFunctions";

const props = defineProps({
   selectedScans: {
    type: Array as PropType<CombinedItem[]>,
    default: () => []
  },
  headers: {
    type: Array<any>,
    default: () => [
    ]
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
      sortBy: []
    })
  },
  loading: {
    type: Boolean,
    default: false
  },
});

const emit = defineEmits(["copyPath","update:selectedScans","update:scanParams"])
//格式化种子生存时间
const formatCreatedTime = (time: string)=>{
  if (time == "1970-01-01 08:00:00"){
return ""
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
// 已选择项变更
const selectedScansChange = (values:Array<CombinedItem>|null|undefined)=>{
    emit('update:selectedScans', values);
}

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
  emit('update:scanParams', {
    pageSize: props.scanParams.pageSize,
    page: props.scanParams.page, // 切换每页数量后跳转到第一页
    sort: items,
    changed:"sort"
  });
}

</script>