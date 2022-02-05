<template>
  <div class="p-3">
    <b-list-group>
      <b-list-group-item
        v-for="item in items"
        :key="item.id"
        :href="item.link_url"
        target="_blank"
      >
        <div class="d-flex flex-row align-items-center">
          <div class="m-3" style="max-width: 40px">
            <img
              :src="item.publisher_icon_url"
              class="img-fluid rounded"
              style="max-width: 40px"
            />
          </div>
          <div class="">
            <small>{{ item.published | moment("dd. DD.MM.YYYY") }}</small>
            <h5 class="mb-1">{{ item.publisher_name }}</h5>
            <p class="mb-1">{{ item.content }}</p>
          </div>
        </div>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "NewsList",
  props: {
    msg: String,
  },
  data() {
    return {
      items: null,
    };
  },
  created() {
    axios.get('/api/newsitems').then((response) => {
      this.items = response.data;
    });
  },
};
</script>
