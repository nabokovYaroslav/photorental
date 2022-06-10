<template>
  <div class="item">
    <router-link
      :to="{ name: 'studio', params: { studioId: studio.id } }"
      class="img"
    >
      <img :src="studio.image" alt="img" />
    </router-link>
    <h3>
      <router-link :to="{ name: 'studio', params: { studioId: studio.id } }">
        {{ studio.name }}
      </router-link>
    </h3>
    <h4>
      {{ studio.description | shortDescription }}
    </h4>
    <span class="price">{{ studio.price }} BYN / час</span>
    <span>Телефон для аренды: {{ studio.phone }}</span>
    <router-link
      :to="{ name: 'studio', params: { studioId: studio.id } }"
      class="link"
    >
      Подробнее
    </router-link>
  </div>
</template>

<script>
export default {
  props: {
    studio: {
      type: Object,
      required: true,
    },
  },
  filters: {
    shortDescription(value) {
      return value.slice(0, 100);
    },
  },
};
</script>

<style scoped>
.item {
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
.item .img {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  height: 200px;
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
  transition: 0.3s;
}

.item h3:hover {
  color: blue;
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

.item .link {
  margin-top: 5px;
  text-decoration: underline;
  color: blue;
}

.item button {
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

.item button:hover {
  background-color: #f1ec40;
}
</style>
