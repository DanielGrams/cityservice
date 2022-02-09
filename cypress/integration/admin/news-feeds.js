describe("NewsFeeds", () => {
  it("default", () => {
    cy.login("admin@test.de");
    cy.visit("/admin/news-feeds");
    cy.screenshot("list-empty");

    cy.get(".add-btn").click();
    cy.get("#publisher").type("Polizei");
    cy.get("#url").type("http://www.polizei.de");
    cy.get(".submit-create-modal-btn").click();
    cy.screenshot("list");

    cy.get("td:contains(Polizei)").click();
    cy.get(".edit-btn");
    cy.screenshot("read");
    cy.get(".edit-btn").click();
    cy.get("#publisher").clear().type("Feuerwehr");
    cy.get(".submit-update-modal-btn").click();

    cy.get(".delete-btn").click();
  });
});
