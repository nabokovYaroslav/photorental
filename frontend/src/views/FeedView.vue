<template>
  <main>
    <header></header>
    <section>
      <div class="container">
        <div class="post" v-if="feed && !feedIsLoading">
          <div class="post-img">
            <img :src="feed.image" alt="" />
            <div class="post-date">
              <span class="month">{{ month | nameMonth }}</span>
              <span class="day">{{ day }}</span>
              <span class="year">{{ year }}</span>
            </div>
          </div>
          <div class="post-desc">
            <h3>{{ feed.name }}</h3>
            <p>{{ feed.description }}</p>
          </div>
        </div>
        <my-no-content v-else-if="!feed && !feedIsLoading"
          >Новость не существует или была удалена</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Feed from "@/api/feed";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      feed: null,
      feedIsLoading: false,
    };
  },
  created() {
    this.feedIsLoading = true;
    Feed.detail(this.$route.params.feedId)
      .then((response) => {
        this.feed = response.data;
        this.feedIsLoading = false;
      })
      .catch(() => {
        this.feedIsLoading = false;
      });
  },
  computed: {
    date() {
      return new Date(this.feed.created_at);
    },
    day() {
      return this.date.getDate();
    },
    month() {
      return this.date.getMonth();
    },
    year() {
      return this.date.getFullYear();
    },
  },
  filters: {
    nameMonth(value) {
      const months = {
        1: "Янв",
        2: "Фев",
        3: "Мар",
        4: "Апр",
        5: "Май",
        6: "Июн",
        7: "Июл",
        8: "Авг",
        9: "Сен",
        10: "Окт",
        11: "Ноя",
        12: "Дек",
      };
      return months[value + 1];
    },
  },
};
</script>

<style scoped>
header {
  padding-top: 75px;
}
.loader {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}
.post .post-img {
  position: relative;
  overflow: hidden;
  height: 300px;
}

.post .post-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post .post-img .post-date {
  position: absolute;
  min-width: 28px;
  min-height: 28px;
  line-height: 28px;
  text-align: center;
  background: #fff;
  display: flex;
  flex-direction: column;
  top: 10px;
  left: 10px;
}

.post .post-img .post-date span {
  display: block;
  font-size: 15px;
  font-weight: 700;
  padding: 5px 15px;
  text-transform: uppercase;
  line-height: 28px;
  text-align: center;
  font-family: "Quicksand", sans-serif;
}

.post .post-img .post-date span:nth-child(odd) {
  color: #000;
  background: #f1ec40;
}

.post .post-img .post-date span:nth-child(even) {
  color: #fff;
  background: #000;
}

.post .post-desc {
  border-left: 1px solid #fff;
  border-right: 1px solid #fff;
  padding: 20px 20px;
}

.post .post-desc h3 {
  margin: 5px 0 10px;
  color: #333;
  font-size: 24px;
  font-weight: 600;
  line-height: 36px;
  text-decoration: none;
}

.post .post-desc p {
  margin-bottom: 15px;
  margin-top: 0;
  color: #727272;
  font-size: 16px;
  font-weight: 500;
  line-height: 26px;
  word-break: break-word;
}
</style>
