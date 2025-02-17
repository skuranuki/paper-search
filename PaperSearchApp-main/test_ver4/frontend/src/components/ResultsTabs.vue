<template>
  <v-tabs v-model="activeTab">
    <v-tab
      :to="{ name: 'TextResults', query: $route.query }"
      :exact="true"
      @click="handleTabClick('TextResults')"
    >
      テキスト
    </v-tab>
    <v-tab
      :to="{ name: 'ChartResults', query: $route.query }"
      :exact="true"
      @click="handleTabClick('ChartResults')"
    >
      チャート
    </v-tab>
  </v-tabs>
</template>

<script>
export default {
  name: "ResultsTabs",
  data() {
    return {
      activeTab: this.$route.name,
    };
  },
  watch: {
    "$route.name": {
      immediate: true,
      handler(newVal) {
        this.activeTab = newVal;
      },
    },
  },
  methods: {
    handleTabClick(tabName) {
      this.activeTab = tabName;
      this.$router.push({
        name: tabName,
        query: this.$route.query,
      });
    },
  },
};
</script>

<style scoped>
.v-tabs {
  background-color: #fff;
}

.v-tab {
  color: black;
}

.v-tab--active {
  color: #1a0dab;
  border-bottom: 2px solid #1a0dab;
}
</style>
