module.exports = {
  outputDir: "../project/static/frontend",

  devServer: {
    proxy: "http://localhost:5000/",
  },

  configureWebpack: {
    devtool: "source-map",
  },

  pluginOptions: {
    i18n: {
      locale: "de",
      fallbackLocale: "de",
      localeDir: "locales",
      enableInSFC: true,
      enableBridge: false,
    },
  },
};
