<template>
  <button @click="toggleMenu" class="menu-button">Menu</button>
</template>

<script>
export default {
  name: 'MenuButton',
  methods: {
    toggleMenu() {
      console.log('toggleMenu');
      this.$emit('toggleMenu');
    }
  }
};
</script>

<style scoped>
.menu-button {
  position: fixed;
  top: 1rem;
  left: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  z-index: 1001; /* Ensure the button is above other content */
}
</style>
