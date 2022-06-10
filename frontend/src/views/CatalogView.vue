<template>
  <main>
    <header></header>
    <section class="catalog">
      <div class="container">
        <div class="title">
          <h1>Каталог проката</h1>
          <span></span>
        </div>
        <category-list
          class="row categories"
          v-if="categories.length !== 0 && !categoriesIsLoading"
        >
          <div
            class="col-12 col-sm-6 col-md-4 col-lg-3"
            v-for="category in categories"
            :key="category.id"
          >
            <category-item :category="category" />
          </div>
        </category-list>
        <my-no-content
          v-else-if="categories.length === 0 && !categoriesIsLoading"
          >Пока нет каталога</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Category from "@/api/category";
import CategoryList from "@/components/CategoryList";
import CategoryItem from "@/components/CategoryItem";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    CategoryList,
    CategoryItem,
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      categories: [],
      categoriesIsLoading: false,
    };
  },
  created() {
    this.categoriesIsLoading = true;
    Category.list()
      .then((response) => {
        this.categories = response.data;
        this.categoriesIsLoading = false;
      })
      .catch(() => {
        this.categoriesIsLoading = false;
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

.catalog .categories {
  margin-top: 20px;
}

.catalog .categories > * {
  margin-top: 30px;
}
</style>
