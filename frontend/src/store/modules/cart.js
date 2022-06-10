function getCart() {
  let cart = localStorage.getItem("cart");
  if (cart === null) return [];
  cart = JSON.parse(cart);
  if (!Array.isArray(cart)) return [];
  return cart;
}

export default {
  namespaced: true,
  state: {
    cart: getCart(),
  },
  getters: {
    count(state) {
      return state.cart.reduce((sum, product) => {
        return sum + product.count;
      }, 0);
    },
    cart(state) {
      return state.cart;
    },
  },
  mutations: {
    addProduct(state, productId) {
      state.cart.push({ product_id: productId, count: 1 });
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },
    removeProduct(state, productId) {
      const index = state.cart
        .map((product) => {
          return product.product_id;
        })
        .indexOf(productId);
      state.cart.splice(index, 1);
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },
    incrementProduct(state, productId) {
      const index = state.cart
        .map((product) => {
          return product.product_id;
        })
        .indexOf(productId);
      state.cart[index].count += 1;
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },
    decrementProduct(state, productId) {
      const index = state.cart
        .map((product) => {
          return product.product_id;
        })
        .indexOf(productId);
      state.cart[index].count -= 1;
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },
  },
  actions: {},
};
