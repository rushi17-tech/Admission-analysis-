<script setup lang="ts">
import { SidebarProvider, SidebarTrigger } from "../components/ui/sidebar";

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
