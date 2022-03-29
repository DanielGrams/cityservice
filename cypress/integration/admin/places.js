describe("Places", () => {
  it("default", () => {
    cy.login("admin@test.de");
    cy.cvisit("/admin/places");
    cy.screenshot("list-empty");

    cy.get(".add-btn").click();
    cy.get("#name");
    cy.wait(1000); // Form gets cleared
    cy.get("#name").type("Goslar");
    cy.get(".submit-create-modal-btn").click();
    cy.screenshot("list");

    cy.get("td:contains(Goslar)").click();
    cy.get(".edit-btn");
    cy.screenshot("read");
    cy.get(".edit-btn").click();
    cy.get("#name").clear().type("Seesen");
    cy.get(".submit-update-modal-btn").click();

    cy.assertNoToast();
    cy.get(".delete-btn").click();
  });
});
