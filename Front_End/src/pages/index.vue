<script setup lang="ts">
import { SidebarProvider, SidebarTrigger } from "../components/ui/sidebar";
import AppSidebar from "../components/appsidebar.vue";
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <main>
      <SidebarTrigger />
      <slot />
    </main>
  </SidebarProvider>
</template>
