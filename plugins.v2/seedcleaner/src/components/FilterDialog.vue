<template>
<div>
    <!-- 筛选对话框 -->
    <v-dialog v-model="props.dialogShow" max-width="600px">
      <v-card flat class="rounded border filter-card">
        <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
          <v-icon icon="mdi-filter-variant" class="mr-2" color="primary" size="small" />
          <span>条件筛选</span>
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            @click="closeDialog"
            variant="text"
            size="small"
            density="compact"
            icon="mdi-close"
          />
        </v-card-title>
        
        <v-card-text class="px-3 py-2">
          <!-- 路径筛选卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-folder-arrow-left" class="mr-2" color="primary" size="small" />
              <span>路径筛选</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-text-field
                label="文件路径"
                hint="输入要筛选的文件路径，支持模糊匹配"
                persistent-hint
                prepend-inner-icon="mdi-folder-search"
                variant="outlined"
                density="compact"
                clearable
                :model-value="props.filter.path"
                @update:model-value="filterChange('path', $event)"
                @keyup.enter="applyFilter"
                autofocus
              />
            </v-card-text>
          </v-card>

          <!-- 下载器筛选卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-download" class="mr-2" color="primary" size="small" />
              <span>下载器筛选</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    :items="allDownloaders.names"
                    :item-title="item=>item"
                    :item-value="item=>item"
                    label="下载器名称"
                    hint="选择特定的下载器名称"
                    persistent-hint
                    prepend-inner-icon="mdi-download-network"
                    variant="outlined"
                    density="compact"
                    clearable
                    :model-value="props.filter.client_name"
                    @update:model-value="filterChange('client_name', $event)"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    :items="allDownloaders.types"
                    :item-title="item=>item"
                    :item-value="item=>item"
                    label="下载器类型"
                    hint="选择下载器类型(qbittorrent/transmission)"
                    persistent-hint
                    prepend-inner-icon="mdi-download-circle"
                    variant="outlined"
                    density="compact"
                    clearable
                    :model-value="props.filter.client"
                    @update:model-value="filterChange('client', $event)"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- 数值范围筛选卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-chart-line" class="mr-2" color="primary" size="small" />
              <span>数值范围筛选</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-row>
                <v-col cols="12" md="6">
                  <div class="text-caption font-weight-medium mb-2">做种数范围</div>
                  <v-row no-gutters>
                    <v-col cols="5">
                      <v-number-input
                        :min="0"
                        :max="props.filter.seeds_limit_up || 999999"
                        variant="outlined"
                        density="compact"
                        hide-details
                        placeholder="最小值"
                        controls-position="compact"
                        control-variant="stacked"
                        clearable
                        class="custom-number-input"
                        :model-value="props.filter.seeds_limit_down"
                         @update:model-value="filterChange('seeds_limit_down', $event)"
                      />
                    </v-col>
                    <v-col cols="1" class="d-flex align-center justify-center text-caption">
                      ~
                    </v-col>
                    <v-col cols="6">
                      <v-number-input
                        :model-value="props.filter.seeds_limit_up"
                        @update:model-value="filterChange('seeds_limit_up', $event)"
                        :min="props.filter.seeds_limit_down || 0"
                        variant="outlined"
                        density="compact"
                        hide-details
                        placeholder="最大值"
                        controls-position="compact"
                        control-variant="stacked"
                        clearable
                        class="custom-number-input"
                      />
                    </v-col>
                  </v-row>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-caption font-weight-medium mb-2">文件大小范围 (MB)</div>
                  <v-row no-gutters>
                    <v-col cols="5">
                      <v-number-input
                        :model-value="props.filter.size_limit_down"
                        @update:model-value="filterChange('size_limit_down', $event)"
                        :min="0"
                        :max="props.filter.size_limit_up || 999999999"
                        variant="outlined"
                        density="compact"
                        hide-details
                        placeholder="最小值"
                        controls-position="compact"
                        control-variant="stacked"
                        clearable
                      />
                    </v-col>
                    <v-col cols="1" class="d-flex align-center justify-center text-caption">
                      ~
                    </v-col>
                    <v-col cols="6">
                      <v-number-input
                         :model-value="props.filter.size_limit_up"
                        @update:model-value="filterChange('size_limit_up', $event)"
                        :min="props.filter.size_limit_down || 0"
                        placeholder="最大值"
                        variant="outlined"
                        density="compact"
                        hide-details
                        controls-position="compact"
                        control-variant="stacked"
                        clearable
                      />
                    </v-col>
                  </v-row>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-caption font-weight-medium mb-2">做种存活时间范围 (天)</div>
                  <v-row no-gutters>
                    <v-col cols="12">
                      <v-number-input
                        v-model="props.filter.live_time"
                        :min="0"
                        variant="outlined"
                        density="compact"
                        hide-details
                        placeholder="输入天数"
                        controls-position="compact"
                        control-variant="stacked"
                        clearable
                        class="custom-number-input"
                      />
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card-text>
        
        <v-card-actions class="px-3 py-2 d-flex justify-end">
          <v-btn 
            @click="closeDialog"
            variant="outlined"
            size="small"
            class="mr-2"
          >
            取消
          </v-btn>
          <v-btn 
            color="primary"
            @click="applyFilter"
            variant="tonal"
            size="small"
          >
            应用筛选
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup> 
import {FilterModel} from './definedFunctions.ts';
import {ref, computed, reactive, watch} from 'vue';

const props = defineProps({
    dialogShow: {
      type: Boolean,
      default: false,
    },
    filter: {
      type: Object as () => FilterModel,
      default: () => ({
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
      }),
    },
    initialConfig: {
        type: Object,
        default: () => ({}),
  },
});

const emit = defineEmits(['update:dialogShow', 'applyFilter', 'filterChange']);
// 下载器名称、下载器类型列表
const allDownloaders = computed(() => {
  console.log("allDownloaders",props.initialConfig);
  let downloaderNames = new Set([
    ...props.initialConfig.downloaders.system.map(d => d.name),
    ...props.initialConfig.downloaders.custom.map(d => d.name)
  ])
  let downloaderTypes = new Set([
    ...props.initialConfig.downloaders.system.map(d => d.type),
    ...props.initialConfig.downloaders.custom.map(d => d.type)
  ])
  return {
    names: Array.from(downloaderNames),
    types: Array.from(downloaderTypes)
  };
});
//
const closeDialog = () => {
  emit('update:dialogShow',false);
};

//应用筛选
const applyFilter = () => {
  // console.log(state.filter);
    closeDialog()
    emit('applyFilter')
};
// 监听筛选条件变化
const filterChange = (_key:string,value:any) => {
    emit('filterChange',{[_key]:value})
};

</script>

<style lang="scss" scoped>
.filter-card{
  max-height: 38rem;
  overflow-y: auto;
}

</style>