<template>
  <div class="plugin-common plugin-config">
    <v-card flat class="rounded border">
      <!-- 标题 -->
      <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
        <v-icon icon="mdi-cog" class="mr-2" color="primary" size="small"/>
        <span>种子清理工</span>
        <v-card-subtitle class="ml-2">配置页</v-card-subtitle>
        <v-spacer />
         <v-btn color="info" 
         @click="emit('switch','page')" 
         icon="mdi-view-dashboard" 
         :disabled="state.saving" 
         variant="tonal" 
         size="small"
         class="mr-4"
         >
          <v-icon icon="mdi-view-dashboard" size="small"></v-icon>
          <v-tooltip activator="parent" location="top">详情页</v-tooltip>
        </v-btn>
        <v-btn color="success" :disabled="state.saving" @click="saveFullConfig" :loading="state.saving" icon="mdi-content-save" variant="tonal" size="small"  class="mr-4">
          <v-icon icon="mdi-content-save" size="small"/>
          <v-tooltip activator="parent" location="top">保存配置</v-tooltip>
        </v-btn>
        <v-btn color="primary" @click="emit('close')" icon="mdi-close" :disabled="state.saving"  variant="tonal" size="small"  class="mr-4">
          <v-icon icon="mdi-close" size="small" />
          <v-tooltip activator="parent" location="top">关闭</v-tooltip>
        </v-btn>
      </v-card-title>

      <v-card-text class="px-3 py-2">
        <v-form ref="formRef" @submit.prevent="saveFullConfig">
          <v-row no-gutters>
            <!-- 左边配置 -->
            <v-col cols="6" class="pr-4">
              <v-card flat class="rounded border config-card mb-4">
                <v-card-text class="px-3 py-2">
                   <!-- 系统下载器改为下拉框 -->
                 <v-select
                    v-model="state.selectedSystemDownloaderNames"
                    :items="state.systemDownloader.map(d => d.name)"
                    label="系统下载器"
                    variant="outlined"
                    density="compact"
                    class="mb-3 text-caption"
                    hint="MoviePilot系统配置中的下载器,可多选"
                    multiple
                    chips
                    clearable
                    @update:model-value="handleSystemDownloadersChange"
                  />
                </v-card-text>
              </v-card>

                  <!-- 自定义下载器 -->
                  <v-card flat class="mt-4 rounded border config-card">
                    <v-card-title class="text-caption px-3 py-2 bg-primary-lighten-5">
                      自定义下载器
                    </v-card-title>
                    <v-card-text class="px-3 py-2">
                      <v-text-field
                        v-model="state.customDownloader.name"
                        label="名称"
                        variant="outlined"
                        density="compact"
                        @blur="validateName(state.customDownloader.name)"
                        :rules="[validateName]"
                        required
                        class="mb-2 text-caption"
                      />
                      <v-select
                        v-model="state.customDownloader.type"
                        :items="['qbittorrent', 'transmission']"
                        label="类型"
                        variant="outlined"
                        density="compact"
                        class="mb-2 text-caption"
                      />
                      <v-text-field
                        v-model="state.customDownloader.host"
                        label="下载器地址 (带http://或https://)"
                        variant="outlined"
                        density="compact"
                        class="mb-2 text-caption"
                      />
                      <v-text-field
                        v-model.number="state.customDownloader.port"
                        label="端口"
                        type="number"
                        variant="outlined"
                        density="compact"
                        class="mb-2 text-caption"
                      />
                      <v-text-field
                        v-model="state.customDownloader.username"
                        label="用户名"
                        variant="outlined"
                        density="compact"
                        class="mb-2 text-caption"
                      />
                      <v-text-field
                        v-model="state.customDownloader.password"
                        label="密码"
                        variant="outlined"
                        density="compact"
                        type="password"
                        class="mb-2 text-caption"
                      />
                    </v-card-text>
                    <v-card-actions class="px-3 pb-2 d-flex justify-end">
                      <v-btn color="primary"
                       prepend-icon="mdi-plus-circle" 
                       @click="addCustomDownloader" 
                       variant="plain">添加到下载器列表</v-btn>
                    </v-card-actions>
                  </v-card>
            </v-col>

            <!-- 右边下载器列表 -->
            <v-col cols="6">
              <v-card flat class="rounded border config-card downloader-list">
                <v-card-title class="text-caption px-3 py-2 bg-primary-lighten-5">
                  下载器列表
                </v-card-title>
                <v-card-text class="px-3 py-2">
                  <v-list dense lines="one">
                    <v-list-item v-for="(item, index) in allDownloaders" :key="index">
                      <v-list-item-title>
                         <v-chip :color="item._type=='system'?'primary':'info'"
                      size="small" text-color="white">{{item._type=='system'?'系统':'自定义'}}</v-chip>
                        {{ item.name }} ({{ item.type }})</v-list-item-title>
                      <v-list-item-subtitle>{{ item.host }}:{{ item.port }}</v-list-item-subtitle>
                      <template #append>
                        <v-btn
                          v-if="item._type === 'custom'"
                          color="info"
                          icon="mdi-pencil"
                          size="x-small"
                          @click="editCustom(item)"
                        ></v-btn>
                        <v-btn
                          class="ml-2"
                          icon="mdi-delete"
                          size="x-small"
                          @click="deleteDownloader(index, item._type)"
                        ></v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>

              <!-- 新增路径设置卡片 -->
                <v-card flat class="rounded border config-card mt-2">
                  <v-card-title class="text-caption px-3 py-2 bg-primary-lighten-5">
                    路径设置
                  </v-card-title>
                  <v-card-text class="px-3 py-2">
                    <!-- 排除目录 -->
                    <v-text-field
                      v-model="editableConfig.exclude_paths"
                      label="排除的目录"
                      hint="用于查找缺失种子的源文件,多个用';'隔开,一般为软/硬链接目标路径"
                      persistent-hint
                      prepend-inner-icon="mdi-cancel"
                      variant="outlined"
                      density="compact"
                      class="mb-3 text-caption"
                    />
                    <!-- 额外目录 -->
                    <v-text-field
                      v-model="editableConfig.extra_dir_paths"
                      label="额外的目录"
                      hint="用于查找缺失种子的源文件,多个用';'隔开,其不是现有下载器的保存目录"
                      persistent-hint
                      prepend-inner-icon="mdi-folder-open"
                      variant="outlined"
                      density="compact"
                      class="text-caption"
                    />
                  </v-card-text>
                   <v-card-text class="d-flex align-center px-3 py-1">
                    <v-icon icon="mdi-information" color="error" class="mr-2" size="small"></v-icon>
                    <span class="text-caption">
                      如果在docker容器中，请确保下载器中的保存(下载/源文件)路径存在于MoviePilot容器中！
                    </span>
                  </v-card-text>
                </v-card>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- 提示框 -->
    <v-snackbar v-model="state.snackbar.show" :timeout="3000" :color="state.snackbar.color" :location="state.snackbar.location">
      {{ state.snackbar.message }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { PLUGIN_ID, SnackbarModel, ApiRequest,DownloaderInfoModel } from './definedFunctions.ts';

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

const emit = defineEmits(['close', 'switch']);

interface StateModel {
  saving: boolean;
  snackbar: SnackbarModel;
  systemDownloader: DownloaderInfoModel[];
  selectedSystemDownloaderNames:string[]
  customDownloader:  DownloaderInfoModel,
}

const state = reactive<StateModel>({
  saving: false,
  snackbar: {
    location: 'top',
    show: false,
    message: '',
    color: 'success'
  },
  systemDownloader: [],
  selectedSystemDownloaderNames: [],
  customDownloader: {
    name: '',
    type: 'qbittorrent',
    host: '',
    port: 443,
    username: '',
    password: ''
  },
});

const formRef = ref();

// 数据模型
const editableConfig = reactive({
  enable: true,
  exclude_paths: "",
  extra_dir_paths: "",
  downloaders: {
    system: [] as any[],
    custom: [] as any[]
  }
});

// 合并系统+自定义下载器
const allDownloaders = computed(() => {
  return [
    ...editableConfig.downloaders.system.map(d => ({ ...d, _type: 'system' })),
    ...editableConfig.downloaders.custom.map(d => ({ ...d, _type: 'custom' }))
  ];
});

// 名称验证（不能重复）
function validateName(value: string) {
  value = value.trim();
  const existsSystem = state.systemDownloader.some(
    d => d.name === value
  );
  // console.log("existsSystem",existsSystem)
  if (existsSystem)
    return '名称已存在于系统下载器中，请重新输入'
  const exists = editableConfig.downloaders.custom.some(
    d => d.name === value
  );
  // console.log("exists",exists)
  return exists ? '名称已存在于自定义下载器中，请重新输入' : true;
}

const showNotification = (text, color = 'success')=> {
  state.snackbar.message = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}
// 监听系统下载器选择变化
function handleSystemDownloadersChange(selectedNames: string[]) {
  // console.log('selectedNames', selectedNames)
  // 获取当前所有系统下载器
  const systemDownloaders = state.systemDownloader;
  // 找出需要添加的项
  const added = systemDownloaders.filter(d => selectedNames.includes(d.name) && !allDownloaders.value.some(dl => dl.name === d.name && dl._type === 'system'));
  // console.log('added', added)
  // 找出需要删除的项
  const removedNames = allDownloaders.value
    .filter(dl => dl._type === 'system')
    .map(dl => dl.name)
    .filter(name => !selectedNames.includes(name));
  // 添加新的系统下载器到列表
  added.forEach(dl => {
    editableConfig.downloaders.system.push(dl);
  });
  // 删除取消选择的系统下载器
  editableConfig.downloaders.system = editableConfig.downloaders.system.filter(dl => !removedNames.includes(dl.name));
}

// 添加自定义下载器
function addCustomDownloader() {
  const newDl = { ...state.customDownloader };
  if (!newDl.name || !newDl.host || !newDl.port) {
    alert('请填写所有必填字段');
    return;
  }
  if (!newDl.host.startsWith("http://") && !newDl.host.startsWith("https://)")){
    alert('请填写正确的下载器地址: http:// 或 https:// 开头');
    return
  }
  const exists = editableConfig.downloaders.custom.some(d => d.name === newDl.name);
  if (exists) {
    alert('名称已存在');
    return;
  }
  // 去除每个字段的前后空格
  Object.keys(newDl).forEach(key => {
    if (typeof newDl[key] === 'string') {
      newDl[key] = newDl[key].trim();
    }
  });
  editableConfig.downloaders.custom.push(newDl);
  // 清空表单
  state.customDownloader = {
    name: '',
    type: 'qbittorrent',
    host: '',
    port: 443,
    username: '',
    password: ''
  };
}

// 查询系统下载器配置
const getSystemDownloaders = () => {
  props.api.get(`plugin/${PLUGIN_ID}/downloader?config_type=system`).then((res) => {
    // console.log('获取系统下载器配置:', res.system);
    state.systemDownloader = res.system;
  });
};

// 编辑自定义下载器
function editCustom(downloader: any) {
  state.customDownloader = { ...downloader };
  deleteDownloader(editableConfig.downloaders.custom.findIndex(d => d.name === downloader.name), 'custom');
}

// 删除下载器
function deleteDownloader(index: number, type: string) {
  if (type === 'system') {
    let deleteItem = editableConfig.downloaders.system[index];
    state.selectedSystemDownloaderNames = state.selectedSystemDownloaderNames.filter(name => name !== deleteItem.name);
    editableConfig.downloaders.system.splice(index, 1);
  } else {
    console.log('删除自定义下载器:',index, type);
    let _index = index - editableConfig.downloaders.system.length;
    editableConfig.downloaders.custom.splice(_index, 1);
  }
}

// 保存配置
const saveFullConfig = async () => {
  // console.log('保存配置...');
  state.saving = true;
  try {
    const res = await props.api.post(`plugin/${PLUGIN_ID}/config`, {
      enable: editableConfig.enable,
      exclude_paths: editableConfig.exclude_paths,
      extra_dir_paths: editableConfig.extra_dir_paths,
      downloaders: editableConfig.downloaders
    });
    if (res["code"]!="ok"){
      showNotification(res["message"] || "保存失败","error")
    }
    // console.log('保存配置API响应:', res);
    showNotification("保存配置成功","success")
  } catch (err) {
    showNotification(err.message || '保存配置失败，请检查网络或查看日志',"error")
  } finally {
    state.saving = false;
  }
};

watch(()=>props.initialConfig,
(newConfig) => {
  if (newConfig && Object.keys(newConfig).length > 0) {
    // console.log('监听初始配置:', newConfig);
    Object.keys(editableConfig).forEach(key => {
      if (newConfig.hasOwnProperty(key)) {
        editableConfig[key] = JSON.parse(JSON.stringify(newConfig[key]));
      }
    });
     editableConfig.downloaders.system.forEach(d => {
        state.selectedSystemDownloaderNames.push(d.name);
    });
  } 
},
{ deep: true ,immediate: true }
)

onMounted(() => {
  getSystemDownloaders()
});
</script>

<style scoped>
.plugin-config {
  margin: 0 auto;
  padding: 0.5rem;
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.07);
}

.border {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}

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
.downloader-list{
  max-height: 17rem;
  overflow-y: scroll;
}
.setting-item {
  border-radius: 8px;
  transition: all 0.2s ease;
  padding: 0.5rem;
  margin-bottom: 4px;
}

.setting-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.03);
}

.small-switch {
  transform: scale(0.8);
  margin-right: -8px;
}

.text-subtitle-1 {
  font-size: 1.1rem !important;
  font-weight: 500;
  margin-bottom: 2px;
}
</style>
