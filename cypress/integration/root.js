describe("Root", () => {
  it("simple", () => {
    cy.visit("/");
    cy.screenshot("home");

    cy.createNewsItem();
    cy.visit("/news");
    cy.url().should("include", "/news");
    cy.get("h5:contains(Feuerwehr)");
    cy.screenshot("news");
  });
});
