describe("Root", () => {
  it("simple", () => {
    cy.visit("/");
    cy.screenshot("home");

    cy.visit("/news");
    cy.url().should("include", "/news");
    cy.screenshot("news");
  });
});
