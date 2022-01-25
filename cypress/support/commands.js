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
  cy.logexec("flask test reset");
});