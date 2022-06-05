<template>
  <DefaultPage :title="$t('app.places.list.title')">
    <DefaultList url="/api/places">
      <template #item="{ item }">
        <div class="p-2">
          {{ item.name }}
          <b-link :to="`/places/${item.id}`" class="stretched-link"></b-link>
        </div>
      </template>
    </DefaultList>
  </DefaultPage>
</template>

<script>
export default {};
</script>
