<template>
  <header>
    <button @click="toggleMenu">Menu</button>
    <div v-if="isMenuOpen" class="menu">
      <button @click="navigateTo(isAuthenticated ? '/profile' : '/register')">
        {{ isAuthenticated ? 'Profile' : 'Register' }}
      </button>
      <button v-if="isAuthenticated" @click="logout">Logout</button>
      <button v-else @click="navigateTo('/login')">Login</button>
      <button @click="navigateTo('/orders')">Orders</button>
      <button @click="navigateTo('/about')">About</button>
      <button @click="navigateTo('/settings')">Settings</button>
    </div>
  </header>
</template>

<script>
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'Header',
  setup() {
    const store = useStore();
    const router = useRouter();
    const isMenuOpen = ref(false);
    const isAuthenticated = computed(() => store.getters.isAuthenticated);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    const navigateTo = (path) => {
      router.push(path);
      isMenuOpen.value = false;
    };

    const logout = () => {
      store.dispatch('logout');
      navigateTo('/');
    };

    return {
      isMenuOpen,
      isAuthenticated,
      toggleMenu,
      navigateTo,
      logout,
    };
  },
};
</script>

<style scoped>
header {
  position: relative;
}
.menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  flex-direction: column;
}
button {
  margin: 5px 0;
}
</style>
