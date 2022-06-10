<template>
  <div class="item">
    <div class="row">
      <div class="col-lg-6 col-12 product-info">
        <router-link
          :to="{ name: 'product', params: { productId: product.id } }"
          class="img"
          ><img :src="product.image" alt="img"
        /></router-link>
        <h3>
          <router-link
            :to="{ name: 'product', params: { productId: product.id } }"
            >{{ product.name }}</router-link
          >
        </h3>
      </div>
      <div class="col-lg-3 col-12 qty">
        <span class="error" v-show="product.valid === false"
          >Доступно {{ product.available_quantity }}</span
        >
        <div class="counter">
          <button
            class="dec"
            @click="onDecrementClick"
            :disabled="product.quantity_to_order <= 1"
          >
            -
          </button>
          <span class="value" v-if="product.available_quantity !== null">
            {{ product.quantity_to_order }} из
            {{ product.available_quantity }}</span
          >
          <span class="value" v-else> {{ product.quantity_to_order }}</span>
          <button
            class="inc"
            @click="onIncrementClick"
            :disabled="isIncrementDisabled"
          >
            +
          </button>
        </div>
      </div>
      <div class="col-lg-3 col-12 price">
        {{ product.price * product.quantity_to_order }} BYN / сутки
      </div>
      <button class="del" @click="onDelete">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
          <path
            d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isIncrementDisabled() {
      if (this.product.available_quantity === null) return false;
      return this.product.quantity_to_order >= this.product.available_quantity;
    },
  },
  methods: {
    ...mapMutations("cart", {
      incrementProduct: "incrementProduct",
      decrementProduct: "decrementProduct",
      removeProduct: "removeProduct",
    }),
    onIncrementClick() {
      this.incrementProduct(this.product.id);
      this.$emit("increment", this.product.id);
    },
    onDecrementClick() {
      this.decrementProduct(this.product.id);
      this.$emit("decrement", this.product.id);
    },
    onDelete() {
      this.removeProduct(this.product.id);
      this.$emit("delete", this.product.id);
    },
  },
};
</script>

<style scoped>
.item {
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  transition: 0.3s;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
  position: relative;
}

.item .row {
  margin-top: -15px;
}

.item .row .product-info,
.item .row .qty,
.item .row .price {
  margin-top: 15px;
}

.item .product-info {
  display: flex;
  align-items: center;
}

.item .product-info .img {
  display: flex;
  width: 80px;
  height: 100px;
  justify-content: center;
  align-items: center;
}

.item .product-info .img img {
  max-width: 100%;
  max-height: 100%;
}

.item .product-info h3 {
  color: #333;
  transition: 0.3s;
  margin-left: 10px;
}

.item .product-info h3:hover {
  color: blue;
}

.item .del {
  position: absolute;
  top: -10px;
  right: -10px;
  height: 30px;
  width: 30px;
  outline: none;
  background-color: #fff;
  border-radius: 50%;
  padding: 0;
  border: none;
  cursor: pointer;
}

.item .del:hover svg {
  fill: #dc3545;
}

.item .del svg {
  fill: #000;
  width: 100%;
  height: 100%;
  transition: 0.3s;
}

.item .qty {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.item .qty .error {
  font-size: 13px;
  color: red;
}

.item .qty .counter {
  margin-top: 5px;
  display: flex;
  align-items: center;
}

.item .qty .counter span {
  margin: 0 10px;
  font-weight: 600;
}

.item .qty .counter .dec,
.item .qty .counter .inc {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  outline: none;
  border-radius: 50%;
  font-size: 20px;
  color: #fff;
  cursor: pointer;
}

.item .qty .counter .dec:disabled,
.item .qty .counter .inc:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.item .qty .counter .dec {
  background-color: #dc3545;
}

.item .qty .counter .inc {
  background-color: #0d6efd;
}

.item .price {
  display: flex;
  align-items: center;
  font-weight: 600;
}
</style>
