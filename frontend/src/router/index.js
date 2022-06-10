import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "@/views/HomeView";
import CatalogView from "@/views/CatalogView";
import ContactView from "@/views/ContactView";
import NewsView from "@/views/NewsView";
import StudiosView from "@/views/StudiosView";
import FAQView from "@/views/FAQView";
import FeedView from "@/views/FeedView";
import StudioView from "@/views/StudioView";
import ProductView from "@/views/ProductView";
import CategoryProductsView from "@/views/CategoryProductsView";
import CartView from "@/views/CartView";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/catalog",
    name: "catalog",
    component: CatalogView,
  },
  {
    path: "/catalog/:categoryId",
    name: "category",
    component: CategoryProductsView,
  },
  {
    path: "/contacts",
    name: "contacts",
    component: ContactView,
  },
  {
    path: "/news",
    name: "news",
    component: NewsView,
  },
  {
    path: "/news/:feedId",
    name: "feed",
    component: FeedView,
  },
  {
    path: "/studios",
    name: "studios",
    component: StudiosView,
  },
  {
    path: "/studios/:studioId",
    name: "studio",
    component: StudioView,
  },
  {
    path: "/faq",
    name: "faq",
    component: FAQView,
  },
  {
    path: "/products/:productId",
    name: "product",
    component: ProductView,
  },
  {
    path: "/cart",
    name: "cart",
    component: CartView,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
