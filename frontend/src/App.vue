<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand href="/">
        <img
          src="@/assets/apple-touch-icon.png"
          width="30"
          height="30"
          class="d-inline-block align-top rounded"
          alt="Logo"
        />
        Goslar Service App
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">News</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="body-content">
      <router-view />
      <footer>
        <p class="text-center">
          Mit <b-icon icon="heart-fill" style="color: red"></b-icon> in
          <strong>Goslar</strong> entwickelt.
        </p>
        <p class="text-center small">
          <a href="/impressum">Impressum</a> |
          <a href="/impressum">Kontakt</a> |
          <a href="/datenschutz">Datenschutz</a>
        </p>
      </footer>
    </div>
  </div>
</template>

<style>
.navbar {
    background-color: lightslategray;
    font-size: 1em;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    color: white;
    padding: 8px 5px 8px 5px;
}

.navbar a {
    text-decoration: none;
    color: inherit;
}

.navbar-brand {
    font-size: 1.2em;
    font-weight: 600;
}

.navbar-item {
    font-variant: small-caps;
    margin-left: 30px;
}
</style>
