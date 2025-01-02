<template>
  <div class="app">
    <template v-if="!isStandalonePage">
      <TheHeader />
    </template>

    <div class="main-content">
      <template v-if="!isStandalonePage">
        <TheSidebar />
      </template>

      <div class="content">
        <router-view></router-view>
      </div>
    </div>

    <template v-if="!isStandalonePage">
      <TheFooter />
    </template>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TheHeader from './components/Layout/TheHeader.vue'
// import TheFooter from './components/Layout/TheFooter.vue'
// import TheSidebar from './components/Layout/TheSidebar.vue'

const route = useRoute()
const isStandalonePage = computed(() => ['/login', '/register'].includes(route.path))
</script>

<style>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
  /* background-color: aqua; */
}

.content {
  flex: 1;
  padding: 0px;
  /* background-color: aqua; */

}
</style>