<template>
    <div class="layout">
        <header>
            <Header />
        </header>

        <main>
            <router-view></router-view>
        </main>
        
        <footer>
            <p>&copy; 2024 Hello</p>
        </footer>
    </div>
</template>

<script>
import Header from '../components/Header.vue';


export default {
    name: 'MainLayout',
    components: {
      Header,
    }
};
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
    
header {
  background-color: #03212bc7;
  color: #93e2ccd7;     
  padding: 0.8rem;
}

main {
  flex: 1;
  padding: 2rem;
  background-color: #e1e1e1;
}

footer {
  background-color: #03212bc7;
  color: #93e2ccd7;
  text-align: center;
  padding: 0.8rem;
}
</style>