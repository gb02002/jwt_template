<template>
  <transition name="submenu">
    <ul v-if="isAuthenticated" class="submenu">
      <li @click="editProfile">Edit Profile</li>
    </ul>
    <ul v-else class="submenu">
      <li @click="openLoginModal">Login</li>
      <li @click="openRegisterModal">Register</li>
    </ul>
  </transition>
</template>

<script>
export default {
  name: 'SubMenu',
  props: {
    isAuthenticated: { type: Boolean, required: true }
  },
  emits: ['openLoginModal', 'openRegisterModal', 'editProfile'],
  methods: {
    openLoginModal() {
      this.$emit('openLoginModal');
    },
    openRegisterModal() {
      this.$emit('openRegisterModal');
    },
    editProfile() {
      this.$emit('editProfile');
    }
  }
};
</script>

<style scoped>
.submenu {
  padding-left: 1rem;
}
</style>
