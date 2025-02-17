<template>
  <v-container :class="{ searched: hasSearched }">
    <loading-spinner v-if="loading" />

    <div v-if="results.length || hasSearched">
      <!-- ここには結果表示のコード -->
    </div>

    <div
      v-if="results.length && !loading"
      class="results-container"
      justify="center"
    >
      <div
        v-for="result in results"
        :key="result.id"
        cols="12"
        md="8"
        class="result-item"
      >
        <v-sheet>
          <h2 class="result-title">
            <a
              :href="result.link"
              target="_blank"
              rel="noopener noreferrer"
              @click.prevent="handleClick(result.id, result.link)"
            >
              {{ result.title }}
            </a>
          </h2>
          <div v-html="renderMath(result.summary)" class="result-summary"></div>
          <div class="result-item">
            <strong>著者:</strong> {{ result.authors.join(", ") }} &nbsp;
            <strong>引用数:</strong> {{ result.citation }} &nbsp;
            <strong>閲覧数:</strong> {{ result.view }}
          </div>
        </v-sheet>
      </div>
    </div>
    <div
      v-else-if="hasSearched && !loading"
      class="no-results"
      justify="center"
    >
      <p>一致する情報は見つかりませんでした。</p>
      <p>検索のヒント:</p>
      <ul>
        <li>キーワードに誤字・脱字がないか確認します。</li>
        <li>別のキーワードを試してみます。</li>
        <li>もっと一般的なキーワードに変えてみます。</li>
      </ul>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapActions, mapGetters } from "vuex";
import katex from "katex";
import "katex/dist/katex.min.css";
import LoadingSpinner from "./LoadingSpinner.vue";

export default {
  name: "TextResults",
  components: {
    LoadingSpinner,
  },
  data() {
    return {
      results: [],
      hasSearched: false,
      loading: false,
    };
  },
  watch: {
    "$route.query": {
      handler: "search",
      immediate: true,
      deep: true,
    },
  },
  methods: {
    ...mapActions(["logClick"]),
    ...mapGetters(["getLogClick"]),
    async search() {
      if (this.$route.query.query) {
        this.loading = true;
        try {
          const response = await axios.post(
            "http://localhost:5000/api/search",
            {
              prefix: this.$route.query.prefix || "all",
              query: this.$route.query.query || "",
            }
          );
          this.results = response.data;
          this.hasSearched = true;
        } catch (error) {
          console.error("API request failed:", error);
          alert("検索中にエラーが発生しました。後でもう一度お試しください。");
        } finally {
          this.loading = false;
        }
      }
    },
    async handleClick(id, link) {
      try {
        await axios.post("http://localhost:5000/api/view_count", {
          id,
          link,
        });
        window.open(link, "_blank", "noopener noreferrer");
      } catch (error) {
        console.error("Error logging click:", error);
      }
    },
    renderMath(text) {
      return text.replace(/\$([^$]+)\$/g, (match, p1) => {
        try {
          return katex.renderToString(p1, {
            throwOnError: false,
          });
        } catch (e) {
          console.error("KaTeX rendering error:", e);
          return match;
        }
      });
    },
  },
};
</script>

<style scoped>
.results-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result-item {
  margin-bottom: 20px;
}

.result-title a {
  text-decoration: none;
  color: #1a0dab;
}

.result-summary {
  margin: 10px 0;
}

.result-details {
  font-size: 0.9em;
  color: #555;
}

.no-results {
  text-align: center;
  color: #555;
}
</style>
