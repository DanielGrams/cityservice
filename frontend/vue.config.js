const path = require("path");

module.exports = {
  outputDir: "../project/static/frontend",

  devServer: {
    proxy: "http://localhost:5000/",
  },

  configureWebpack: {
    devtool: "source-map",
  },

  chainWebpack: (config) => {
    config.plugin("copy").tap((args) => {
      args[0].push({
        from: path.resolve(__dirname, "node_modules/localforage/dist/localforage.min.js"),
        to: path.resolve(__dirname, "../project/static/frontend/localforage.min.js"),
      });
      return args;
    });
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

  pwa: {
    name: "City service",
    themeColor: "#009688",
    appleMobileWebAppCapable: "yes",
    iconPaths: {
      maskIcon: null,
    },
    start_url: "/user/profile",
    workboxPluginMode: "InjectManifest",
    workboxOptions: {
      swSrc: "src/service-worker.js",
    },
  },
};
