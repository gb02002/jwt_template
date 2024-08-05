<template>
  И тут что-то есть

  <transition>Еще какой-то блок</transition>

  <transition name="menu">
    <div class="menu" ref="menu" @click.stop>
      У нас тут что-то есть
      <button @click="toggleMenu" class="close-button">X</button>
      <ul>
        <li @click="toggleSubMenu('auth')">
          <span v-if="isAuthenticated">Account</span>
          <span v-else>Login/Register</span>
        </li>
        <SubMenu
          v-if="showSubMenu === 'auth'"
          :isAuthenticated="isAuthenticated"
          @openLoginModal="openLoginModal"
          @openRegisterModal="openRegisterModal"
          @editProfile="editProfile"
        />
        <li @click="viewOrders">Orders</li>
        <li @click="viewAbout">About</li>
        <li @click="viewSettings">Settings</li>
      </ul>
    </div>
  </transition>
</template>

<script>
import SubMenu from './SubMenu.vue';

export default {
  name: 'Menu',
  components: { SubMenu },
  props: {
    isAuthenticated: { type: Boolean, default: false }
  },
  data() {
    return { showSubMenu: null };
  },
  emits: [
    'toggleMenu',
    'openLoginModal',
    'openRegisterModal',
    'editProfile',
    'viewOrders',
    'viewAbout',
    'viewSettings'
  ],
  methods: {
    toggleMenu() {
      console.log('toggleMenu in Menu');
      this.$emit('toggleMenu');
    },
    toggleSubMenu(menuItem) {
      this.showSubMenu = this.showSubMenu === menuItem ? null : menuItem;
    },
    openLoginModal() {
      this.$emit('openLoginModal');
      this.toggleMenu();
    },
    openRegisterModal() {
      this.$emit('openRegisterModal');
      this.toggleMenu();
    },
    editProfile() {
      this.$emit('editProfile');
      this.toggleMenu();
    },
    viewOrders() {
      this.$emit('viewOrders');
      this.toggleMenu();
    },
    viewAbout() {
      this.$emit('viewAbout');
      this.toggleMenu();
    },
    viewSettings() {
      this.$emit('viewSettings');
      this.toggleMenu();
    },
    handleClickOutside(event) {
      if (this.$refs.menu && !this.$refs.menu.contains(event.target)) {
        this.toggleMenu();
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  }
};
</script>

<style scoped>
.close-button {
  position: absolute;
  top: 10rem;
  right: 10rem;
  background-color: #ff0000;
  color: #000000;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.menu {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 250px; /* Width of the menu */
  background-color: #ffffff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  border-radius: 0 4px 4px 0;
  padding: 1rem;
  z-index: 1000; /* Ensure the menu is above other content */
  transform: translateX(-100%);
  transition: transform 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.menu-enter-active, .menu-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.menu-enter, .menu-leave-to {
  transform: translateX(0);
  opacity: 1;
}

.menu-leave {
  transform: translateX(-100%);
  opacity: 0;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu li:hover {
  background-color: #f0f0f0;
}
</style>
