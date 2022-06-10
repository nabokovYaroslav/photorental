<template>
  <feed-list v-if="!newsIsLoading">
    <template v-if="news.length !== 0">
      <div class="col-12 col-md-6 col-lg-4" v-for="feed in news" :key="feed.id">
        <feed-item :feed="feed" />
      </div>
    </template>
    <my-no-content v-else>Пока нет новостей</my-no-content>
  </feed-list>
  <div class="loader" v-else>
    <my-spinner :size="50" />
  </div>
</template>

<script>
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
    };
  },
  created() {
    this.newsIsLoading = true;
    Feed.list()
      .then((response) => {
        this.news = response.data.results;
        this.newsIsLoading = false;
      })
      .catch(() => {
        this.newsIsLoading = false;
      });
  },
};
</script>

<style scoped>
.loader {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}
</style>
