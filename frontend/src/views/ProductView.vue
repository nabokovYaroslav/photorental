<template>
  <main>
    <header></header>
    <section>
      <div class="container">
        <div class="product" v-if="product && !productIsLoading">
          <div class="img"><img :src="product.image" alt="img" /></div>
          <h3>{{ product.name }}</h3>
          <h4>
            {{ product.description }}
          </h4>
          <span class="price">{{ product.price }} BYN / сутки</span>
          <button v-if="!productInCart" @click="addProduct(product.id)">
            Добавить в корзину
          </button>
          <button v-else @click="removeProduct(product.id)">
            Удалить из корзины
          </button>
          <h2>Описание</h2>
          <div
            class="description"
            v-if="charachteristics.length !== 0 && !charachteristicsIsLoading"
          >
            <div
              class="description-item"
              v-for="charachteristic in charachteristics"
              :key="charachteristic.id"
            >
              <div class="description-caption">{{ charachteristic.name }}</div>
              <div
                class="description-group"
                v-for="attribute in charachteristic.attributes"
                :key="attribute.id"
              >
                <div class="row">
                  <div class="col-12 col-md-6">
                    <span class="property">{{ attribute.name }}</span>
                  </div>
                  <div class="col-12 col-md-6">
                    <span class="value">{{ attribute.value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <my-no-content
            v-else-if="
              charachteristics.length === 0 && !charachteristicsIsLoading
            "
          >
            У данного товара отсутствует подробная информация
          </my-no-content>
          <div class="loader" v-else>
            <my-spinner :size="50" />
          </div>
        </div>
        <my-no-content v-else-if="!product && !productIsLoading"
          >Товар не существует или был удален</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { mapMutations, mapGetters } from "vuex";

import Product from "@/api/product";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      product: null,
      productIsLoading: false,
      charachteristics: [],
      charachteristicsIsLoading: false,
    };
  },
  created() {
    this.productIsLoading = true;
    Product.detail(this.$route.params.productId)
      .then((response) => {
        this.product = response.data;
        this.loadCharachteristics();
        this.productIsLoading = false;
      })
      .catch(() => {
        this.productIsLoading = false;
      });
  },
  methods: {
    loadCharachteristics() {
      this.charachteristicsIsLoading = true;
      Product.productCharacteristics(this.$route.params.productId)
        .then((response) => {
          this.charachteristics = response.data;

          this.charachteristicsIsLoading = false;
        })
        .catch(() => {
          this.charachteristicsIsLoading = false;
        });
    },
    ...mapMutations("cart", {
      addProduct: "addProduct",
      removeProduct: "removeProduct",
    }),
  },
  computed: {
    ...mapGetters("cart", {
      cart: "cart",
    }),
    productInCart() {
      const index = this.cart
        .map((product) => {
          return product.product_id;
        })
        .indexOf(this.product.id);
      return index === -1 ? false : true;
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
  width: 100%;
}
.product {
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.product .img {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.product .img img {
  max-width: 100%;
  max-height: 100%;
}

.product h3 {
  margin-top: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  color: #333;
  transition: 0.3s;
}

.product h3:hover {
  color: blue;
}

.product h4 {
  font-weight: normal;
  margin-top: 5px;
  color: #727272;
  margin-bottom: 20px;
}

.product span {
  margin-top: 10px;
  font-weight: 600;
  margin-top: auto;
}

.product .link {
  margin-top: 5px;
  text-decoration: underline;
  color: blue;
}

.product button {
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

.product button:hover {
  background-color: #f1ec40;
}

.product h2 {
  margin-top: 20px;
}

.product .description {
  width: 100%;
  margin-top: 30px;
}

.product .description .description-caption {
  padding: 7px 10px;
  border-bottom: 1px solid #ccc;
  background: #f3f3f3;
  font-size: 15px;
  font-weight: 600;
}

.product .description .description-group {
  border-bottom: 1px solid #eee;
}

.product .description .description-group:last-child {
  border-bottom: none;
}

.product .description .description-group .property,
.product .description .description-group .value {
  padding: 10px 10px;
  display: block;
  font-size: 15px;
}

.product .description .description-group .property {
  font-weight: normal;
}
</style>
