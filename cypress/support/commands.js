Cypress.Commands.add("logexec", (command) => {
  return cy.exec(command, { failOnNonZeroExit: false }).then(function (result) {
    if (result.code) {
      throw new Error(`Execution of "${command}" failed
          Exit code: ${result.code}
          Stdout:\n${result.stdout}
          Stderr:\n${result.stderr}`);
    }

    return result;
  });
});

Cypress.Commands.add("setup", () => {
  cy.logexec("flask test reset --seed && flask users create test@test.de --password password --active && flask users create admin@test.de --password password --active && flask roles add admin@test.de admin");
});

Cypress.Commands.add("createCommonScenario", () => {
  cy.logexec("flask test create-common-scenario");
});

Cypress.Commands.add("createNewsItem", () => {
  cy.logexec("flask test news-item-create");
});

Cypress.Commands.add("createNewsFeed", () => {
  cy.logexec("flask test news-feed-create");
});

Cypress.Commands.add("createPlace", () => {
  cy.logexec("flask test place-create");
});

Cypress.Commands.add("assertValid", (fieldId) => {
  cy.get("#" + fieldId).should("have.class", "is-valid");
  cy.get("#" + fieldId + "-error").should("have.value", "");
});

Cypress.Commands.add("assertInvalid", (fieldId, msg) => {
  cy.get("#" + fieldId).should("have.class", "is-invalid");
  cy.get("#" + fieldId + "-error").should("contain", msg);
});

Cypress.Commands.add("assertRequired", (fieldId) => {
  cy.assertInvalid(fieldId, "Pflichtfeld");
});

Cypress.Commands.add("assertErrorToast", (msg) => {
  cy.contains(".toast-body", msg);
});

Cypress.Commands.add("assertNoToast", () => {
  cy.get(".toast-body", { timeout: 10000 }).should("not.exist");
});

Cypress.Commands.add(
  "login",
  (email = "test@test.de", password = "password", redirectTo = "/user/profile") => {
    let loginUrl = "/login";

    if (redirectTo != "/user/profile") {
      loginUrl += "?redirectTo=" + redirectTo
    }

    cy.visit(loginUrl);
    cy.get("#email").type(email);
    cy.get("#password").type(password);
    cy.get("#submit").click();

    cy.url().should("include", redirectTo);
    cy.getCookie("session").should("exist");
  }
);
