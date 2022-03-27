import '@cypress/code-coverage/support'
import "./commands";
import failOnConsoleError from "cypress-fail-on-console-error";

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

  // From https://github.com/cypress-io/cypress/issues/702#issuecomment-435873135
  if (window.navigator && navigator.serviceWorker) {
		navigator.serviceWorker.getRegistrations()
			.then((registrations) => {
				registrations.forEach((registration) => {
					registration.unregister();
				});
			});
	}
});

Cypress.on('window:before:load', (win) => {
  delete win.navigator.__proto__.ServiceWorker
})

Cypress.on('uncaught:exception', (err, runnable, promise) => {
  // when the exception originated from an unhandled promise
  // rejection, the promise is provided as a third argument
  // you can turn off failing the test in this case
  if (promise) {
    return false
  }
  // we still want to ensure there are no other unexpected
  // errors, so we let them fail the test
})
