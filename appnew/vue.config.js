const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer:{
    //proxy: 'http://192.168.3.2:3000/'
    proxy: 'https://link-shortener-production-0bf0.up.railway.app:3000/'
  },
  //added to deploy
  publicPath: '/static/app',
})
