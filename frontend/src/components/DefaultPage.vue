<template>
  <div>
    <b-navbar
      type="light"
      variant="light"
      fixed="top"
      :sticky="true"
      class="top-nav justify-content-between"
    >
      <b-navbar-nav>
        <slot name="left"></slot>
      </b-navbar-nav>
      <b-navbar-brand>
        {{ title }}
      </b-navbar-brand>
      <b-navbar-nav>
        <slot name="right"></slot>
      </b-navbar-nav>
    </b-navbar>
    <div class="container px-0 px-md-5">
      <slot name="default"></slot>
    </div>
  </div>
</template>
<script>
export default {
  name: "DefaultPage",
  props: {
    title: {
      type: String,
    },
  },
};
</script>
