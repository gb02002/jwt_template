<template>
  <div id="app">
      <MainLayout>
        <router-view></router-view>
      </MainLayout>
  </div>
</template>

<script>
import MainLayout from "../src/layout/MainLayout.vue";

export default {
  name: 'App',
  components: {
    MainLayout
  }
}
</script>

<style>
/* Глобальные стили для всего приложения */
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f5f5f5; /* Добавлен фон для всего приложения */
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #07101a;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #547290;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>