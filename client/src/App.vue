<template>
  <div>
    <header-component />
    <router-view />
    <footer-component />
  </div>
</template>

<script setup>
import HeaderComponent from './components/HeaderComponent.vue';
import FooterComponent from './components/FooterComponent.vue';
</script>