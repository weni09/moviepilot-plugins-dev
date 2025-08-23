<template>
  <div class="plugin-config">
    <v-card flat class="rounded border">
      <!-- 标题区域 -->
      <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
        <v-icon icon="mdi-cog" class="mr-2" color="primary" size="small" />
        <span>种子清理工配置</span>
        <v-spacer></v-spacer>
        <div class="header-actions">
        <v-btn
          color="info"
          @click="emit('switch','page')"
          :disabled="state.saving"
          variant="text"
          size="small"
          density="compact"
          class="header-action-btn"
        >
          <template v-if="smAndDown">
            <v-icon icon="mdi-view-dashboard" size="18" />
          </template>
          <template v-else>
            <v-icon icon="mdi-view-dashboard" size="18" class="mr-1" />
            <span>详情页</span>
          </template>
        </v-btn>
        <v-btn
          color="success"
          :disabled="state.saving"
          @click="saveFullConfig"
          :loading="state.saving"
          variant="text"
          size="small"
          density="compact"
          class="header-action-btn"
        >
          <template v-if="smAndDown">
            <v-icon icon="mdi-content-save" size="18" />
          </template>
          <template v-else>
            <v-icon icon="mdi-content-save" size="18" class="mr-1" />
            <span>保存配置</span>
          </template>
        </v-btn>
        <v-btn
          color="grey"
          @click="emit('close')"
          :disabled="state.saving"
          variant="text"
          size="small"
          density="compact"
          class="header-action-btn"
        >
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
      
      <v-card-text class="px-3 py-2">
        <v-form ref="formRef" @submit.prevent="saveFullConfig">
          <!-- 系统下载器选择卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-download" class="mr-2" color="primary" size="small" />
              <span>选择系统下载器</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-select
                v-model="state.selectedSystemDownloaderNames"
                :items="state.systemDownloader.map(d => d.name)"
                label="系统下载器"
                variant="outlined"
                density="compact"
                hint="选择MoviePilot中已配置的下载器，可多选。"
                persistent-hint
                prepend-inner-icon="mdi-download-network"
                multiple
                chips
                clearable
                :disabled="state.saving"
                @update:model-value="handleSystemDownloadersChange"
              />
            </v-card-text>
          </v-card>

          <!-- 自定义下载器设置卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-plus-circle" class="mr-2" color="primary" size="small" />
              <span>自定义下载器</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="state.customDownloader.name"
                    label="名称"
                    variant="outlined"
                    density="compact"
                    hint="自定义下载器名称，不能与系统下载器名称重复。"
                    persistent-hint
                    @blur="validateName(state.customDownloader.name)"
                    :rules="[validateName]"
                    required
                    prepend-inner-icon="mdi-tag"
                    :disabled="state.saving"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="state.customDownloader.type"
                    :items="['qbittorrent', 'transmission']"
                    label="下载器类型"
                    variant="outlined"
                    density="compact"
                    hint="选择下载器类型，目前支持qbittorrent和transmission。"
                    persistent-hint
                    prepend-inner-icon="mdi-download"
                    :disabled="state.saving"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="state.customDownloader.host"
                    label="下载器地址"
                    hint="下载器地址，带http://或https://"
                    persistent-hint
                    variant="outlined"
                    density="compact"
                    prepend-inner-icon="mdi-web"
                    :disabled="state.saving"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="state.customDownloader.port"
                    label="端口"
                    type="number"
                    variant="outlined"
                    density="compact"
                    hint="下载器访问端口，默认443。"
                    persistent-hint
                    prepend-inner-icon="mdi-ethernet"
                    :disabled="state.saving"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="state.customDownloader.username"
                    label="用户名"
                    variant="outlined"
                    density="compact"
                    hint="下载器访问用户名。"
                    persistent-hint
                    prepend-inner-icon="mdi-account"
                    :disabled="state.saving"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="state.customDownloader.password"
                    label="密码"
                    variant="outlined"
                    density="compact"
                    :type="showPassword ? 'text' : 'password'"
                    hint="下载器访问密码。"
                    persistent-hint
                    prepend-inner-icon="mdi-lock"
                    :disabled="state.saving"
                  >
                    <template #append-inner>
                      <v-icon
                        :icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                        :size="16"
                        class="clickable-icon"
                        @click="showPassword = !showPassword"
                      />
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
              <v-card-actions class="px-0 pt-2 d-flex justify-end">
                <v-btn 
                  color="primary"
                  prepend-icon="mdi-plus-circle" 
                  @click="addCustomDownloader" 
                  variant="tonal"
                  size="small"
                  :disabled="state.saving"
                >
                  添加到下载器列表
                </v-btn>
              </v-card-actions>
            </v-card-text>
          </v-card>

          <!-- 下载器列表卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-format-list-bulleted" class="mr-2" color="primary" size="small" />
              <span>下载器列表</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <div class="downloader-list">
                <v-list lines="two" density="compact">
                  <v-list-item v-for="(item, index) in allDownloaders" :key="index" class="mb-1">
                    <template #prepend>
                      <v-icon 
                        :icon="getDownloaderIcon(item)" 
                        :style="{ color: getDownloaderColor(item) }"
                        size="small"
                      />
                    </template>
                    <v-list-item-title class="d-flex align-center">
                      <v-chip 
                        :color="item._type === 'system' ? 'primary' : 'info'"
                        size="x-small" 
                        text-color="white"
                        class="mr-2"
                      >
                        {{ item._type === 'system' ? '系统' : '自定义' }}
                      </v-chip>
                      <span class="text-subtitle-2">{{ item.name }}</span>
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-caption">
                      {{ item.host }}:{{ item.port }}
                    </v-list-item-subtitle>
                    <template #append>
                      <div class="d-flex align-center">
                        <v-btn
                          v-if="item._type === 'custom'"
                          color="info"
                          icon="mdi-pencil"
                          size="x-small"
                          variant="text"
                          @click="editCustom(item)"
                          :disabled="state.saving"
                        />
                        <v-btn
                          color="error"
                          icon="mdi-delete"
                          size="x-small"
                          variant="text"
                          @click="deleteDownloader(index, item._type)"
                          :disabled="state.saving"
                        />
                      </div>
                    </template>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>

          <!-- 路径设置卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-title class="text-caption d-flex align-center px-3 py-2 bg-primary-lighten-5">
              <v-icon icon="mdi-folder-cog" class="mr-2" color="primary" size="small" />
              <span>路径设置</span>
            </v-card-title>
            <v-card-text class="px-3 py-2">
              <v-text-field
                v-model="editableConfig.exclude_paths"
                label="排除的目录"
                hint="用于查找缺失种子的源文件，多个用';'隔开，一般为软/硬链接目标路径"
                persistent-hint
                prepend-inner-icon="mdi-cancel"
                variant="outlined"
                density="compact"
                :disabled="state.saving"
                class="mb-3"
              />
              <v-text-field
                v-model="editableConfig.extra_dir_paths"
                label="额外的目录"
                hint="用于查找缺失种子的源文件，多个用';'隔开，其不是现有下载器的保存目录"
                persistent-hint
                prepend-inner-icon="mdi-folder-open"
                variant="outlined"
                density="compact"
                :disabled="state.saving"
              />
            </v-card-text>
          </v-card>

          <!-- 帮助信息卡片 -->
          <v-card flat class="rounded mb-3 border config-card">
            <v-card-text class="d-flex align-center px-3 py-2">
              <v-icon icon="mdi-information" color="warning" class="mr-2" size="small"></v-icon>
              <span class="text-caption">
                如果在docker容器中，请确保下载器中的保存(下载/源文件)路径存在于MoviePilot容器中！
              </span>
            </v-card-text>
          </v-card>
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
    name: '自定义下载器1',
    type: 'qbittorrent',
    host: 'http://127.0.0.1',
    port: 443,
    username: 'admin',
    password: 'adminadmin'
  },
});

const formRef = ref();
// 响应式断点：小屏幕（含）仅显示图标
import { useDisplay } from 'vuetify';
const { smAndDown } = useDisplay();
const showPassword = ref(false);

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

// 列表图标映射（大小写不敏感）。
// 说明：某些 MDI 图标（如 mdi-qbittorrent）在不同版本包里可能不存在，为保证兼容，统一映射到常见可用图标。
function getDownloaderIcon(item: any) {
  const type = (item?.type || '').toString().toLowerCase();
  if (type.includes('qbittorrent') || type === 'qbittorrent' || type === 'qbit') {
    // 使用通用的下载图标，避免因缺少特定品牌图标导致的空 svg/path
    return 'mdi-download';
  }
  if (type.includes('transmission') || type === 'transmission') {
    return 'mdi-download-network';
  }
  // 系统下载器但无类型时也给到一个稳定图标
  if (item?._type === 'system' && !type) {
    return 'mdi-download-network';
  }
  return 'mdi-download';
}

// 图标颜色映射：Qbittorrent -> 蓝色，Transmission -> 红色，其余沿用原有逻辑（系统紫色、其它信息蓝）
function getDownloaderColor(item: any) {
  const type = (item?.type || '').toString().toLowerCase();
  if (type.includes('qbittorrent') || type === 'qbittorrent' || type === 'qbit') {
    return '#64B5F6'; // blue-300 浅蓝
  }
  if (type.includes('transmission') || type === 'transmission') {
    return '#E57373'; // red-300 浅红
  }
  // 保底：系统下载器用主题primary，其它用info（使用接近主题的hex以避免主题变量解析为灰色）
  return item?._type === 'system' ? '#1976D2' : '#0288D1';
}

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
  const host = String(newDl.host).trim();
  if (!(host.startsWith('http://') || host.startsWith('https://'))){
    alert('请填写正确的下载器地址: http:// 或 https:// 开头');
    return;
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
  max-width: 80rem;
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

.downloader-list {
  max-height: 20rem;
  overflow-y: auto;
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

.text-subtitle-2 {
  font-size: 14px !important;
  font-weight: 500;
  margin-bottom: 2px;
}

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

.clickable-icon {
  cursor: pointer;
}
</style>
