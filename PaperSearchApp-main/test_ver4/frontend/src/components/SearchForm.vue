<template>
  <v-form @submit.prevent="submitSearch" class="search-form">
    <select v-model="localPrefix" class="classic">
      <option value="all">ALL</option>
      <option value="ti">Title</option>
      <option value="au">Author</option>
      <option value="abs">Abstract</option>
      <option value="co">Comment</option>
      <option value="jr">Journal Reference</option>
      <option value="cat">Subject Category</option>
      <option value="rn">Report Number</option>
      <option value="id">ID</option>
    </select>
    <input
      v-model="localQuery"
      type="text"
      placeholder="キーワードを入力"
    />
    <v-btn type="submit" class="search-button bg-black" >検索</v-btn>
  </v-form>
</template>

<script>
export default {
  name: "SearchForm",
  props: {
    query: {
      type: String,
      default: "",
    },
    prefix: {
      type: String,
      default: "all",
    }
  },
  data() {
    return {
      localQuery: this.query,
      localPrefix: this.prefix,
    };
  },
  methods: {
    submitSearch() {
      this.$emit("search", {
        prefix: this.localPrefix,
        query: this.localQuery,
      });
    },
  },
};
</script>

<style scoped>
.search-form {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.search-select,
.search-input {
  margin-right: 10px;
}
.search-button {
  padding: 6px 12px;
}

input,
select {
  /* styling */
  background-color: white;
  border: thin solid black;
  border-radius: 4px;
  display: inline-block;
  font: inherit;
  line-height: 1.5em;
  padding: 0.5em 3.5em 0.5em 1em;
  /* reset */
  margin: 0;      
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  margin-right: 10px;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.classic {
  background-image:
    linear-gradient(45deg, transparent 50%, gray 50%),
    linear-gradient(135deg, gray 50%, transparent 50%),
    linear-gradient(to right, black, black);
  background-position:
    calc(100% - 20px) calc(1em + 2px),
    calc(100% - 15px) calc(1em + 2px),
    100% 0;
  background-size:
    5px 5px,
    5px 5px,
    2.5em 2.5em;
  background-repeat: no-repeat;
}
select.classic:focus {
  background-image:
    linear-gradient(45deg, white 50%, transparent 50%),
    linear-gradient(135deg, transparent 50%, white 50%),
    linear-gradient(to right, gray, gray);
  background-position:
    calc(100% - 15px) 1em,
    calc(100% - 20px) 1em,
    100% 0;
  background-size:
    5px 5px,
    5px 5px,
    2.5em 2.5em;
  background-repeat: no-repeat;
  border-color: grey;
  outline: 0;
}
</style>
