import { Http } from "@capacitor-community/http";

class HttpService {
  baseURL = "";
  withCredentials = true;
  handler = null;

  get(url, config = null) {
    let httpOptions = {
      method: "GET",
      url: this.buildAbsoluteUrl(url),
    };

    if (config && config.headers) {
      httpOptions.headers = config.headers;
    }

    if (config && config.params) {
      httpOptions.params = config.params;
    }

    return this.request(httpOptions, config);
  }

  delete(url, config = null) {
    let httpOptions = {
      method: "DELETE",
      url: this.buildAbsoluteUrl(url),
    };

    if (config && config.headers) {
      httpOptions.headers = config.headers;
    }

    if (config && config.params) {
      httpOptions.params = config.params;
    }

    return this.request(httpOptions, config);
  }

  post(url, data, config = null) {
    return this.patchPutPost("POST", url, data, config);
  }

  patch(url, data, config = null) {
    return this.patchPutPost("PATCH", url, data, config);
  }

  put(url, data = null, config = null) {
    return this.patchPutPost("PUT", url, data, config);
  }

  patchPutPost(method, url, data, config = null) {
    let headers = {
      "Content-Type": "application/json",
      ...((config && config.headers) || {}),
    };

    let httpOptions = {
      method: method,
      url: this.buildAbsoluteUrl(url),
      headers: headers,
    };

    if (data != null) {
      httpOptions.data = data;
    }

    return this.request(httpOptions, config);
  }

  request(httpOptions, config = null) {
    if (this.withCredentials) {
      httpOptions.webFetchExtra = {
        credentials: "include",
      };
    }

    if (httpOptions.params) {
      Object.keys(httpOptions.params).forEach((key) => {
        httpOptions.params[key] = "" + httpOptions.params[key];
      });
    }

    console.log("Request", httpOptions, config);
    this.handler?.handleHttpStart(config);

    return Http.request(httpOptions)
      .then((response) => {
        console.log("Response", response);

        if (response.error) {
          const error = new Error(response.error);
          error.response = response;
          throw error;
        }

        if (response.status < 200 || response.status >= 400) {
          const error = new Error(`Status ${response.status}`);
          error.response = response;
          throw error;
        }

        if (config) {
          this.handler?.handleHttpFinish(config);
        }

        return response;
      })
      .catch((error) => {
        console.log(error);
        error.config = config;
        this.handler?.handleHttpError(error);
        return Promise.reject(error);
      });
  }

  buildAbsoluteUrl(url) {
    return `${this.baseURL}${url}`;
  }
}

export default new HttpService();
