module.exports = {
    outputDir: '../static/frontend',
    devServer: {
      proxy: {
        '/api*': {
          target: 'http://localhost:5000/'
        }
      }
    }
  }