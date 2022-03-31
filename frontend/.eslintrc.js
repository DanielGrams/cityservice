module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended',
    'plugin:@intlify/vue-i18n/recommended'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  ignorePatterns: ["src/app/root/views/*.vue"],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    "@intlify/vue-i18n/no-raw-text": [
      "warn",
      {
        "ignorePattern": "^[-#:()&]+$",
        "ignoreText": ["Goslar", "|"]
      }
    ]
  },
  settings: {
    'vue-i18n': {
      localeDir: './src/locales/**/*.json',
      messageSyntaxVersion: '^8.26.3'
    }
  }
}
