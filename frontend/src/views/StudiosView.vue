<template>
  <main>
    <header></header>
    <section class="studios">
      <div class="container">
        <div class="title">
          <h2>Аренда студий</h2>
          <span></span>
        </div>
        <studio-list
          class="row"
          v-if="studios.length !== 0 && !studiosIsLoading"
        >
          <div
            class="col-12 col-md-6 col-lg-4"
            v-for="studio in studios"
            :key="studio.id"
          >
            <studio-item :studio="studio" />
          </div>
        </studio-list>
        <my-no-content v-else-if="studios.length === 0 && !studiosIsLoading"
          >Пока нет студий</my-no-content
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
import StudioList from "@/components/StudioList";
import StudioItem from "@/components/StudioItem";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    StudioList,
    StudioItem,
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      studios: [],
      studiosIsLoading: false,
      next: null,
    };
  },
  created() {
    this.studiosIsLoading = true;
    Studio.list()
      .then((response) => {
        this.studios = response.data.results;
        this.next = response.data.next;
        this.studiosIsLoading = false;
      })
      .catch(() => {
        this.studiosIsLoading = false;
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

.studios .row {
  margin-top: 20px;
}

.studios .row > * {
  margin-top: 30px;
}
</style>
