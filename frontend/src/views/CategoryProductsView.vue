<template>
  <main>
    <header></header>
    <section class="main">
      <div class="filters-button"><span>Фильтры</span></div>
      <div class="container">
        <div class="title">
          <h1>Фотоаппараты</h1>
          <span></span>
        </div>
        <div class="row">
          <div class="col-3 filters">
            <span class="caption">Фильтры</span>
            <div class="filter-items">
              <div
                class="filter-item"
                v-for="filter in filters"
                :key="filter.slug"
              >
                <span class="filter-caption">{{ filter.name }}</span>
                <div
                  class="filter-group"
                  v-for="choice in filter.enum_group.choices"
                  :key="choice.id"
                >
                  <input
                    type="checkbox"
                    :value="choice.value"
                    v-model="
                      checkedFilters[`eav__${filter.slug}__${filter.datatype}`]
                    "
                    @change="onFilterChange"
                    :id="choice.id"
                  />
                  <label :for="choice.id">{{ choice.value }}</label>
                </div>
              </div>
            </div>
          </div>
          <div class="col-9 products-container">
            <product-list
              v-if="products.length !== 0 && !productsIsLoading"
              class="row products"
            >
              <div class="col-12" v-for="product in products" :key="product.id">
                <product-item :product="product" />
              </div>
            </product-list>
            <my-no-content
              v-else-if="
                products.length === 0 &&
                !productsIsLoading &&
                !this.$route.query
              "
              >Пока нет товаров</my-no-content
            >
            <my-no-content
              v-else-if="
                products.length === 0 && !productsIsLoading && this.$route.query
              "
              >По вашим фильтрам ничего не найдено. Попробуйте изменить
              фильтры</my-no-content
            >
            <div class="loader" v-else>
              <my-spinner :size="50" />
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Category from "@/api/category";
import CategoryProduct from "@/api/categoryProduct";
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
      next: null,
      checkedFilters: {},
      filters: [],
      controller: null,
    };
  },
  computed: {
    query() {
      return this.$route.query;
    },
  },
  watch: {
    query: {
      handler: function () {
        this.loadProducts();
      },
      deep: true,
    },
  },
  methods: {
    loadProducts() {
      if (this.controller !== null) {
        this.controller.abort();
        this.controller = null;
      }
      this.controller = new AbortController();
      this.productsIsLoading = true;
      CategoryProduct.list(
        this.$route.params.categoryId,
        this.query,
        this.controller.signal
      )
        .then((response) => {
          this.products = response.data.results;
          this.next = response.data.next;
          this.productsIsLoading = false;
        })
        .catch(() => {
          this.productsIsLoading = false;
        });
    },
    onFilterChange() {
      this.$router.push({
        name: "category",
        params: { categoryId: this.$route.params.categoryId },
        query: this.checkedFilters,
      });
    },
  },
  created() {
    Category.filters(this.$route.params.categoryId).then((response) => {
      this.filters = response.data;
      this.filters.forEach((filter) => {
        const attribute = `eav__${filter.slug}__${filter.datatype}`;
        let value = this.query[attribute];
        if (value) {
          if (!Array.isArray(value)) {
            value = [value];
          }
        } else {
          value = [];
        }
        this.$set(this.checkedFilters, attribute, value);
      });
    });
    this.loadProducts();
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
.main .products {
  margin-top: 20px;
}

.main .products > * {
  margin-top: 30px;
}

.main .products .product {
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: 0.3s;
  height: 100%;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
}

.main .products .product .img {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.main .products .product .img img {
  max-width: 100%;
  max-height: 100%;
}

.main .products .product h3 {
  margin-top: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  color: #333;
  transition: 0.3s;
}

.main .products .product h3:hover {
  color: blue;
}

.main .products .product h4 {
  font-weight: normal;
  margin-top: 5px;
  color: #727272;
  margin-bottom: 20px;
}

.main .products .product span {
  margin-top: 10px;
  font-weight: 600;
  margin-top: auto;
}

.main .products .product .link {
  margin-top: 5px;
  text-decoration: underline;
  color: blue;
}

.main .products button {
  display: block;
  padding: 8px 20px;
  font-size: 16px;
  border-radius: 17px;
  border: 2px solid #000;
  color: #000;
  font-weight: 600;
  transition: 0.3s;
  background-color: #fff;
  align-self: center;
  cursor: pointer;
  margin-top: 20px;
}

.main .products button:hover {
  background-color: #f1ec40;
}

/* products */

/* filters */

.filters {
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: 0.3s;
  height: 100%;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
  margin-top: 50px;
}

.filters .caption {
  font-size: 17px;
  font-weight: 600;
  color: #333;
  margin-top: 10px;
  margin-left: 10px;
}

.filters .filter-items {
  margin-top: 10px;
  margin-left: 15px;
}

.filters .filter-items .filter-item {
  margin: 10px 0;
}

.filters .filter-items .filter-item .filter-caption {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.filters .filter-items .filter-item .filter-group {
  margin: 10px 0;
}

.filters-button {
  display: none;
  padding: 10px 0;
  position: fixed;
  background: #e3e3e3;
  border: 1px solid #eee;
  left: 0;
  top: calc(50% - 59.28px);
  cursor: pointer;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  font-size: 20px;
}

.filters-button span {
  writing-mode: vertical-rl;
  color: #333;
  pointer-events: none;
}

@media screen and (max-width: 991px) {
  .filters-button {
    display: block;
  }

  .filters {
    display: none;
  }
  .products-container {
    flex: 0 0 auto;
    width: 100%;
  }
}

.filters label {
  margin-left: 5px;
}
</style>
