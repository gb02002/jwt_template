<template>
  <div>
    <!-- Компонент кнопки меню -->
    <MenuButton v-if="!showMenu" @toggleMenu="showMenu = true" />

    <!-- Компонент меню -->
    <Menu v-if="showMenu" @toggleMenu="showMenu = false" @openLoginModal="showLoginModal = false" @openRegisterModal="showRegisterModal = true" />

    <!-- Модальные окна -->
    <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
    <RegisterModal v-if="showRegisterModal" @close="showRegisterModal = false" />
  </div>
</template>

<script>
import MenuButton from '../components/menu/MenuButton.vue';
import Menu from '../components/menu/Menu.vue';
import LoginModal from '../components/menu/LoginModal.vue';
import RegisterModal from '../components/menu/RegisterModal.vue';

export default {
  name: 'MainMenu',
  components: {
    MenuButton,
    Menu,
    LoginModal,
    RegisterModal
  },
  data() {
    return {
      showMenu: false,
      showLoginModal: false,
      showRegisterModal: false
    };
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
};
</script>

<style scoped>
/* Вы можете разместить стили здесь */
</style>
