describe("Root", () => {
  it("simple", () => {
    cy.cvisit("/");
    cy.screenshot("home");

    cy.createNewsItem();
    cy.cvisit("/news");
    cy.url().should("include", "/news");
    cy.get("h5:contains(Feuerwehr)");
    cy.screenshot("news");
  });
});
