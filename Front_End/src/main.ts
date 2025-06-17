import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router"; 
import './assets/main.css'  // adjust path if neede
// main.ts or App.vue


createApp(App).use(router).mount("#app");
