<template>
  <main>
    <header></header>
    <section class="checkout">
      <div class="container">
        <div class="title">
          <h1>Корзина</h1>
          <span></span>
        </div>
        <div
          class="cart-wrapper"
          v-if="products.length !== 0 && !productsIsLoading"
        >
          <div
            class="choose-date-wrapper"
            v-if="availableProducts.length !== 0"
          >
            <h2 class="h2">Выбор срока эксплуатации</h2>
            <div class="choose-date">
              <div class="row">
                <div class="col-12 col-md-6">
                  <div class="form-group">
                    <label for="start-date">Я планирую забрать технику</label>
                    <br />
                    <date-picker
                      v-model="startDate"
                      type="datetime"
                      @close="onClose"
                      :time-picker-options="{
                        start: '09:00',
                        step: '00:30',
                        end: '21:00',
                        format: 'HH:mm',
                      }"
                      @clear="onDateTimeClear"
                      :disabled-date="disabledStartDateBeforeTommorowAndEndDate"
                      format="DD.MM.YYYY HH:mm"
                      value-type="date"
                    ></date-picker>
                  </div>
                </div>
                <div class="col-12 col-md-6">
                  <div class="form-group">
                    <label for="end-date">Я планирую отдать технику</label>
                    <br />
                    <date-picker
                      v-model="endDate"
                      type="datetime"
                      @close="onClose"
                      :time-picker-options="{
                        start: '09:00',
                        step: '00:30',
                        end: '21:00',
                        format: 'HH:mm',
                      }"
                      @clear="onDateTimeClear"
                      :disabled-date="disabledEndDateBeforeTommorowAndStartDate"
                      format="DD.MM.YYYY HH:mm"
                      value-type="date"
                    ></date-picker>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="cart" v-if="products.length !== 0">
            <div class="available-items" v-if="availableProducts.length !== 0">
              <cart-item
                v-for="product in availableProducts"
                :key="product.id"
                :product="product"
                @increment="onIncrement"
                @decrement="onDecrement"
                @delete="onDelete"
              />
            </div>
            <h2 v-if="unavailableProducts.length !== 0" class="h2">
              Недоступны к оформлению
            </h2>
            <div
              class="unavailable-items"
              v-if="unavailableProducts.length !== 0"
            >
              <cart-unavailable-item
                v-for="product in unavailableProducts"
                :key="product.id"
                :product="product"
                @delete="onDelete"
              />
            </div>
          </div>
          <div
            class="info-wrapper"
            v-if="startDate && endDate && !reservedQuantityLoading"
          >
            <h2 class="h2">Предварительная информация</h2>
            <div class="info">
              <div class="row">
                <div class="col-12">
                  <div class="info-group">
                    <div class="info-caption">Количество товара</div>
                    <div class="info-value">
                      {{ availableProductsQuantity }} шт.
                    </div>
                  </div>
                </div>
                <div class="col-12">
                  <div class="info-group">
                    <div class="info-caption">Количество дней</div>
                    <div class="info-value">{{ orderDays }}</div>
                  </div>
                </div>
                <div class="col-12">
                  <div class="info-group">
                    <div class="info-caption">Итого</div>
                    <div class="info-value">{{ orderPrice }} BYN</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            class="contacts-wrapper"
            v-if="startDate && endDate && !reservedQuantityLoading"
          >
            <h2 class="h2">Контакты</h2>
            <form @submit.prevent="onFormSubmit">
              <div class="form-group">
                <span
                  class="error"
                  :class="{ active: surname.error.isVisible }"
                  >{{ surname.error.message }}</span
                >
                <my-input
                  placeholder="Фамилия"
                  v-model="surname.value"
                  @input="onSurnameInput"
                />
              </div>
              <div class="form-group">
                <span class="error" :class="{ active: name.error.isVisible }">{{
                  name.error.message
                }}</span>
                <my-input
                  placeholder="Имя"
                  v-model="name.value"
                  @input="onNameInput"
                />
              </div>
              <div class="form-group">
                <span
                  class="error"
                  :class="{ active: phone.error.isVisible }"
                  >{{ phone.error.message }}</span
                >
                <my-input
                  placeholder="Телефон"
                  v-model="phone.value"
                  @input="onPhoneInput"
                />
              </div>
              <div class="loader" v-if="formIsSubmitting">
                <my-spinner :size="38" />
              </div>
              <button v-else :disabled="!formIsValid">Оформить заказ</button>
            </form>
          </div>
        </div>
        <my-no-content v-else-if="products.length === 0 && !productsIsLoading"
          >Ваша корзина пуста</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
    <my-dialog :show="show" @hide="onHide">
      <h2 class="h3">
        Ваш заказ успешно добавлен. В скорем времени мы с Вами свяжемся
      </h2>
    </my-dialog>
  </main>
</template>

<script>
import Order from "@/api/order";
import { mapGetters, mapMutations } from "vuex";
import DatePicker from "vue2-datepicker";
import "vue2-datepicker/index.css";
import "vue2-datepicker/locale/ru";
import Product from "@/api/product";
import CartItem from "@/components/CartItem";
import CartUnavailableItem from "@/components/CartUnavailableItem";
import MyInput from "@/components/UI/MyInput";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";
import MyDialog from "@/components/UI/MyDialog";

export default {
  components: {
    CartItem,
    CartUnavailableItem,
    DatePicker,
    MyInput,
    MySpinner,
    MyNoContent,
    MyDialog,
  },
  data() {
    return {
      products: [],
      productsIsLoading: false,
      startDate: null,
      endDate: null,
      reservedQuantityLoading: false,
      surname: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      name: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      phone: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: false,
      },
      show: false,
      formIsSubmitting: false,
    };
  },
  computed: {
    ...mapGetters("cart", {
      cart: "cart",
      count: "count",
    }),
    availableProducts() {
      return this.products.filter((product) => {
        return product.quantity !== 0;
      });
    },
    unavailableProducts() {
      return this.products.filter((product) => {
        return product.quantity === 0;
      });
    },
    availableProductsQuantity() {
      return this.availableProducts.reduce((sum, product) => {
        return sum + product.quantity_to_order;
      }, 0);
    },
    orderPrice() {
      return (
        this.availableProducts.reduce((sum, product) => {
          return sum + product.quantity_to_order * product.price;
        }, 0) * this.orderDays
      );
    },
    orderDays() {
      if (this.startDate && this.endDate) {
        const time = this.endDate.getTime() - this.startDate.getTime();
        return Math.ceil(time / (1 * 24 * 3600 * 1000));
      }
      return 0;
    },
    formIsValid() {
      return (
        this.startDate &&
        this.endDate &&
        this.availableProducts.filter((product) => {
          return product.valid !== true;
        }).length === 0 &&
        this.surname.valid &&
        this.name.valid &&
        this.phone.valid
      );
    },
  },
  methods: {
    ...mapMutations("cart", {
      removeProduct: "removeProduct",
    }),
    onIncrement(productId) {
      const index = this.products
        .map((product) => {
          return product.id;
        })
        .indexOf(productId);
      this.products[index].quantity_to_order += 1;
      if (this.products[index].available_quantity !== null) {
        if (
          this.products[index].quantity_to_order >
          this.products[index].available_quantity
        ) {
          this.products[index].valid = false;
        } else {
          this.products[index].valid = true;
        }
      }
    },
    onDecrement(productId) {
      const index = this.products
        .map((product) => {
          return product.id;
        })
        .indexOf(productId);
      this.products[index].quantity_to_order -= 1;
      if (this.products[index].available_quantity !== null) {
        if (
          this.products[index].quantity_to_order >
          this.products[index].available_quantity
        ) {
          this.products[index].valid = false;
        } else {
          this.products[index].valid = true;
        }
      }
    },
    disabledStartDateBeforeTommorowAndEndDate(date) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const tommorow = new Date(today.getTime() + 1 * 24 * 3600 * 1000);
      if (this.endDate) {
        const endDate = this.endDate;
        endDate.setHours(0, 0, 0, 0);
        return (
          date.getTime() < tommorow.getTime() ||
          date.getTime() >= endDate.getTime()
        );
      }
      return date.getTime() < tommorow.getTime();
    },
    disabledEndDateBeforeTommorowAndStartDate(date) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const dayAfterTommorow = new Date(today.getTime() + 2 * 24 * 3600 * 1000);
      if (this.startDate) {
        const startDate = new Date(this.startDate.getTime());
        startDate.setHours(0, 0, 0, 0);
        return (
          date.getTime() < dayAfterTommorow.getTime() ||
          date.getTime() <= startDate.getTime()
        );
      }
      return date.getTime() < dayAfterTommorow.getTime();
    },
    onClose() {
      if (this.startDate && this.endDate) {
        const expectedTimezoneOffset = -3;
        const timezoneOffset = new Date().getTimezoneOffset() / 60;
        const UTCHours = expectedTimezoneOffset - timezoneOffset;
        const startDate = new Date(
          this.startDate.setUTCHours(this.startDate.getUTCHours() + UTCHours)
        ).toISOString();
        const endDate = new Date(
          this.endDate.setUTCHours(this.endDate.getUTCHours() + UTCHours)
        ).toISOString();
        this.products.forEach((product) => {
          product.available_quantity = null;
          product.valid = null;
        });
        const products = this.availableProducts.map((product) => {
          return product.id;
        });
        this.reservedQuantityLoading = true;
        Product.productsReservedQuantity(products, startDate, endDate)
          .then((response) => {
            response.data.forEach((product) => {
              const index = this.products
                .map((product) => {
                  return product.id;
                })
                .indexOf(product.id);
              this.products[index].available_quantity =
                this.products[index].quantity - product.reserved_quantity;
              this.products[index].valid =
                this.products[index].quantity_to_order >
                this.products[index].available_quantity
                  ? false
                  : true;
            });
            this.reservedQuantityLoading = false;
          })
          .catch(() => {
            this.reservedQuantityLoading = false;
          });
      }
    },
    onDateTimeClear() {
      this.products.forEach((product) => {
        product.available_quantity = null;
        product.valid = null;
      });
    },
    onSurnameInput() {
      if (this.surname.value.length == 0) {
        this.surname.valid = false;
        this.surname.error.message = "Обязательное поле";
        this.surname.error.isVisible = true;
        return;
      }
      if (this.surname.value.length > 255) {
        this.surname.valid = false;
        this.surname.error.message =
          "Фамилия не может быть больше 255 символов";
        this.surname.error.isVisible = true;
        return;
      }
      this.surname.valid = true;
      this.surname.error.message = "";
      this.surname.error.isVisible = false;
    },
    onNameInput() {
      if (this.name.value.length == 0) {
        this.name.valid = false;
        this.name.error.message = "Обязательное поле";
        this.name.error.isVisible = true;
        return;
      }
      if (this.name.value.length > 255) {
        this.name.valid = false;
        this.name.error.message = "Имя не может быть больше 255 символов";
        this.name.error.isVisible = true;
        return;
      }
      this.name.valid = true;
      this.name.error.message = "";
      this.name.error.isVisible = false;
    },
    onPhoneInput() {
      if (this.phone.value.length == 0) {
        this.phone.valid = false;
        this.phone.error.message = "Обязательное поле";
        this.phone.error.isVisible = true;
        return;
      }
      if (!/^(\+375|80)(29|25|44|33)\d{7}$/.test(this.phone.value)) {
        this.phone.valid = false;
        this.phone.error.message =
          "Телефон должен быть в формате (+375|80)(29|25|44|33)XXXXXXX где X это цифры";
        this.phone.error.isVisible = true;
        return;
      }
      this.phone.valid = true;
      this.phone.error.message = "";
      this.phone.error.isVisible = false;
    },
    onFormSubmit() {
      this.formIsSubmitting = true;
      const expectedTimezoneOffset = -3;
      const timezoneOffset = new Date().getTimezoneOffset() / 60;
      const UTCHours = expectedTimezoneOffset - timezoneOffset;
      const startDate = new Date(
        this.startDate.setUTCHours(this.startDate.getUTCHours() + UTCHours)
      ).toISOString();
      const endDate = new Date(
        this.endDate.setUTCHours(this.endDate.getUTCHours() + UTCHours)
      ).toISOString();
      const products = this.availableProducts.map((product) => {
        return {
          product: product.id,
          count: product.quantity_to_order,
        };
      });
      Order.create(
        this.surname.value,
        this.name.value,
        this.phone.value,
        startDate,
        endDate,
        products
      ).then((response) => {
        this.name.value = "";
        this.surname.value = "";
        this.phone.value = "";
        response.data.products_in_order.forEach((product) => {
          const index = this.products
            .map((product) => {
              return product.id;
            })
            .indexOf(product.product);
          this.removeProduct(product.product);
          this.products.splice(index, 1);
        });
        this.startDate = null;
        this.endDate = null;
        this.show = true;
        this.formIsSubmitting = false;
      });
    },
    onHide(show) {
      this.show = show;
    },
    onDelete(productId) {
      const index = this.products
        .map((product) => {
          return product.id;
        })
        .indexOf(productId);
      this.products.splice(index, 1);
    },
  },
  created() {
    this.productsIsLoading = true;
    const productIds = this.cart.map((product) => {
      return product.product_id;
    });
    Product.products_in_cart({ id: productIds })
      .then((response) => {
        this.products = response.data;
        for (let i = 0; i < this.products.length; i++) {
          const index = this.cart
            .map((product) => {
              return product.product_id;
            })
            .indexOf(this.products[i].id);
          this.$set(
            this.products[i],
            "quantity_to_order",
            this.cart[index].count
          );
          this.$set(this.products[i], "valid", null);
          this.$set(this.products[i], "available_quantity", null);
        }
        this.productsIsLoading = false;
      })
      .catch(() => {
        this.productsIsLoading = false;
      });
  },
};
</script>

<style scoped>
.h2 {
  margin: 15px 0;
  color: #333;
  font-size: 24px;
}

.h3 {
  color: #333;
  font-size: 24px;
  text-align: center;
  padding: 30px;
}

.loader {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

header {
  padding-top: 75px;
}

.checkout .items {
  margin-top: 20px;
}

.checkout .items > * {
  margin-top: 30px;
}

.checkout .info {
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
  margin-top: 20px;
}

.checkout .info .row {
  margin-top: -10px;
}

.checkout .info label {
  font-size: 15px;
  color: #333;
  font-weight: 600;
}

.checkout .info input {
  margin-top: 5px;
}

.checkout .info .form-group {
  margin-top: 10px;
}

.checkout .info .info-group {
  margin-top: 10px;
  padding: 10px 0;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
}

.checkout .info .info-group .info-value {
  font-weight: 600;
}

.checkout .info .row {
  width: 100%;
}

.checkout form button {
  margin: 20px auto 0 auto;
  display: block;
  padding: 8px 20px;
  font-size: 16px;
  border-radius: 17px;
  border: 2px solid #198754;
  color: #198754;
  font-weight: 600;
  transition: 0.3s;
  background-color: #fff;
  align-self: center;
  cursor: pointer;
}

.checkout form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checkout form button:hover {
  background-color: #198754;
  color: #fff;
}

.choose-date {
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  transition: 0.3s;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
  margin-top: 20px;
}

.available-items {
  margin-top: 15px;
}

form {
  padding: 10px;
  background-color: #fff;
  border-radius: 10px;
  transition: 0.3s;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
}

form .form-group .error {
  font-size: 14px;
  color: red;
  display: none;
}

form .form-group .error.active {
  display: block;
}

form .form-group input {
  margin-top: 5px;
}

form .form-group {
  margin-top: 15px;
}
</style>
