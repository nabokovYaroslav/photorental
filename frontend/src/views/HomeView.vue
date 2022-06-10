<template>
  <main>
    <header>
      <div class="container">
        <div class="text">
          <h1>PHOTO RENTAL</h1>
          <p>Прокат фотооборудования и аренда студий в Могилеве</p>
        </div>
        <div class="links">
          <router-link :to="{ name: 'catalog' }">Каталог</router-link>
          <router-link :to="{ name: 'studios' }">Студии</router-link>
        </div>
      </div>
      <div class="overlay"></div>
    </header>
    <section class="news-items">
      <div class="container">
        <div class="title">
          <h2>Новинки</h2>
          <span></span>
        </div>
        <new-product-list class="row items" />
      </div>
    </section>
    <section class="top-rental">
      <div class="container">
        <div class="title">
          <h2>Топ проката</h2>
          <span></span>
        </div>
        <top-product-list class="row items" />
      </div>
    </section>
    <section class="news">
      <div class="container">
        <div class="title">
          <h2>Последние новости</h2>
          <span></span>
        </div>
        <latest-feed-list class="row posts" />
      </div>
    </section>
  </main>
</template>

<script>
import NewProductList from "@/components/NewProductList";
import TopProductList from "@/components/TopProductList";
import LatestFeedList from "@/components/LatestFeedList";
export default {
  components: {
    NewProductList,
    TopProductList,
    LatestFeedList,
  },
};
</script>

<style scoped>
/* header */

header {
  background-image: url("@/assets/images/background.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  position: relative;
  padding: 200px 0;
}

header .overlay {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

header .container {
  z-index: 2;
  position: relative;
}

header .text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

header .text h1 {
  font-size: 60px;
  color: #f1ec40;
}

header .text p {
  font-size: 25px;
  color: #e3e3e3;
  font-weight: 600;
  margin-top: 20px;
}

header .links {
  margin-top: 30px;
  margin-left: -15px;
  display: flex;
}

header .links > a {
  margin-left: 15px;
  display: block;
  padding: 8px 20px;
  font-size: 16px;
  border-radius: 17px;
  border: 2px solid #e3e3e3;
  color: #e3e3e3;
  font-weight: 600;
  transition: 0.3s;
}

header .links > a:hover {
  color: #f1ec40;
  border-color: #f1ec40;
}

/* header */
</style>
