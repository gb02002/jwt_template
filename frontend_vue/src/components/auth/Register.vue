<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <label for="username">Username:</label>
      <input type="text" v-model="username" required>
      <label for="password">Password:</label>
      <input type="password" v-model="password" required>
      <button type="submit">Register</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import {computed, ref} from 'vue';
import { useStore } from "vuex";


export default {
  name: 'Registration',
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const errorMessage = ref('');
    const store = useStore();

    const register = async () => {
      try {
        await store.dispatch('register', { username: username.value, password: password.value });
        await router.push('/login');
      } catch (error) {
        errorMessage.value = 'Registration failed: ' + (error.response?.data?.detail || 'Unknown error');
      }
    };

    return {
      username,
      password,
      register,
      errorMessage,
      isAuthenticated: computed(() => store.getters.isAuthenticated)
    };
  }
};
</script>

<style scoped>
.register-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
}
label, input {
  margin-bottom: 10px;
  margin-right: auto;
  margin-left: auto;
  border: #e1086e;
  border-radius: 5px;
}
button {
  margin-top: 10px;
  width: 200px;
  align-self: center;
  background-color: #02390b;
  color: #42b983;
}
</style>
