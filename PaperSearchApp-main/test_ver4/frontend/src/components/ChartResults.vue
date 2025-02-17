<template>
  <div class="chart-wrapper">
    <div class="chart-container">
      <loading-spinner v-if="loading" />
      <div v-else>
        <div
          v-if="chartData.length"
          id="citationChart"
          class="full-width-height"
        ></div>
        <div v-else class="no-results">
          <p>一致する情報は見つかりませんでした。</p>
          <p>検索のヒント:</p>
          <ul>
            <li>キーワードに誤字・脱字がないか確認します。</li>
            <li>別のキーワードを試してみます。</li>
            <li>もっと一般的なキーワードに変えてみます。</li>
          </ul>
        </div>
        <div id="tooltip" class="tooltip"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import axios from "axios";
import LoadingSpinner from "./LoadingSpinner.vue";

export default {
  name: "ChartResults",
  components: {
    LoadingSpinner,
  },
  data() {
    return {
      chartData: [],
      loading: false,
      width: 1200, // 固定幅
      height: 700, // 固定高さ
      localQuery: this.$route.query.query || "", // ローカルクエリ
    };
  },
  methods: {
    async fetchResults() {
      this.loading = true;
      try {
        const response = await axios.post("http://localhost:5000/api/search", {
          prefix: this.$route.query.prefix || "all",
          query: this.$route.query.query || "",
        });
        this.chartData = response.data;
        this.chartData.sort((a, b) => b.citation - a.citation);
        this.chartData = this.chartData.slice(0, 20); // トップ20のチャートに絞る
        this.normalizeCitations();
        this.$nextTick(() => {
          if (this.chartData.length) {
            this.createChart();
          }
        });
        this.$emit("results", this.chartData);
        this.$emit("search", true);
      } catch (error) {
        console.error("API request failed:", error);
        alert("検索中にエラーが発生しました。後でもう一度お試しください。");
      } finally {
        this.loading = false;
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
    normalizeCitations() {
      const minCitation = Math.min(
        ...this.chartData.map((item) => item.citation)
      );
      const maxCitation = Math.max(
        ...this.chartData.map((item) => item.citation)
      );
      const range = maxCitation - minCitation;

      this.chartData = this.chartData.map((item) => ({
        ...item,
        normalizedCitation:
          range === 0 ? 100 : ((item.citation - minCitation) / range) * 99 + 1,
      }));
    },
    createChart() {
      const width = this.width;
      const height = this.height;

      d3.select("#citationChart").selectAll("*").remove(); // 既存のチャートをクリア

      const svg = d3
        .select("#citationChart")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      const pack = d3.pack().size([width, height]).padding(1.5);

      const root = d3
        .hierarchy({ children: this.chartData })
        .sum((d) => d.normalizedCitation);

      const nodes = pack(root).leaves();

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      const node = svg
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g")
        .attr("transform", (d) => `translate(${d.x},${d.y})`)
        .on("click", (event, d) => {          
          this.handleClick(d.data.id, d.data.link);
        })
        .on("mouseover", (event, d) => {
          const tooltip = d3.select("#tooltip");
          tooltip
            .style("opacity", 1)
            .html(
              `<strong>${d.data.title}</strong><br>引用数: ${d.data.citation}`
            )
            .style("left", `${event.pageX + 10}px`)
            .style("top", `${event.pageY - 200}px`);
        })
        .on("mouseout", () => {
          d3.select("#tooltip").style("opacity", 0);
        });

      node
        .append("circle")
        .attr("r", (d) => d.r)
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "black")
        .attr("stroke-width", 1);

      const getTextWidth = (text, font) => {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        context.font = font;
        return context.measureText(text).width;
      };

      const adjustFontSize = (text, radius) => {
        const maxFontSize = radius * 0.4;
        let fontSize = maxFontSize;
        const font = () => `${fontSize}px sans-serif`;
        while (fontSize > 12 && getTextWidth(text, font()) > radius * 2) {
          fontSize -= 1;
        }
        return fontSize;
      };

      node.each(function (d) {
        const group = d3.select(this);
        const fontSize = adjustFontSize(d.data.citation.toString(), d.r);

        group
          .append("text")
          .attr("dy", "0.3em")
          .attr("text-anchor", "middle")
          .attr("fill", "white")
          .attr("font-size", `${fontSize}px`)
          .text(d.data.citation);
      });
    },
  },
  mounted() {
    this.fetchResults();
  },
  unmounted() {
    d3.select("#citationChart").selectAll("*").remove(); // コンポーネントが破棄される際にチャートをクリア
  },
  watch: {
    "$route.query": {
      handler: "fetchResults",
      immediate: true,
    },
  },
};
</script>

<style scoped>
.chart-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.chart-container {
  width: 100%; /* 固定幅 */
  height: 100%; /* 固定高さ */
  position: absolute;
  top: 300px;
  right: 0;
  bottom: 0;
  left: 0;
  margin: auto;
}

#citationChart {
  width: 100%;
  height: 100%;
  text-align: center;
}

.tooltip {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.no-results {
  text-align: center;
  color: #555;
}
</style>
