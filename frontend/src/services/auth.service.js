import axios from "axios";

class AuthService {
  init() {
    return axios
      .get("/auth/login", {
        data: null,
        headers: { "Content-Type": "application/json" },
      })
      .then(function (resp) {
        const csrf_token = resp.data["response"]["csrf_token"];

        return axios
          .get("/api/user", {
            headers: { "X-CSRF-Token": csrf_token },
            suppressErrorToast: true,
          })
          .then((response) => {
            return response.data;
          });
      });
  }

  login(email, password) {
    return axios
      .get("/auth/login", {
        data: null,
        headers: { "Content-Type": "application/json" },
      })
      .then(function (resp) {
        const csrf_token = resp.data["response"]["csrf_token"];

        return axios
          .post(
            "/auth/login",
            {
              email: email,
              password: password,
            },
            {
              headers: { "X-CSRF-Token": csrf_token },
              suppressErrorToast: true,
            }
          )
          .then((response) => {
            return response.data["response"]["user"];
          });
      });
  }

  logout() {
    return axios.post("/auth/logout", null);
  }
}

export default new AuthService();
