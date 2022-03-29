describe("User", () => {
  it("login", () => {
    // /profile without Login should redirect to Login
    cy.visit("/user/profile");
    cy.url().should("include", "/login");

    // Login
    cy.visit("/login");
    cy.screenshot("login");

    // Blank
    cy.get("#submit").click();
    cy.assertRequired("email");
    cy.assertRequired("password");

    // Email
    cy.get("#email").type("invalidmail");
    cy.assertInvalid("email", "Email muss eine gültige E-Mail-Adresse sein");

    cy.get("#email").clear().type("test@test.de");
    cy.assertValid("email");

    // Wrong password
    cy.get("#password").type("wrong");
    cy.assertValid("password");
    cy.get("#submit").click();
    cy.assertErrorToast("Die Anmeldung ist fehlgeschlagen.");

    // Password
    cy.get("#password").clear().type("password");
    cy.assertValid("password");

    // Submit
    cy.get("#submit").click();

    // Profile
    cy.url().should("include", "/user/profile");
    cy.screenshot("profile");

    // Redirect to profile if logged in
    cy.visit("/login");
    cy.url().should("include", "/user/profile");
  });

  it("loginWithRedirect", () => {
    cy.login("test@test.de", "password", "/news");

    // /admin without role should redirect to Profile
    cy.visit("/admin");
    cy.url().should("include", "/profile");

    // Logout
    cy.get("body").then($body => {
        if ($body.find("button.navbar-toggler:visible").length > 0) {
            cy.get("button.navbar-toggler").click();
        }
    });
    cy.get(".user-dropdown").click();
    cy.get(".user-dropdown .logout").click();
    cy.url().should("eq", Cypress.config().baseUrl + "/");

    // Admin
    cy.login("admin@test.de");
    cy.visit("/admin");
    cy.url().should("include", "/admin");
    cy.screenshot("admin");
  });

  it("profile", () => {
    cy.createCommonScenario().then(function () {
      cy.login("test@test.de");
      cy.visit("/user/profile");
      cy.screenshot("Profile");

      cy.visit("/user/profile");
      cy.wait(2000);
      cy.get("#user-recycling-street-table td:first").click();
      cy.url().should("include", "/recycling-streets/");

      cy.visit("/user/profile");
      cy.get(".remove-place-btn:first").click();
      cy.get(".remove-recycling-street-btn:first").click();

      cy.assertNoToast();
      cy.get("#add-place-btn").click();
      cy.screenshot("Places");
      cy.get(".favorite-btn:first").click();
      cy.wait(2000);
      cy.get(".favorite-btn:first").click();

      cy.visit("/user/profile");
      cy.get("#add-recycling-street-btn").click();
      cy.screenshot("Recycling streets places");

      cy.get("#select-place-table td").eq(3).click();
      cy.screenshot("Recycling streets");
      cy.get(".favorite-btn:first").click();
      cy.wait(2000);
      cy.get(".favorite-btn:first").click();
      cy.get("#filter-input").type("berg");
      cy.wait(2000);

      cy.visit("/user/profile");
      cy.wait(2000);
      cy.get("#user-place-table td:first").click();
      cy.url().should("include", "/places/");
    });
  });

});
