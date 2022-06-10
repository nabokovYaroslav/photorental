<template>
  <main>
    <header></header>
    <section>
      <div class="container">
        <div class="item" v-if="studio && !studioIsLoading">
          <div class="img">
            <img :src="studio.image" alt="img" />
          </div>
          <h3>{{ studio.name }}</h3>
          <h4>{{ studio.description }}</h4>
          <span class="price">{{ studio.price }} BYN / час</span>
          <span>Телефон для аренды: {{ studio.phone }}</span>
        </div>
        <my-no-content v-else-if="!studio && !studioIsLoading"
          >Студия не существует или была удалена</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Studio from "@/api/studio";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      studio: null,
      studioIsLoading: false,
    };
  },
  created() {
    this.studioIsLoading = true;
    Studio.detail(this.$route.params.studioId)
      .then((response) => {
        this.studio = response.data;
        this.studioIsLoading = false;
      })
      .catch(() => {
        this.studioIsLoading = false;
      });
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
.item {
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.item .img {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.item .img img {
  max-width: 100%;
  max-height: 100%;
}

.item h3 {
  margin-top: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  color: #333;
}

.item h4 {
  font-weight: normal;
  margin-top: 5px;
  color: #727272;
  margin-bottom: 20px;
}

.item span {
  margin-top: 10px;
  font-weight: 600;
  margin-top: auto;
}
</style>
