describe("Root", () => {
  it("simple", () => {
    cy.visit("/");
    cy.screenshot("home");

    cy.visit("/news");
    cy.screenshot("news");
  });
});
