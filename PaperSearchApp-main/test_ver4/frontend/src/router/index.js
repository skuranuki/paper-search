import { createRouter, createWebHistory } from "vue-router";
import { defineAsyncComponent } from "vue";

const TextResults = defineAsyncComponent(() =>
  import("../components/TextResults.vue")
);
const ChartResults = defineAsyncComponent(() =>
  import("../components/ChartResults.vue")
);

const routes = [
  {
    path: "/",
    redirect: "/search/text",
  },
  {
    path: "/search",
    children: [
      {
        path: "text",
        name: "TextResults",
        component: TextResults,
      },
      {
        path: "chart",
        name: "ChartResults",
        component: ChartResults,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
