<template>
<div class="mb-5 mx-auto">
  <h1 class="mb-5 mt-5 text-center">Сервис сокращения ссылок</h1>
  <ShortenLinkForm/>
</div>  
</template>

<script>
import ShortenLinkForm from './components/ShortenLinkForm.vue'

export default {
  name: 'App',
  components: {
    ShortenLinkForm
  }
}
</script>

<style>
body{
  color: #fff!important;
  background-color: #343a40!important;
}
</style>
