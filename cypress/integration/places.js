describe("Places", () => {
  it("default", () => {
    cy.createCommonScenario().then(function () {
      cy.login("test@test.de");
      cy.visit("/places");
      cy.screenshot("Places");
      cy.wait(2000);
      cy.get("#main-table td").eq(0).click();

      cy.screenshot("Place");
      cy.get(".favorite-btn").click();
      cy.wait(2000);
      cy.get(".favorite-btn").click();

      cy.get(".page-link:contains(2)").click();
    });
  });
});
