import HTTP from "@/api/common";

export default {
  async list() {
    const response = await HTTP.get("studios/");
    return response;
  },
  async detail(studioId) {
    const response = await HTTP.get(`studios/${studioId}/`);
    return response;
  },
};
