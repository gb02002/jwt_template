<template>
  <div v-if="showRegisterModal" class="modal">
    <div class="modal-content">
      <span @click="closeRegisterModal" class="close">&times;</span>
      <Register @close="closeRegisterModal" />
    </div>
  </div>
</template>

<script>
import Register from "../auth/Register.vue";

export default {
  name: 'RegisterModal',
  components: {
    Register
  },
  props: {
    showRegisterModal: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    closeRegisterModal() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
