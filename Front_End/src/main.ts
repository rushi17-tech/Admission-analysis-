import { createApp } from 'vue'
import App from './App.vue'

import router from './router/router'
import { Icon } from "@iconify/vue";
import './assets/main.css'



const app = createApp(App)

app.use(router)

app.mount('#app')

