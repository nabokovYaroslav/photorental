<template>
  <main>
    <header></header>
    <section class="news">
      <div class="container">
        <div class="title">
          <h2>Новости</h2>
          <span></span>
        </div>
        <feed-list class="row" v-if="news.length !== 0 && !newsIsLoading">
          <div
            class="col-12 col-md-6 col-lg-4"
            v-for="feed in news"
            :key="feed.id"
          >
            <feed-item :feed="feed" />
          </div>
        </feed-list>
        <my-no-content v-else-if="news.length === 0 && !newsIsLoading"
          >Пока нет новостей</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
        <div class="observer" ref="observer"></div>
      </div>
    </section>
  </main>
</template>

<script>
import axios from "axios";
import Feed from "@/api/feed";
import FeedList from "@/components/FeedList";
import FeedItem from "@/components/FeedItem";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    FeedList,
    FeedItem,
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      news: [],
      newsIsLoading: false,
      next: null,
      observer: null,
    };
  },
  created() {
    const options = {
      rootMargin: "0px",
      threshold: 1.0,
    };
    const callback = (entries, observer) => {
      if (entries[0].isIntersecting) {
        observer.unobserve(this.$refs.observer);
        this.loadMoreNews();
      }
    };
    this.observer = new IntersectionObserver(callback, options);
    this.newsIsLoading = true;
    Feed.list()
      .then((response) => {
        this.news = response.data.results;
        this.next = response.data.next;
        this.observe();
        this.newsIsLoading = false;
      })
      .catch(() => {
        this.newsIsLoading = false;
      });
  },
  methods: {
    async loadMoreNews() {
      const response = await axios.get(this.next);
      this.news.push(...response.data.results);
      this.next = response.data.next;
      this.observe();
    },
    observe() {
      if (this.next !== null) {
        this.observer.observe(this.$refs.observer);
      }
    },
  },
};
</script>

<style scoped>
.news .observer {
  height: 30px;
  background-color: transparent;
}
header {
  padding-top: 75px;
}

.loader {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.news .row {
  margin-top: 20px;
}

.news .row > * {
  margin-top: 30px;
}
</style>
