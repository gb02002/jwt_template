<template>
  <div>
    <h1>Profile</h1>
    <p>This is your profile page.</p>
    <div v-if="profile">
      <p><strong>Username:</strong> {{ profile.username }}</p>
      <p><strong>First Name:</strong> {{ profile.first_name }}</p>
      <p><strong>Last Name:</strong> {{ profile.last_name }}</p>
      <p><strong>Verified:</strong> {{ profile.is_verified ? 'Yes' : 'No' }}</p>
      <p><strong>Superuser:</strong> {{ profile.is_superuser ? 'Yes' : 'No' }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <div v-if="errorMessage">
      <p style="color: red;">{{ errorMessage }}</p>
    </div>
  </div>
</template>


<script>
import {onMounted, ref} from "vue";
import $api from "@/http";

export default {
  name: 'ProfileView',
  setup() {
    const errorMessage = ref('');
    const profile = ref(null);

    const fetchProfile = async () => {
      try {
        profile.value = await $api.get("/us/profile");
      } catch (error) {
        errorMessage.value = 'Profile not found: ' + (error.response?.data?.detail || 'Unknown error');
      }
    }

    onMounted(fetchProfile);

    return {
      profile,
      errorMessage,
    };
  }
};
</script>