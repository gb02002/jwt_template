<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <label for="username">Username:</label>
      <input type="text" v-model="username" required>
      <label for="password">Password:</label>
      <input type="password" v-model="password" required>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
    <p v-if="isAuthenticated">User is authenticated</p>
  </div>
</template>

<script>
import {computed, ref} from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const errorMessage = ref('');
    const store = useStore();

    const login = async () => {
      try {
        await store.dispatch('login', { username: username.value, password: password.value });
        await router.push('/');
      } catch (error) {
        errorMessage.value = 'Login failed: ' + (error.response?.data?.detail || 'Unknown error');
      }
    };

    return {
      username,
      password,
      login,
      errorMessage,
      isAuthenticated: computed(() => store.getters.isAuthenticated)
    };
  }
};
</script>

<style scoped>

.login-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-form label {
  margin-bottom: 5px;
}

.login-form input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.login-form button {
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.login-form button:hover {
  background-color: #0056b3;
}
</style>
