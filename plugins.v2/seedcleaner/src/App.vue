
<template>
  <div class="app-container">
    <v-app>
      <v-app-bar color="primary" app>
        <v-app-bar-title>插件 - 本地测试</v-app-bar-title>
      </v-app-bar>

      <v-main style="margin-top: 56px;">
        <v-container>
          <v-tabs v-model="state.activeTab" bg-color="primary" grow>
            <v-tab value="page">运行状态</v-tab>
            <v-tab value="config">插件配置</v-tab>
            <v-tab value="dashboard">仪表盘组件</v-tab>
          </v-tabs>

          <v-window v-model="state.activeTab" class="mt-4">
            <v-window-item value="page">
              <h2 class="text-h5 mb-4">运行状态与操作 (Page.vue)</h2>
              <div class="component-preview">
                <page-component
                  :api="requestWrapper"
                  @switch="switch_tab"
                  @close="handleClose('Page')"
                  :initial-config="state.initConfig"
                ></page-component>
              </div>
            </v-window-item>

            <v-window-item value="config">
              <h2 class="text-h5 mb-4">插件配置 (Config.vue)</h2>
              <div class="component-preview">
                <config-component
                  :api="requestWrapper"
                  :initial-config="state.initConfig"
                  @close="handleClose('Config')"
                  @switch="switch_tab"
                ></config-component>
              </div>
            </v-window-item>
             <v-window-item value="dashboard">
              <h2 class="text-h5 mb-4">仪表盘组件 (Dashboard.vue)</h2>
              <div class="component-preview">
                <dashboard-component
                  :api="requestWrapper"
                  @close="handleClose('Config')"
                  @switch="switch_tab"
                ></dashboard-component>
              </div>
            </v-window-item>
          </v-window>
        </v-container>
      </v-main>

      <!-- <v-footer app color="primary" class="text-center d-flex justify-center">
        <span class="text-white">MoviePilot 种子清理工插件本地测试 ©{{ new Date().getFullYear() }}</span>
      </v-footer> -->
    </v-app>

    <v-snackbar v-model="state.snackbar.show" :color="state.snackbar.color" :timeout="state.snackbar.timeout" location="top end">
      {{ state.snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" @click="state.snackbar.show = false"> 关闭 </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import PageComponent from './components/Page.vue'
import ConfigComponent from './components/Config.vue'
import DashboardComponent from './components/Dashboard.vue'
import { PLUGIN_ID } from './components/definedFunctions'
import {request,loginAndGetToken} from './utils/request';
import session from './utils/session';

// 挂载到 api 属性上，供子组件调用
const requestWrapper = {
    get: (url, config?) => request.get(url, config),
    post: (url, data?, config?) => request.post(url, data, config),
    put: (url, data?, config?) => request.put(url, data, config),
    delete: (url, config?) => request.delete(url, config),
    patch: (url, data?, config?) => request.patch(url, data, config)
}

const state = reactive({
  activeTab: "page",
  snackbar: {
    show: false,
    text: '',
    color: 'success',
    timeout: 3000,
  },
  initConfig:{

  }
});

const switch_tab = (name) => {
  state.activeTab = name;
};


const showNotification = (text, color = 'success')=> {
  state.snackbar.text = text;
  state.snackbar.color = color;
  state.snackbar.show = true;
}

const getConfig = ()=>{
  let url = `/plugin/${PLUGIN_ID}/config`;
  requestWrapper.get(url).then(res=>{
    console.log('获取配置:', res);
    state.initConfig = res;
  })
}

const handleClose = (componentName) => {
  showNotification(`${componentName} 已关闭 (模拟)`, 'info');
}



onMounted(async () => {
  try {
    const token = session.token
    if (!token) {
      // 1. 获取 token
    const token = await loginAndGetToken();
    }
    // 3. 获取配置
    getConfig();
  } catch (error) {
    console.error('初始化失败:', error);
  }
});

</script>

<style lang="scss" scoped>

.app-container {
}

.component-preview {
  // overflow: hidden;
  backface-visibility: hidden;
  overflow-y: auto;
  font-size: inherit;
  letter-spacing: .0094rem;
  line-height: inherit;
  .plugin-common{
    max-width: 80rem;
  }
}

.v-tab {
  text-transform: none !important;
}
</style>
