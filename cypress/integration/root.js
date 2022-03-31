describe("Root", () => {
  it("simple", () => {
    cy.visit("/");
    cy.screenshot("home");

    cy.visit("/impressum");
    cy.screenshot("Impressum");

    cy.visit("/datenschutz");
    cy.screenshot("Datenschutz");
  });
});
