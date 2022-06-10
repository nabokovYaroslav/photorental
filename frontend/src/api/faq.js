import HTTP from "@/api/common";

export default {
  async list() {
    const response = await HTTP.get("faq/");
    return response;
  },
};
