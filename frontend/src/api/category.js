import HTTP from "@/api/common";

export default {
  async list() {
    const response = await HTTP.get("categories/");
    return response;
  },
  async filters(categoryId) {
    const response = await HTTP.get(`categories/${categoryId}/filters/`);
    return response;
  },
  async detail(categoryId) {
    const response = await HTTP.get(`categories/${categoryId}/`);
    return response;
  },
};
