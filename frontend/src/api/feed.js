import HTTP from "@/api/common";

export default {
  async list() {
    const response = await HTTP.get("news/");
    return response;
  },
  async detail(feedId) {
    const response = await HTTP.get(`news/${feedId}/`);
    return response;
  },
};
