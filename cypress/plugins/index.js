/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)
const fs = require("fs");
/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  require("@cypress/code-coverage/task")(on, config);
  on("after:screenshot", (details) => {
    const newPath = details.path
      .replace(/ \(\d*\)/i, "")
      .replace(".png", "-" + config.viewportWidth + ".png");

    return new Promise((resolve, reject) => {
      fs.rename(details.path, newPath, (err) => {
        if (err) return reject(err);
        resolve({ path: newPath });
      });
    });
  });

  return config;
};
