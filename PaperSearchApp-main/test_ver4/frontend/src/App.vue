<template>
  <v-app>
    <v-container>
      <v-app-bar app class="bg-grey-lighten-2">
        <v-toolbar-title><img src="@/assets/arXiver_Z.png" /></v-toolbar-title>
        <template v-slot:append>
          <v-row class="results-header" justify="center">
            <v-col class="d-flex align-end">
              <SearchForm
                :query="$route.query.query"
                :prefix="$route.query.prefix"
                @search="submitSearch"
              />
            </v-col>
          </v-row>
        </template>
      </v-app-bar>
      <v-main>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <div v-if="!hasSearched" class="center-message">
              <h3>検索ボックスで検索してください</h3>
            </div>
            <div v-else>
              <ResultsTabs />
            </div>
            <router-view
              :key="$route.fullPath"
              @search="updateSearchState"
              @results="updateResults"
            ></router-view>
          </v-col>
        </v-row>
      </v-main>
    </v-container>
  </v-app>
</template>

<script>
import { defineAsyncComponent } from "vue";

const ResultsTabs = defineAsyncComponent(() =>
  import("./components/ResultsTabs.vue")
);
const SearchForm = defineAsyncComponent(() =>
  import("./components/SearchForm.vue")
);

export default {
  name: "App",
  components: {
    ResultsTabs,
    SearchForm,
  },
  data() {
    return {
      results: [],
      hasSearched: false,
    };
  },
  methods: {
    updateSearchState(searched) {
      this.hasSearched = searched;
    },
    updateResults(results) {
      this.results = results;
    },
    submitSearch({ prefix, query }) {
      this.hasSearched = true; // 検索実行時にhasSearchedをtrueに設定
      const currentTab = this.$route.name;
      const path =
        currentTab === "ChartResults" ? "/search/chart" : "/search/text";
      this.$router.push({
        path: path,
        query: { prefix, query },
      });
    },
  },
};
</script>

<style scoped>
.results-header {
  margin-top: 20px;
  text-align: center;
}

.results-header h1 {
  margin-bottom: 20px;
}

img {
  margin-top: 10px;
  height: 65px;
}

.center-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh; /* 画面の中央に表示するための高さ調整 */
  text-align: center;
}

.center-message h3 {
  margin: 0;
}
</style>
