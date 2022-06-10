<template>
  <router-link
    :to="{ name: 'category', params: { categoryId: category.id } }"
    class="category"
  >
    <div class="img">
      <img :src="category.image" alt="" />
    </div>
    <h2>{{ category.name }}</h2>
  </router-link>
</template>

<script>
export default {
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.category {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #e3e3e3;
  border: 1px solid #eee;
  box-shadow: 0 4px 20px 0 rgb(0 0 0 / 9%);
  padding: 8px;
  transition: 0.3s;
  height: 100%;
}

.category:hover {
  transform: scale(1.1);
}

.category .img {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.category .img img {
  max-height: 100%;
  max-width: 100%;
}

.category h2 {
  margin-top: 10px;
  color: #333;
  text-align: center;
  font-size: 19px;
}
</style>
