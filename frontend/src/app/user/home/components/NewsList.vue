<template>
  <div class="">
    <DefaultList
      :url="url"
      :perPage="5"
      :showPagination="false"
      :showEmpty="false"
    >
      <template #item="{ item }">
        <div
          class="news-item d-flex flex-row align-items-center position-relative px-3 py-2"
        >
          <div>
            <div class="list-item-title">{{ item.content }}</div>
            <div class="list-item-detail">
              <img
                :src="item.publisher_icon_url"
                class="img-fluid rounded"
                style="
                  max-width: 20px;
                  border-radius: 10px !important;
                  vertical-align: sub;
                "
              />
              {{ item.news_feed.publisher }}
            </div>
            <div class="list-item-head">
              {{ item.published | moment("dd. DD.MM.YYYY") }}
            </div>
          </div>
          <a
            href="#"
            @click.prevent="newsItemClicked(item)"
            class="stretched-link"
          ></a>
        </div>
      </template>
      <template #footer>
        <b-list-group-item class="text-primary" :to="`/places/${place.id}`">
          {{
            $t("app.home.news.more", { placeName: place.name })
          }}</b-list-group-item
        >
      </template>
    </DefaultList>
  </div>
</template>

<script>
import { Browser } from "@capacitor/browser";
import DefaultList from "@/components/DefaultList";
export default {
  components: {
    DefaultList,
  },
  props: {
    place: {
      type: Object,
    },
  },
  computed: {
    url() {
      return `/api/places/${this.place.id}/news-items`;
    },
  },
  methods: {
    /* istanbul ignore next */
    newsItemClicked(item) {
      Browser.open({ url: item.link_url });
    },
  },
};
</script>
