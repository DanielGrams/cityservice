module.exports = {
    outputDir: '../project/static/frontend',
    devServer: {
      proxy: {
        '/api*': {
          target: 'http://localhost:5000/'
        }
      }
    }
  }