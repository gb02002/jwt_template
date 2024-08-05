<template>
  <div class="login-container">
    <h2>log-out</h2>
    <form @submit.prevent="logout" class="log-out">
      <button type="submit">Log-out</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from "vuex";


export default {
  name: 'Logout',
  setup() {
    const errorMessage = ref('');
    const router = useRouter();
    const store = useStore();

    const logout = async () => {
      try {
        await store.dispatch('logout');
        await router.push('/');
      } catch (error) {
        errorMessage.value = 'Logout failed: ' + (error.response?.data?.detail || 'Unknown error');
      }
    };

return {
  logout,
  errorMessage
  };
}
};
</script>
