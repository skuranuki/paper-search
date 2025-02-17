<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          class="bg-gray"
        ></v-progress-circular>
        <p>検索中...</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "LoadingSpinner",
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
