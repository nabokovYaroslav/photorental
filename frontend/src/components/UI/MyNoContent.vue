<template>
  <div class="no-content">
    <h2>
      <slot></slot>
    </h2>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.no-content {
  width: 100%;
}
.no-content h2 {
  text-align: center;
  padding: 30px 0;
  border: 2px dashed gray;
}
</style>
