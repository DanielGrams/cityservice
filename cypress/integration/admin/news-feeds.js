describe("NewsFeeds", () => {
  it("default", () => {
    cy.createPlace().then(function (placeId) {
      cy.login("admin@test.de");
      cy.visit("/admin/news-feeds");
      cy.screenshot("list-empty");

      cy.get(".add-btn").click();
      cy.get("#publisher");
      cy.wait(1000); // Form gets cleared
      cy.get("#publisher").type("Polizei");
      cy.get("#url").type("http://www.polizei.de");
      cy.get(".submit-create-modal-btn").click();
      cy.screenshot("list");

      cy.assertNoToast();
      cy.get("td:contains(Polizei)").click();
      cy.get(".edit-btn");
      cy.screenshot("read");

      cy.assertNoToast();
      cy.get(".edit-btn").click();
      cy.get("#publisher").clear().type("Feuerwehr");
      cy.get("#place input").type("G");
      cy.get(".vbt-autcomplete-list").click();
      cy.get(".submit-update-modal-btn").click();
      cy.assertToast();

      cy.assertNoToast();
      cy.get(".delete-btn").click();
    });
  });
});
