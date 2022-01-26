module.exports = {
  outputDir: '../project/static/frontend',

  devServer: {
    proxy: {
      '/api*': {
        target: 'http://localhost:5000/'
      }
    }
  },

  pluginOptions: {
    i18n: {
      locale: 'de',
      fallbackLocale: 'de',
      localeDir: 'locales',
      enableInSFC: true,
      enableBridge: false
    }
  }
}
