<template>
  <div>
    <b-jumbotron
      header="Goslar Service App"
      lead="Die inoffizielle App"
      header-level="5"
      class="p-4"
    >
      <b-button variant="primary" to="/places">{{
        $t("app.menu.places")
      }}</b-button>
      <hr class="my-4" />

      <p>Features:</p>
      <ul>
        <li>
          <strong><a to="/news">News:</a></strong> Hier werden neue Meldungen
          aus offiziellen Kanälen wie
          <a href="https://www.landkreis-goslar.de/">Landkreis</a> und
          <a href="https://www.goslar.de">Stadt</a> angezeigt. Die News können
          außerdem im iOS-Heute-Widget angezeigt werden.
        </li>
        <li>
          <strong>Müllabfuhr: </strong>Nachdem du deine Straße ausgewählt hast,
          werden dir die Abfuhrtermine der
          <a
            href="https://www.kwb-goslar.de/Abfallwirtschaft/Abfuhr/Online-Abfuhrkalender"
            >Kreiswirtschaftsbetriebe</a
          >
          angezeigt. Die Termine können in den Kalender exportiert werden.
        </li>
      </ul>

      <div class="d-flex flex-row flex-wrap">
        <div class="p-2">
          <a
            href="https://play.google.com/store/apps/details?id=de.danielgrams.goslar_service&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1"
            ><img
              alt="Jetzt bei Google Play"
              src="https://play.google.com/intl/en_us/badges/static/images/badges/de_badge_web_generic.png"
              style="width: 150px; max-width: 100%"
          /></a>
        </div>
        <div class="p-2">
          <div style="margin: 0.6rem 0.6rem">
            <a
              href="https://apps.apple.com/de/app/goslar-service/id1503485350?mt=8"
              style="
                display: inline-block;
                overflow: hidden;
                background: url(https://linkmaker.itunes.apple.com/de-de/badge-lrg.svg?releaseDate=2020-03-30&kind=iossoftware&bubble=ios_apps)
                  no-repeat;
                width: 135px;
                height: 40px;
              "
            ></a>
          </div>
        </div>
      </div>

      <hr class="my-4" />
      <small
        >Google Play und das Google Play-Logo sind Marken von Google LLC.</small
      >
    </b-jumbotron>
  </div>
</template>

<script>
export default {};
</script>
