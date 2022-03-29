import '@cypress/code-coverage/support'
import "./commands";
import failOnConsoleError from "cypress-fail-on-console-error";
require('cypress-failed-log')
require('cypress-terminal-report/src/installLogsCollector')({
  xhr: {
    printHeaderData: true,
    printRequestData: true,
  }
});

failOnConsoleError();

before(() => {
  if (Cypress.browser.family === "chromium") {
    Cypress.automation("remote:debugger:protocol", {
      command: "Network.setCacheDisabled",
      params: { cacheDisabled: true },
    });
  }
});

beforeEach(() => {
  cy.setup();
});
