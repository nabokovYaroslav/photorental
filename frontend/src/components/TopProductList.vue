<template>
  <product-list v-if="!productsIsLoading">
    <template v-if="products.length !== 0">
      <div
        class="col-12 col-md-6 col-lg-4"
        v-for="product in products"
        :key="product.id"
      >
        <product-item :product="product" />
      </div>
    </template>
    <my-no-content v-else>Пока нет товаров</my-no-content>
  </product-list>
  <div class="loader" v-else>
    <my-spinner :size="50" />
  </div>
</template>

<script>
import Product from "@/api/product";
import ProductList from "@/components/ProductList";
import ProductItem from "@/components/ProductItem";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    ProductList,
    ProductItem,
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      products: [],
      productsIsLoading: false,
    };
  },
  created() {
    this.productsIsLoading = true;
    Product.topProducts()
      .then((response) => {
        this.products = response.data.results;
        this.productsIsLoading = false;
      })
      .catch(() => {
        this.productsIsLoading = false;
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
