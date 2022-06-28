<template>
  <div class="mobile-nav" :class="{ active: active }">
    <div class="link-wrapper">
      <ul>
        <li>
          <router-link :to="{ name: 'home' }" @click.native="$emit('close')"
            >Главная</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'catalog' }" @click.native="$emit('close')"
            >Прокат оборудования</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'studios' }" @click.native="$emit('close')"
            >Аренда студии</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'faq' }" @click.native="$emit('close')"
            >FAQ</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'news' }" @click.native="$emit('close')"
            >Новости</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'contacts' }" @click.native="$emit('close')"
            >Контакты</router-link
          >
        </li>
      </ul>
    </div>
    <div class="layout" @click="$emit('close')"></div>
  </div>
</template>

<script>
export default {
  props: {
    active: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.mobile-nav {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  visibility: hidden;
  z-index: 10;
}

.mobile-nav.active {
  visibility: visible;
}

.mobile-nav .link-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  right: -100%;
  z-index: 1;
  min-width: 200px;
  overflow: hidden;
  transition: 0.3s;
}

.mobile-nav .link-wrapper ul {
  display: flex;
  flex-direction: column;
  transition: 0.3s;
  background-color: #35302d;
  height: 100%;
  overflow-y: auto;
}

.mobile-nav.active .link-wrapper {
  right: 0;
}

.mobile-nav .layout {
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 0;
  position: absolute;
  transition: 0.3s;
  visibility: hidden;
  opacity: 0;
}

.mobile-nav.active .layout {
  visibility: visible;
  opacity: 1;
}

ul::-webkit-scrollbar {
  width: 3px; /* ширина для вертикального скролла */
  height: 3px; /* высота для горизонтального скролла */
  background-color: #cecece;
}

ul::-webkit-scrollbar-thumb {
  background-color: #f1ec40;
  border-radius: 9em;
  box-shadow: inset 1px 1px 10px #f1ec40;
}

ul::-moz-scrollbar-button:decrement,
ul::-moz-scrollbar-button:increment,
ul::-webkit-scrollbar-button:decrement,
ul::-webkit-scrollbar-button:increment {
  width: 0px;
}

li {
  position: relative;
  border-bottom: solid 1px #3c3735;
}

li a {
  display: block;
  position: relative;
  z-index: 1;
  transition: 0.35s ease color;
  padding: 1.1em 10px;
  color: #dfdbd9;
  text-align: center;
}

li a:hover {
  color: #f1ec40;
}

li a:hover::before {
  left: -5px;
}

li a::before {
  content: "";
  display: block;
  z-index: -1;
  position: absolute;
  left: calc(-100% - 5px);
  top: 0;
  width: 100%;
  height: 100%;
  border-right: solid 5px #f1ec40;
  background: #3c3735;
  transition: 0.35s ease left;
}
</style>
