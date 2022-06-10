<template>
  <main>
    <header></header>
    <section>
      <div class="container">
        <div class="title">
          <h1>FAQ</h1>
          <span></span>
        </div>
        <h2>
          Здесь Вы найдете ответы на часто задаваемые вопросы, касающиеся правил
          работы нашей компании.
        </h2>
        <div class="faq-items" v-if="faqs.length !== 0 && !faqsIsLoading">
          <div class="faq-item" v-for="faq in faqs" :key="faq.id">
            <div class="faq-question">
              {{ faq.question }}
            </div>
            <div class="faq-answer">
              {{ faq.answer }}
            </div>
          </div>
        </div>
        <my-no-content v-else-if="faqs.length === 0 && !faqsIsLoading"
          >Пока нет ответов на самые часто задавемые вопросы</my-no-content
        >
        <div class="loader" v-else>
          <my-spinner :size="50" />
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import FAQ from "@/api/faq";
import MySpinner from "@/components/UI/MySpinner";
import MyNoContent from "@/components/UI/MyNoContent";

export default {
  components: {
    MySpinner,
    MyNoContent,
  },
  data() {
    return {
      faqs: [],
      faqsIsLoading: false,
    };
  },
  created() {
    this.faqsIsLoading = true;
    FAQ.list()
      .then((response) => {
        this.faqs = response.data;
        this.faqsIsLoading = false;
      })
      .catch(() => {
        this.faqsIsLoading = false;
      });
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
h2 {
  font-size: 17px;
}

.faq-items {
  margin-top: 30px;
}

.faq-items .faq-item {
  margin-top: 20px;
}

.faq-items .faq-item .faq-question {
  font-weight: 600;
  font-style: italic;
  padding-bottom: 5px;
  border-bottom: 2px solid #eee;
  color: #333;
}

.faq-items .faq-item .faq-answer {
  margin-top: 5px;
  font-size: 15px;
}
</style>
