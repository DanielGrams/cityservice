import httpService from "./http.service";

class AuthService {
  init() {
    return httpService
      .get("/auth/login", {
        headers: { "Content-Type": "application/json" },
      })
      .then(function (resp) {
        const csrf_token = resp.data["response"]["csrf_token"];

        return httpService
          .get("/api/user", {
            headers: {
              "X-CSRF-Token": csrf_token,
              "Referer": httpService.baseURL,
            },
            suppressErrorToast: true,
          })
          .then((response) => {
            return response.data;
          });
      });
  }

  login(email, password) {
    return httpService
      .get("/auth/login", {
        headers: { "Content-Type": "application/json" },
      })
      .then(function (resp) {
        const csrf_token = resp.data["response"]["csrf_token"];

        return httpService
          .post(
            "/auth/login",
            {
              email: email,
              password: password,
              remember: true,
            },
            {
              headers: {
                "X-CSRF-Token": csrf_token,
                "Referer": httpService.baseURL,
              },
              suppressErrorToast: true,
            }
          )
          .then((resp) => {
            return resp.data["response"]["user"];
          });
      });
  }

  logout() {
    return httpService.post("/auth/logout", null);
  }
}

export default new AuthService();
