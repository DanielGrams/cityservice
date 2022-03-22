describe("Places", () => {
  it("default", () => {
    cy.createCommonScenario().then(function () {
      cy.login("test@test.de");
      cy.visit("/places");
      cy.screenshot("Places");
      cy.wait(2000);
      cy.get("#main-table td:contains(Goslar)").click();

      cy.screenshot("Place");
      cy.get(".favorite-btn").click();
      cy.wait(2000);
      cy.get(".favorite-btn").click();

      cy.get(".tabs li.nav-item").eq(1).click();
      cy.screenshot("Weather");

      cy.get(".tabs li.nav-item").eq(2).click();
      cy.screenshot("Recycling");
      cy.get("#filter-input").type("berg");
      cy.wait(2000);
      cy.get("#select-recycling-street-table td:first").click();
      cy.screenshot("RecyclingStreet");
      cy.get(".favorite-btn").click();
      cy.wait(2000);
      cy.get(".favorite-btn").click();
    });
  });
});
