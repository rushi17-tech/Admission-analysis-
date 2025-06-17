<script setup lang="ts">
import LoginPage from './pages/login.vue'
import signuppage from './pages/signup.vue'

import { ref } from 'vue'

import AppSidebar from './components/appsidebar.vue'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'

</script>



<template>
  <!-- <SidebarProvider>
    <AppSidebar /> -->
    <main>
      <!-- <SidebarTrigger /> -->
      <RouterView />
    </main>
  <!-- </SidebarProvider> -->
</template>
 


<style scoped>
.app-container {
  font-family: 'Segoe UI', sans-serif;
  text-align: center;
  background-color: #f9f9f9;
  min-height: 100vh;
}

.app-header {
  background-color: #343a40;
  color: white;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.app-header h1 {
  font-size: 1.5rem;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 0.75rem;
}

.nav-button {
  background-color: #495057;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
  font-size: 0.95rem;
}

.nav-button:hover {
  background-color: #ffc107;
  color: #343a40;
}

.app-content {
  padding: 2rem;
}
</style>

